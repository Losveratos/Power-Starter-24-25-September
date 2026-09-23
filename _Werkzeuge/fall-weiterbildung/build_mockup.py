#!/usr/bin/env python3
"""Baut das Seiten-Mockup „Weiterbildungs-Monitoring" mit der echten MockupKitchen.

Der Zustand (Modell, Layout, Kacheln, Steckbriefe) wird hier beschrieben und in die MockupKitchen
geladen; die Exporte erzeugt das Tool selbst – dieselben Dateien, die man sonst über
„Export für Claude Code" herunterlädt.

Ergebnis in 03-Fall-Weiterbildung/Mockup/:
  weiterbildungs-monitoring.mockup.json   in MockupKitchen über „Öffnen" laden und weiterbearbeiten
  mockup-spec.json, AGENT-BRIEF.md, WORKSHOP-DOKU.md, pbir-visuals.<Seite>.json, page-1-<Seite>.png

Aufruf (aus dem Repo-Root, mit einem Klon der Knowledge Kitchen daneben):
  pip install playwright
  python3 _Werkzeuge/fall-weiterbildung/build_mockup.py ../PowerBI-Kitchen-
Chromium: PLAYWRIGHT_CHROMIUM=/pfad/zu/chrome setzen, falls Playwright keinen eigenen Browser hat.
"""
import base64
import functools
import http.server
import json
import os
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

CASE = Path(__file__).resolve().parents[2] / "03-Fall-Weiterbildung"
OUT = CASE / "Mockup"


# ---------------------------------------------------------------- Modell (wie das Trainingsmodell der Anleitung)
def col(name, typ="string", desc=""):
    return {"name": name, "kind": "column", "type": typ, "desc": desc, "hidden": False, "format": ""}


def mea(name, fmt, desc=""):
    return {"name": name, "kind": "measure", "type": "measure", "desc": desc, "hidden": False, "format": fmt}


