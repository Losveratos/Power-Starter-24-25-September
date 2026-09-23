#!/usr/bin/env python3
"""Prüft einen PBIR-Bericht ohne Power BI Desktop.

1. Jede JSON-Datei mit "$schema" wird gegen das offizielle Microsoft-Schema validiert
   (geladen aus github.com/microsoft/json-schemas, zwischengespeichert in _Werkzeuge/pbip/.schema-cache/).
2. Jeder Feldbezug (Entity/Property in visual.json, report.json, page.json) muss im Semantikmodell
   existieren – Spalte oder Measure, passend zur Art des Bezugs (wie `pbir validate --fields`).
3. Seitenreihenfolge, Visual-Namen und Positionen (innerhalb der Seite) werden geprüft.

Aufruf:  python3 tools/pbip/validate_pbir.py <Name>.Report <feldliste.json>
Die Feldliste schreibt TmdlCheck (--inventory).
"""
import json
import sys
import urllib.request
from pathlib import Path

from jsonschema import Draft202012Validator, Draft7Validator
from referencing import Registry, Resource

HERE = Path(__file__).resolve().parent
CACHE = HERE / ".schema-cache"
MS = "https://developer.microsoft.com/json-schemas/"
GH = "https://raw.githubusercontent.com/microsoft/json-schemas/main/"


def fetch(uri):
    url = uri.replace(MS, GH)
    f = CACHE / url.replace(GH, "").replace("/", "__")
    if not f.exists():
        CACHE.mkdir(exist_ok=True)
        with urllib.request.urlopen(url, timeout=30) as r:
            f.write_bytes(r.read())
    return json.loads(f.read_text(encoding="utf-8"))


def retrieve(uri):
    return Resource.from_contents(fetch(uri))


REGISTRY = Registry(retrieve=retrieve)


def walk_fields(node, out, path=""):
    """Sammelt alle {Column|Measure|Aggregation…: {Expression: {SourceRef: {Entity}}, Property}}."""
    if isinstance(node, dict):
        for kind in ("Column", "Measure", "Hierarchy"):
            v = node.get(kind)
            if isinstance(v, dict) and "Property" in v:
                ent = v.get("Expression", {}).get("SourceRef", {}).get("Entity")
                if ent:
                    out.append((kind, ent, v["Property"], path))
        for k, v in node.items():
            walk_fields(v, out, f"{path}/{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk_fields(v, out, f"{path}[{i}]")


def main():
    report = Path(sys.argv[1])
    model = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    errors, checked = [], 0

    for f in sorted(report.rglob("*.json")) + sorted(report.glob("*.pbir")) + sorted(report.glob(".platform")):
        data = json.loads(f.read_text(encoding="utf-8"))
        uri = data.get("$schema") if isinstance(data, dict) else None
        if not uri:
            continue
        schema = fetch(uri)
        cls = Draft7Validator if "draft-07" in schema.get("$schema", "") else Draft202012Validator
        v = cls(schema, registry=REGISTRY)
        errs = sorted(v.iter_errors(data), key=lambda e: list(e.path))
        for e in errs:
            errors.append(f"SCHEMA  {f.relative_to(report)}: {'/'.join(map(str, e.path))}: {e.message[:200]}")
        checked += 1

        refs = []
        walk_fields(data, refs)
        for kind, ent, prop, p in refs:
            t = model.get(ent)
            if t is None:
                errors.append(f"FELD    {f.relative_to(report)}: Tabelle '{ent}' gibt es im Modell nicht ({p})")
            elif kind == "Measure" and prop not in t["measures"]:
                errors.append(f"FELD    {f.relative_to(report)}: Measure '{ent}'[{prop}] fehlt ({p})")
            elif kind == "Column" and prop not in t["columns"]:
                errors.append(f"FELD    {f.relative_to(report)}: Spalte '{ent}'[{prop}] fehlt ({p})")

    # Seiten und Visuals
    pages_meta = json.loads((report / "definition/pages/pages.json").read_text(encoding="utf-8"))
    n_visuals = 0
    for pid in pages_meta["pageOrder"]:
        pdir = report / "definition/pages" / pid
        page = json.loads((pdir / "page.json").read_text(encoding="utf-8"))
        if page["name"] != pid:
            errors.append(f"SEITE   {pid}: name in page.json ({page['name']}) passt nicht zum Ordner")
        for vf in sorted((pdir / "visuals").glob("*/visual.json")):
            vis = json.loads(vf.read_text(encoding="utf-8"))
            n_visuals += 1
            if vis["name"] != vf.parent.name:
                errors.append(f"VISUAL  {vf.parent.name}: name passt nicht zum Ordner")
            pos = vis.get("position", {})
            if not all(k in pos for k in ("x", "y", "width", "height")):
                continue                                   # meldet schon die Schemaprüfung
            if pos["x"] < 0 or pos["y"] < 0 or pos["x"] + pos["width"] > page["width"] or pos["y"] + pos["height"] > page["height"]:
                errors.append(f"VISUAL  {vf.parent.name}: ragt über den Seitenrand")
    if pages_meta["activePageName"] not in pages_meta["pageOrder"]:
        errors.append("SEITE   activePageName steht nicht in pageOrder")

    print(f"{checked} Dateien gegen Microsoft-Schemas geprüft · {len(pages_meta['pageOrder'])} Seite(n) · {n_visuals} Visuals")
    for e in errors:
        print(e)
    print("OK – keine Fehler" if not errors else f"{len(errors)} Fehler")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