MODEL = {
    "source": "Weiterbildungs-Monitoring (Trainingsmodell, 03-Fall-Weiterbildung)",
    "tables": [
        {"name": "fakt_buchungen", "desc": "Eine Zeile je Kursbuchung aus dem LMS", "columns": [
            col("BuchungsID", "int64"), col("Personalnr"), col("Kursnr"), col("Buchungsdatum", "dateTime"),
            col("Kursbeginn", "dateTime"), col("Kursende", "dateTime"), col("Status", "string", "abgeschlossen · storniert · No-Show · angemeldet"),
            col("Stunden", "double"), col("Kosten", "decimal"), col("Feedback", "int64", "1–5, leer = nicht bewertet")], "measures": []},
        {"name": "dim_mitarbeitende", "desc": "HR-Stamm, eine Zeile je Person (pseudonymisiert)", "columns": [
            col("Personalnr"), col("BereichID"), col("Standort"), col("Rolle"), col("Beschaeftigung", "string", "Vollzeit / Teilzeit"),
            col("FTE", "double"), col("Altersgruppe"), col("Eintritt", "dateTime")], "measures": []},
        {"name": "dim_bereich", "desc": "Organisationsbereiche", "columns": [
            col("BereichID"), col("Bereich"), col("Ressort"), col("Kostenstelle")], "measures": []},
        {"name": "dim_kurs", "desc": "Kurskatalog", "columns": [
            col("Kursnr"), col("Kurstitel"), col("Kategorie"), col("Format"), col("Anbieter"), col("Pflicht", "string", "Ja / Nein"),
            col("Dauer_h", "double"), col("Listenpreis", "decimal")], "measures": []},
        {"name": "Kalender", "desc": "Kalender 2025", "columns": [
            col("Datum", "dateTime"), col("Jahr", "int64"), col("Quartal"), col("MonatNr", "int64"), col("Monat"), col("Monatsanfang", "dateTime")], "measures": []},
        {"name": "Budget", "desc": "Weiterbildungsbudget je Bereich und Quartal (entpivotiert)", "columns": [
            col("Bereich"), col("Quartal"), col("Budget", "decimal"), col("Quartalsanfang", "dateTime")], "measures": []},
        {"name": "Zielwerte", "desc": "Zielwerte je Bereich und Kennzahl (entpivotiert)", "columns": [
            col("Bereich"), col("Kennzahl"), col("Zielwert", "double")], "measures": []},
        {"name": "_Measures", "desc": "Kennzahlen (Loesungen/DAX/measures.dax)", "columns": [], "measures": [
            mea("Headcount", "#,##0", "Anzahl Personen im HR-Stamm"),
            mea("Teilnahmen", "#,##0", "Buchungen mit Status abgeschlossen"),
            mea("Stunden", "#,##0", "Weiterbildungsstunden aus abgeschlossenen Buchungen"),
            mea("Ø Stunden je MA", "#,##0.0", "Stunden ÷ Headcount (alle Personen, auch ohne Weiterbildung)"),
            mea("Teilnahmequote", "0.0%", "Personen mit ≥ 1 abgeschlossener freiwilliger Weiterbildung ÷ Headcount"),
            mea("Pflichtquote", "0.0%", "Personen, die alle Pflichtkurse abgeschlossen haben ÷ Headcount"),
            mea("Kosten", "#,##0", "Summe Kosten inkl. No-Show und Stornogebühren"),
            mea("Kosten je MA", "#,##0", "Kosten ÷ Headcount"),
            mea("Stornoquote", "0.0%"), mea("No-Show-Quote", "0.0%"),
            mea("Ø Zufriedenheit", "0.00", "Mittelwert der Bewertungen 1–5"),
            mea("Budget", "#,##0"), mea("Δ Budget", "#,##0", "Kosten − Budget"), mea("Budget-Ausschöpfung", "0.0%"),
            mea("Ziel Ø Stunden je MA", "#,##0.0", "nach Headcount gewichtet"),
            mea("Ziel Teilnahmequote", "0.0%"), mea("Ziel Pflichtquote", "0.0%"), mea("Ziel Zufriedenheit", "0.0")]},
    ],
}
FIELDS = {f"{t['name']}.{f['name']}": (t["name"], f) for t in MODEL["tables"] for f in t["columns"] + t["measures"]}


def F(ref):
    table, f = FIELDS[ref]
    return {"table": table, "name": f["name"], "kind": f["kind"], "type": f["type"], "isNew": False}


_n = 0


def nid(prefix):
    global _n
    _n += 1
    return f"wb{prefix}{_n:02d}"


def leaf(kind, engine, title, roles, sub="", scenario="AC/PL", analysis=None, notes="", priority="must", status="agreed", content=""):
    return {"id": nid("t"), "type": "leaf", "visual": {
        "kind": kind, "engine": engine, "title": title, "sub": sub, "scenario": scenario,
        "roles": {k: [F(r) for r in v] for k, v in roles.items()}, "notes": notes, "link": "", "content": content,
        "priority": priority, "status": status, "openQuestion": False, "analysis": analysis or {}, "interaction": {}}}


def row(children):
    return {"id": nid("r"), "type": "split", "dir": "row", "children": [{"size": s, "node": n} for s, n in children]}


def column(children):
    return {"id": nid("c"), "type": "split", "dir": "col", "children": [{"size": s, "node": n} for s, n in children]}


M = "_Measures."
KPIS = row([
    [1, leaf("kpi", "ck", "Teilnahmequote", {"indicator": [M + "Teilnahmequote"], "goal": [M + "Ziel Teilnahmequote"]},
             sub="vs. Ziel", analysis={"unit": "%", "decimals": 1},
             notes="Anteil der Belegschaft mit mindestens einer freiwilligen Weiterbildung. Pflichtkurse zählen nicht mit.")],
    [1, leaf("kpi", "ck", "Ø Stunden je MA", {"indicator": [M + "Ø Stunden je MA"], "goal": [M + "Ziel Ø Stunden je MA"]},
             sub="vs. Ziel", analysis={"unit": "h", "decimals": 1},
             notes="Nenner ist der Headcount – Personen ohne Weiterbildung ziehen den Schnitt bewusst nach unten.")],
    [1, leaf("kpi", "ck", "Pflichtquote", {"indicator": [M + "Pflichtquote"], "goal": [M + "Ziel Pflichtquote"]},
             sub="alle 3 Pflichtkurse", analysis={"unit": "%", "decimals": 1},
             notes="Compliance-relevant: Datenschutz, Arbeitsschutz, Verhaltenskodex. Ziel 95 %.")],
    [1, leaf("kpi", "ck", "Kosten", {"indicator": [M + "Kosten"], "goal": [M + "Budget"]},
             sub="vs. Budget", analysis={"unit": "€", "displayUnits": "K", "decimals": 0, "polarity": "lower"},
             notes="Weniger ist besser (Polarität gesetzt): Überschreitung = rot.")],
    [1, leaf("kpi", "ck", "Ø Zufriedenheit", {"indicator": [M + "Ø Zufriedenheit"], "goal": [M + "Ziel Zufriedenheit"]},
             sub="Skala 1–5", analysis={"decimals": 2},
             notes="Mittelwert ist hier richtig: jede Bewertung zählt gleich. Nur abgeschlossene, bewertete Kurse.")],
])
ZEILE2 = row([
    [3, leaf("columns", "ck", "Kosten vs. Budget je Quartal", {"category": ["Kalender.Quartal"], "ac": [M + "Kosten"], "ref": [M + "Budget"]},
             sub="in T€", analysis={"unit": "T€", "displayUnits": "K", "polarity": "lower", "deltaBasis": "PL", "deltaKind": ["abs", "rel"],
                                   "timeGrain": "quarter", "message": "Q2 sprengt das Budget – Vertriebsoffensive mit Premium-Seminaren"},
             notes="Budget liegt nur auf Quartalsebene vor – nie nach Monat zeigen.")],
    [3, leaf("bars", "ck", "Pflichtquote je Standort", {"category": ["dim_mitarbeitende.Standort"], "ac": [M + "Pflichtquote"], "ref": [M + "Ziel Pflichtquote"]},
             sub="in % vs. Ziel", analysis={"unit": "%", "sort": {"by": "value", "dir": "asc"}, "deltaBasis": "PL", "deltaKind": ["abs"],
                                         "message": "Werk Ulm hängt beim Datenschutz-E-Learning zurück"},
             notes="Drill-Idee: Standort → Bereich → Pflichtkurs. Ulm/Produktion hat kaum PC-Arbeitsplätze.")],
    [3, leaf("bars", "ck", "Ø Stunden je MA nach Bereich", {"category": ["dim_bereich.Bereich"], "ac": [M + "Ø Stunden je MA"], "ref": [M + "Ziel Ø Stunden je MA"]},
             sub="in h vs. Ziel", analysis={"unit": "h", "sort": {"by": "delta", "dir": "asc"}, "deltaBasis": "PL", "deltaKind": ["abs"]},
             notes="Ziel je Bereich unterschiedlich (IT 28 h, Logistik 12 h) – deshalb Abweichung statt Rangfolge.")],
])
ZEILE3 = row([
    [3, leaf("nline", "native", "Weiterbildungsstunden je Monat", {"category": ["Kalender.Monat"], "values": [M + "Stunden"]},
             sub="abgeschlossene Kurse", analysis={"timeGrain": "month"}, priority="should",
             notes="Saisonmuster: Sommerloch und Dezember. Hilft bei der Kursplanung 2026.")],
    [3, leaf("nbar", "native", "Vollzeit vs. Teilzeit", {"category": ["dim_mitarbeitende.Beschaeftigung"], "values": [M + "Teilnahmequote", M + "Ø Stunden je MA"]},
             sub="Teilnahmequote · Ø Stunden", priority="should",
             analysis={"message": "Teilzeitkräfte kommen nur halb so oft zum Zug"},
             notes="Fairness-Frage für GF und Betriebsrat: Kurszeiten passen nicht zu Teilzeitmodellen?")],
    [3, leaf("matrix", "native", "Top-Kurse nach Kosten", {"rows": ["dim_kurs.Kurstitel"], "values": [M + "Teilnahmen", M + "Kosten", M + "Ø Zufriedenheit"]},
             sub="Teilnahmen · Kosten · Zufriedenheit", priority="could",
             analysis={"topN": 8, "sort": {"by": "value", "dir": "desc"}},
             notes="Kosten und Zufriedenheit nebeneinander: Welche teuren Kurse lohnen sich?")],
])
LAYOUT = column([[1, KPIS], [2, ZEILE2], [2, ZEILE3]])

FIELD_META = {
    M + "Teilnahmequote": {"alias": "Teilnahmequote", "confirmed": True, "owner": "Personalentwicklung", "source": "LMS + HR-Stamm",
                           "target": "75 %", "unit": "%", "note": "nur freiwillige Kurse; Nenner = Headcount"},
    M + "Pflichtquote": {"alias": "Pflichtschulungsquote", "confirmed": True, "owner": "Compliance / Arbeitssicherheit", "source": "LMS + HR-Stamm",
                         "target": "95 %", "unit": "%", "note": "alle drei Pflichtkurse abgeschlossen"},
    M + "Ø Stunden je MA": {"alias": "Weiterbildungsstunden pro Kopf", "confirmed": True, "owner": "Personalentwicklung", "source": "LMS",
                            "target": "je Bereich (12–28 h)", "unit": "h", "note": "Nenner Headcount, nicht Teilnehmende"},
    M + "Kosten": {"alias": "Weiterbildungskosten", "confirmed": False, "owner": "Controlling", "source": "LMS (Kosten je Buchung)",
                   "target": "≤ Budget", "unit": "€", "note": "offen: Reisekosten gehören (noch) nicht dazu"},
    M + "Ø Zufriedenheit": {"alias": "Kurszufriedenheit", "confirmed": True, "owner": "Personalentwicklung", "source": "LMS-Feedback",
                            "target": "4,0", "unit": "1–5", "note": "freiwillige Angabe, ca. 70 % Rücklauf"},
}

STATE = {
    "version": 2, "name": "Weiterbildungs-Monitoring 2025",
    "canvas": {"w": 1280, "h": 720, "preset": "1280x720"},
    "spacing": {"margin": 16, "gutter": 12, "pad": 8},
    "defScenario": "AC/PL",
    "chrome": {
        "header": {"on": True, "h": 56, "logoPos": "left", "title": "Weiterbildungs-Monitoring 2025",
                   "sub": "Muster Maschinenbau GmbH · Personalentwicklung", "navAuto": True, "navOn": False, "nav": []},
        "nav": {"on": False, "w": 64},
        "filter": {"on": True, "side": "right", "w": 180, "topH": 56, "collapsible": False,
                   "fields": [F("dim_mitarbeitende.Standort"), F("dim_bereich.Bereich"),
                              F("dim_mitarbeitende.Beschaeftigung"), F("dim_kurs.Kategorie")]},
        "footer": {"on": True, "h": 24, "text": "Quelle: LMS-Export + HR-Stamm · Stand: Monatsende · fiktive Trainingsdaten"},
    },
    "design": {"radius": 8, "tile": "border", "pageBg": "light", "header": "dark", "accent": "#C25A2D", "palette": "teal",
               "pageBgHex": "#F4F4F1", "tileBg": "#FFFFFF", "ink": "#0F1E2E", "headerBg": "#0F1E2E", "headerInk": "#FFFFFF"},
    "report": {"audience": "Geschäftsführung, Personalentwicklung, Betriebsrat",
               "purpose": "Monatlicher Blick, ob die Weiterbildungsziele 2025 erreicht werden und das Budget hält.",
               "decision": "Wo steuern wir nach: Pflichtschulungen nachholen (Werk Ulm), Budget umschichten (Vertrieb), Kursangebot für Teilzeit öffnen?",
               "participants": "Personalentwicklung, Controlling, Betriebsrat (Datenschutz), Standortleitungen",
               "version": "0.1", "dataDate": "monatlich, LMS-Export zum Monatsersten"},
    "lang": "de",
    "fieldMeta": FIELD_META,
    "pages": [{"id": "wbpage01", "name": "Überblick",
               "question": "Erreichen wir unsere Weiterbildungsziele 2025 – und wo müssen wir nachsteuern?",
               "notes": "Eine Seite für die GF. Details (Person, Kurs) bewusst nicht hier – personenbezogene Daten nur mit RLS.",
               "layout": LAYOUT}],
    "cur": "wbpage01",
    "model": MODEL,
    "newFields": [],
}


def main():
    kitchen = Path(sys.argv[1] if len(sys.argv) > 1 else "../PowerBI-Kitchen-").resolve()
    if not (kitchen / "mockup-kitchen.html").exists():
        sys.exit(f"MockupKitchen nicht gefunden unter {kitchen} – Pfad zum Kitchen-Klon angeben.")
    OUT.mkdir(parents=True, exist_ok=True)

    class Leise(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(Leise, directory=str(kitchen))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}/mockup-kitchen.html"

    launch = {"executable_path": os.environ["PLAYWRIGHT_CHROMIUM"]} if os.environ.get("PLAYWRIGHT_CHROMIUM") else {}
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch)
        page = browser.new_page(viewport={"width": 1600, "height": 1000})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(url)
        page.wait_for_function("window.MK && window.MK_EXPORT && window.MK_PNG")
        result = page.evaluate("""async (state) => {
            MK.setLang('de');
            MK.state = state;
            const spec = MK_EXPORT.buildSpec();
            const pngs = await MK_PNG.allPagesPng({ scale: 2 });
            const png = [];
            for (const x of pngs) {
              const buf = new Uint8Array(await x.blob.arrayBuffer());
              let s = ''; for (let i = 0; i < buf.length; i += 0x8000) s += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000));
              png.push({ name: x.fileName, b64: btoa(s) });
            }
            return {
              saved: JSON.stringify(MK.state, null, 2),
              spec: JSON.stringify(spec, null, 2),
              brief: MK_EXPORT.buildBrief(spec),
              docs: MK_EXPORT.buildDocs(spec),
              pbir: spec.pages.map(pg => [MK_EXPORT.pbirName(pg), JSON.stringify(MK_EXPORT.buildPbir(spec, pg.id), null, 2)]),
              png,
              issues: spec.issues,
            };
        }""", STATE)
        browser.close()
    srv.shutdown()
    if errors:
        sys.exit("Fehler in der MockupKitchen: " + " | ".join(errors))

    (OUT / "weiterbildungs-monitoring.mockup.json").write_text(result["saved"] + "\n", encoding="utf-8")
    (OUT / "mockup-spec.json").write_text(result["spec"] + "\n", encoding="utf-8")
    (OUT / "AGENT-BRIEF.md").write_text(result["brief"], encoding="utf-8")
    (OUT / "WORKSHOP-DOKU.md").write_text(result["docs"], encoding="utf-8")
    for name, body in result["pbir"]:
        (OUT / name).write_text(body + "\n", encoding="utf-8")
    for x in result["png"]:
        (OUT / x["name"]).write_bytes(base64.b64decode(x["b64"]))
    print("✓ Mockup exportiert nach", OUT)
    for i in result["issues"] or []:
        print(f"  [{i['level']}] {i['code']}: {i['text']}")


if __name__ == "__main__":
    main()
