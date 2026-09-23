#!/usr/bin/env python3
"""Erzeugt das Power-BI-Projekt (PBIP) „Weiterbildungs-Monitoring" als Lösung zum Fall
cases/weiterbildungs-monitoring/.

Ablauf (siehe tools/pbip/README.md):
  1. Modell als TMDL-Rohfassung schreiben (dieses Skript)
  2. mit TmdlCheck (Microsoft TOM) einlesen, prüfen und kanonisch neu schreiben
  3. Bericht als PBIR schreiben (dieses Skript) – Layout exakt aus dem MockupKitchen-Export
  4. validate_pbir.py: alle JSON-Dateien gegen die offiziellen Microsoft-Schemas + alle Feldbezüge gegen das Modell

Aufruf aus dem Repo-Root:
  python3 tools/pbip/build_weiterbildung_pbip.py          # schreibt pbip/Weiterbildungs-Monitoring/
"""
import json
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
NAME = "Weiterbildungs-Monitoring"
OUT = ROOT / "pbip" / NAME
SM = OUT / f"{NAME}.SemanticModel"
RP = OUT / f"{NAME}.Report"
SPEC = json.loads((ROOT / "cases/weiterbildungs-monitoring/mockup/mockup-spec.json").read_text(encoding="utf-8"))
DATEN_URL = ("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/"
             "cases/weiterbildungs-monitoring/daten/")
NS = uuid.UUID("5a3c1f2e-9d4b-4e8a-b7c6-2f1e0d9c8b7a")        # feste IDs → reproduzierbare Dateien


def sid(*parts):
    return str(uuid.uuid5(NS, "/".join(parts)))


def tab(text, n):
    return "\n".join(("\t" * n + line) if line.strip() else "" for line in text.strip("\n").splitlines())


# =====================================================================================
# 1 · Semantikmodell (TMDL)
# =====================================================================================
def W(rel):
    return f'Web.Contents(DatenQuelle, [RelativePath = "{rel}"])'


M_FAKT = f"""
let
    // LMS-Export: Windows-1252, Semikolon, deutsche Zahlen (Lösung zu Schritt 2)
    Quelle = Csv.Document({W("roh/weiterbildung_buchungen_2025.csv")}, [Delimiter = ";", Columns = 11, Encoding = 1252, QuoteStyle = QuoteStyle.None]),
    Ueberschriften = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true]),
    OhneSummenzeile = Table.RemoveLastN(Ueberschriften, 1),
    OhneDuplikate = Table.Distinct(OhneSummenzeile),
    OhneKurstitel = Table.RemoveColumns(OhneDuplikate, {{"Kurstitel"}}),
    Personalnr = Table.TransformColumns(OhneKurstitel, {{{{"Personalnr", each Text.PadStart(Text.Trim(_), 5, "0"), type text}}}}),
    StatusBereinigt = Table.TransformColumns(Personalnr, {{{{"Status", each Text.Lower(Text.Trim(_)), type text}}}}),
    StatusSynonyme = Table.TransformColumns(StatusBereinigt, {{{{"Status", each if _ = "teilgenommen" then "abgeschlossen" else if List.Contains({{"no-show", "no show", "nicht erschienen"}}, _) then "No-Show" else _, type text}}}}),
    OhneEuro = Table.ReplaceValue(StatusSynonyme, " €", "", Replacer.ReplaceText, {{"Kosten"}}),
    FeedbackLeer = Table.ReplaceValue(OhneEuro, "", null, Replacer.ReplaceValue, {{"Feedback"}}),
    Typen = Table.TransformColumnTypes(FeedbackLeer, {{{{"BuchungsID", Int64.Type}}, {{"Kursnr", type text}}, {{"Buchungsdatum", type date}}, {{"Kursbeginn", type date}}, {{"Kursende", type date}}, {{"Stunden", type number}}, {{"Kosten", Currency.Type}}, {{"Feedback", Int64.Type}}}}, "de-DE")
in
    Typen
"""


def m_csv(rel, types, culture=None):
    t = ", ".join(f'{{"{c}", {ty}}}' for c, ty in types)
    cul = f', "{culture}"' if culture else ""
    return f"""
let
    Quelle = Csv.Document({W(rel)}, [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Ueberschriften = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true]),
    Typen = Table.TransformColumnTypes(Ueberschriften, {{{t}}}{cul})
in
    Typen
"""


M_BUDGET = f"""
let
    Quelle = Excel.Workbook({W("ziele/ziele_2025.xlsx")}, null, true),
    Blatt = Quelle{{[Item = "Budget 2025", Kind = "Sheet"]}}[Data],
    OhneTitel = Table.Skip(Blatt, 2),
    Ueberschriften = Table.PromoteHeaders(OhneTitel, [PromoteAllScalars = true]),
    OhneGesamtzeile = Table.SelectRows(Ueberschriften, each [Bereich] <> "Gesamt"),
    OhneSummenspalte = Table.RemoveColumns(OhneGesamtzeile, {{"Summe"}}),
    Entpivotiert = Table.UnpivotOtherColumns(OhneSummenspalte, {{"Bereich"}}, "Quartal", "Budget"),
    Quartalsanfang = Table.AddColumn(Entpivotiert, "Quartalsanfang", each #date(2025, (Number.From(Text.End([Quartal], 1)) - 1) * 3 + 1, 1), type date),
    Typen = Table.TransformColumnTypes(Quartalsanfang, {{{{"Bereich", type text}}, {{"Quartal", type text}}, {{"Budget", Currency.Type}}}})
in
    Typen
"""

M_ZIELE = f"""
let
    Quelle = Excel.Workbook({W("ziele/ziele_2025.xlsx")}, null, true),
    Blatt = Quelle{{[Item = "Zielwerte 2025", Kind = "Sheet"]}}[Data],
    OhneTitel = Table.Skip(Blatt, 2),
    Ueberschriften = Table.PromoteHeaders(OhneTitel, [PromoteAllScalars = true]),
    Entpivotiert = Table.UnpivotOtherColumns(Ueberschriften, {{"Bereich"}}, "Kennzahl", "Zielwert"),
    Typen = Table.TransformColumnTypes(Entpivotiert, {{{{"Bereich", type text}}, {{"Kennzahl", type text}}, {{"Zielwert", type number}}}})
in
    Typen
"""

M_KALENDER = """
let
    Start = #date(2025, 1, 1),
    Ende = #date(2025, 12, 31),
    Liste = List.Dates(Start, Duration.Days(Ende - Start) + 1, #duration(1, 0, 0, 0)),
    Tabelle = Table.FromList(Liste, Splitter.SplitByNothing(), {"Datum"}),
    Datum = Table.TransformColumnTypes(Tabelle, {{"Datum", type date}}),
    Jahr = Table.AddColumn(Datum, "Jahr", each Date.Year([Datum]), Int64.Type),
    Quartal = Table.AddColumn(Jahr, "Quartal", each "Q" & Text.From(Date.QuarterOfYear([Datum])), type text),
    MonatNr = Table.AddColumn(Quartal, "MonatNr", each Date.Month([Datum]), Int64.Type),
    Monat = Table.AddColumn(MonatNr, "Monat", each Date.ToText([Datum], [Format = "MMM", Culture = "de-DE"]), type text),
    Monatsanfang = Table.AddColumn(Monat, "Monatsanfang", each Date.StartOfMonth([Datum]), type date)
in
    Monatsanfang
"""

M_MEASURES = """
let
    // leere Hilfstabelle, die nur die Measures trägt
    Quelle = #table(type table [Measures = text], {})
in
    Quelle
"""

# Spalten: (Name, dataType, formatString|None, hidden, sortBy|None, isKey)
TABLES = [
    ("fakt_buchungen", "Eine Zeile je Kursbuchung aus dem LMS (bereinigt)", M_FAKT, [
        ("BuchungsID", "int64", "0", True, None, False),
        ("Personalnr", "string", None, True, None, False),
        ("Kursnr", "string", None, True, None, False),
        ("Buchungsdatum", "dateTime", "dd.MM.yyyy", False, None, False),
        ("Kursbeginn", "dateTime", "dd.MM.yyyy", True, None, False),
        ("Kursende", "dateTime", "dd.MM.yyyy", False, None, False),
        ("Status", "string", None, False, None, False),
        ("Stunden", "double", "#,0.0", True, None, False),
        ("Kosten", "decimal", "#,0.00 €", True, None, False),
        ("Feedback", "int64", "0", True, None, False)]),
    ("dim_mitarbeitende", "HR-Stamm, eine Zeile je Person (pseudonymisiert)", m_csv(
        "anreicherung/dim_mitarbeitende.csv",
        [("Personalnr", "type text"), ("BereichID", "type text"), ("Standort", "type text"), ("Rolle", "type text"),
         ("Beschaeftigung", "type text"), ("FTE", "type number"), ("Altersgruppe", "type text"), ("Eintritt", "type date")],
        "en-US"), [
        ("Personalnr", "string", None, False, None, False),
        ("BereichID", "string", None, True, None, False),
        ("Standort", "string", None, False, None, False),
        ("Rolle", "string", None, False, None, False),
        ("Beschaeftigung", "string", None, False, None, False),
        ("FTE", "double", "0.00", True, None, False),
        ("Altersgruppe", "string", None, False, None, False),
        ("Eintritt", "dateTime", "dd.MM.yyyy", False, None, False)]),
    ("dim_bereich", "Organisationsbereiche", m_csv(
        "anreicherung/dim_bereich.csv",
        [("BereichID", "type text"), ("Bereich", "type text"), ("Ressort", "type text"), ("Kostenstelle", "type text")]), [
        ("BereichID", "string", None, True, None, False),
        ("Bereich", "string", None, False, None, False),
        ("Ressort", "string", None, False, None, False),
        ("Kostenstelle", "string", None, False, None, False)]),
    ("dim_kurs", "Kurskatalog", m_csv(
        "anreicherung/dim_kurs.csv",
        [("Kursnr", "type text"), ("Kurstitel", "type text"), ("Kategorie", "type text"), ("Format", "type text"),
         ("Anbieter", "type text"), ("Pflicht", "type text"), ("Dauer_h", "type number"), ("Listenpreis", "Currency.Type")],
        "en-US"), [
        ("Kursnr", "string", None, False, None, False),
        ("Kurstitel", "string", None, False, None, False),
        ("Kategorie", "string", None, False, None, False),
        ("Format", "string", None, False, None, False),
        ("Anbieter", "string", None, False, None, False),
        ("Pflicht", "string", None, False, None, False),
        ("Dauer_h", "double", "#,0.0", False, None, False),
        ("Listenpreis", "decimal", "#,0.00 €", False, None, False)]),
    ("Kalender", "Kalender 2025 (als Datumstabelle markiert)", M_KALENDER, [
        ("Datum", "dateTime", "dd.MM.yyyy", False, None, True),
        ("Jahr", "int64", "0", False, None, False),
        ("Quartal", "string", None, False, None, False),
        ("MonatNr", "int64", "0", True, None, False),
        ("Monat", "string", None, False, "MonatNr", False),
        ("Monatsanfang", "dateTime", "dd.MM.yyyy", True, None, False)]),
    ("Budget", "Weiterbildungsbudget je Bereich und Quartal (entpivotiert)", M_BUDGET, [
        ("Bereich", "string", None, True, None, False),
        ("Quartal", "string", None, True, None, False),
        ("Budget", "decimal", "#,0 €", True, None, False),
        ("Quartalsanfang", "dateTime", "dd.MM.yyyy", True, None, False)]),
    ("Zielwerte", "Zielwerte je Bereich und Kennzahl (entpivotiert)", M_ZIELE, [
        ("Bereich", "string", None, True, None, False),
        ("Kennzahl", "string", None, False, None, False),
        ("Zielwert", "double", "#,0.00", True, None, False)]),
    ("_Measures", "Alle Kennzahlen", M_MEASURES, [
        ("Measures", "string", None, True, None, False)]),
]


def ziel(kennzahl):
    return f"""VAR Summe =
    SUMX (
        VALUES ( dim_bereich[Bereich] ),
        CALCULATE ( SUM ( Zielwerte[Zielwert] ), Zielwerte[Kennzahl] = "{kennzahl}" ) * [Headcount]
    )
RETURN
    DIVIDE ( Summe, [Headcount] )"""


# (Name, Ausdruck, Format, Ordner, Beschreibung)
MEASURES = [
    ("Headcount", "COUNTROWS ( dim_mitarbeitende )", "#,0", "1 Grundgrößen", "Personen im HR-Stamm"),
    ("FTE", "SUM ( dim_mitarbeitende[FTE] )", "#,0.0", "1 Grundgrößen", "Vollzeitäquivalente"),
    ("Buchungen", "COUNTROWS ( fakt_buchungen )", "#,0", "1 Grundgrößen", "alle Buchungen, jeder Status"),
    ("Teilnahmen", 'CALCULATE ( [Buchungen], fakt_buchungen[Status] = "abgeschlossen" )', "#,0", "1 Grundgrößen", "abgeschlossene Buchungen"),
    ("Stunden", 'CALCULATE ( SUM ( fakt_buchungen[Stunden] ), fakt_buchungen[Status] = "abgeschlossen" )', "#,0", "1 Grundgrößen", "Weiterbildungsstunden"),
    ("Kosten", "SUM ( fakt_buchungen[Kosten] )", "#,0 €", "1 Grundgrößen", "inkl. No-Show und Stornogebühren"),
    ("Ø Stunden je MA", "DIVIDE ( [Stunden], [Headcount] )", "#,0.0", "2 Quoten", "Nenner: alle Personen im HR-Stamm"),
    ("Kosten je MA", "DIVIDE ( [Kosten], [Headcount] )", "#,0 €", "2 Quoten", ""),
    ("Stornoquote", 'DIVIDE ( CALCULATE ( [Buchungen], fakt_buchungen[Status] = "storniert" ), [Buchungen] )', "0.0 %", "2 Quoten", ""),
    ("No-Show-Quote", 'DIVIDE ( CALCULATE ( [Buchungen], fakt_buchungen[Status] = "No-Show" ), [Buchungen] )', "0.0 %", "2 Quoten", ""),
    ("Teilnehmende freiwillig", """CALCULATE (
    DISTINCTCOUNT ( fakt_buchungen[Personalnr] ),
    fakt_buchungen[Status] = "abgeschlossen",
    dim_kurs[Pflicht] = "Nein"
)""", "#,0", "2 Quoten", "Personen mit ≥ 1 abgeschlossener freiwilliger Weiterbildung"),
    ("Teilnahmequote", "DIVIDE ( [Teilnehmende freiwillig], [Headcount] )", "0.0 %", "2 Quoten", ""),
    ("Pflicht erfüllt", """VAR AnzahlPflichtkurse =
    CALCULATE ( COUNTROWS ( dim_kurs ), REMOVEFILTERS ( dim_kurs ), dim_kurs[Pflicht] = "Ja" )
RETURN
    COUNTROWS (
        FILTER (
            dim_mitarbeitende,
            CALCULATE (
                DISTINCTCOUNT ( fakt_buchungen[Kursnr] ),
                fakt_buchungen[Status] = "abgeschlossen",
                REMOVEFILTERS ( dim_kurs ),         // Kursfilter (z. B. Kategorie) gelten hier nicht
                dim_kurs[Pflicht] = "Ja"
            ) = AnzahlPflichtkurse
        )
    )""", "#,0", "2 Quoten", "Personen, die alle Pflichtkurse abgeschlossen haben"),
    ("Pflichtquote", "DIVIDE ( [Pflicht erfüllt], [Headcount] )", "0.0 %", "2 Quoten", ""),
    ("Ø Zufriedenheit", "AVERAGE ( fakt_buchungen[Feedback] )", "0.00", "2 Quoten", "Mittelwert der Bewertungen 1–5"),
    ("Budget", "SUM ( Budget[Budget] )", "#,0 €", "3 Ziele & Budget", ""),
    ("Δ Budget", "[Kosten] - [Budget]", "+#,0 €;-#,0 €;0 €", "3 Ziele & Budget", "Kosten − Budget"),
    ("Budget-Ausschöpfung", "DIVIDE ( [Kosten], [Budget] )", "0.0 %", "3 Ziele & Budget", ""),
    ("Ziel Ø Stunden je MA", ziel("Ø Stunden je MA"), "#,0.0", "3 Ziele & Budget", "nach Headcount gewichtet"),
    ("Ziel Teilnahmequote", ziel("Teilnahmequote"), "0.0 %", "3 Ziele & Budget", "nach Headcount gewichtet"),
    ("Ziel Pflichtquote", ziel("Pflichtquote"), "0.0 %", "3 Ziele & Budget", "nach Headcount gewichtet"),
    ("Ziel Zufriedenheit", 'CALCULATE ( AVERAGE ( Zielwerte[Zielwert] ), Zielwerte[Kennzahl] = "Zufriedenheit" )', "0.0", "3 Ziele & Budget", ""),
    ("Δ Pflichtquote", "[Pflichtquote] - [Ziel Pflichtquote]", "+0.0 %;-0.0 %;0.0 %", "3 Ziele & Budget", ""),
    ("Δ Teilnahmequote", "[Teilnahmequote] - [Ziel Teilnahmequote]", "+0.0 %;-0.0 %;0.0 %", "3 Ziele & Budget", ""),
    # Beschriftungen für die KPI-Karten (dynamische Untertitel)
    ("Text Teilnahmequote", '"Ziel " & FORMAT ( [Ziel Teilnahmequote], "0.0 %" ) & "  ·  Δ " & FORMAT ( [Δ Teilnahmequote] * 100, "+0.0;-0.0" ) & " Pp"', None, "9 Beschriftungen", ""),
    ("Text Stunden", '"Ziel " & FORMAT ( [Ziel Ø Stunden je MA], "0.0" ) & " h  ·  Δ " & FORMAT ( [Ø Stunden je MA] - [Ziel Ø Stunden je MA], "+0.0;-0.0" ) & " h"', None, "9 Beschriftungen", ""),
    ("Text Pflichtquote", '"Ziel " & FORMAT ( [Ziel Pflichtquote], "0.0 %" ) & "  ·  Δ " & FORMAT ( [Δ Pflichtquote] * 100, "+0.0;-0.0" ) & " Pp"', None, "9 Beschriftungen", ""),
    ("Text Kosten", '"Budget " & FORMAT ( [Budget], "#,0 €" ) & "  ·  " & FORMAT ( [Budget-Ausschöpfung], "0.0 %" ) & " ausgeschöpft"', None, "9 Beschriftungen", ""),
    ("Text Zufriedenheit", '"Ziel " & FORMAT ( [Ziel Zufriedenheit], "0.0" ) & "  ·  " & FORMAT ( COUNT ( fakt_buchungen[Feedback] ), "#,0" ) & " Bewertungen"', None, "9 Beschriftungen", ""),
]

RELATIONSHIPS = [
    ("fakt_buchungen", "Personalnr", "dim_mitarbeitende", "Personalnr"),
    ("fakt_buchungen", "Kursnr", "dim_kurs", "Kursnr"),
    ("fakt_buchungen", "Kursbeginn", "Kalender", "Datum"),
    ("dim_mitarbeitende", "BereichID", "dim_bereich", "BereichID"),
    ("Budget", "Bereich", "dim_bereich", "Bereich"),
    ("Budget", "Quartalsanfang", "Kalender", "Datum"),
    ("Zielwerte", "Bereich", "dim_bereich", "Bereich"),
]


def q(name):
    """TMDL-Namen quoten, wenn nötig."""
    return name if name.replace("_", "").isalnum() and name.isascii() else "'" + name.replace("'", "''") + "'"


def write_model(raw):
    (raw / "tables").mkdir(parents=True, exist_ok=True)
    (raw / "database.tmdl").write_text("database\n\tcompatibilityLevel: 1567\n", encoding="utf-8")
    refs = "\n".join(f"ref table {q(t[0])}" for t in TABLES)
    (raw / "model.tmdl").write_text(f"""model Model
	culture: de-DE
	defaultPowerBIDataSourceVersion: powerBI_V3
	sourceQueryCulture: de-DE
	discourageImplicitMeasures

	annotation __PBI_TimeIntelligenceEnabled = 0

{refs}
""", encoding="utf-8")
    (raw / "expressions.tmdl").write_text(
        f'expression DatenQuelle = "{DATEN_URL}" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]\n'
        "\tannotation PBI_ResultType = Text\n", encoding="utf-8")
    for name, desc, m, cols in TABLES:
        out = [f"/// {desc}", f"table {q(name)}"]
        if name == "Kalender":
            out.append("\tdataCategory: Time")
        out.append("")
        if name == "_Measures":
            for mn, expr, fmt, folder, mdesc in MEASURES:
                if mdesc:
                    out.append(f"\t/// {mdesc}")
                if "\n" in expr:
                    out.append(f"\tmeasure {q(mn)} =")
                    out.append(tab(expr, 3))
                else:
                    out.append(f"\tmeasure {q(mn)} = {expr}")
                if fmt:
                    out.append(f"\t\tformatString: {fmt}")
                out.append(f"\t\tdisplayFolder: {folder}")
                out.append("")
        for cn, dt, fmt, hidden, sort_by, is_key in cols:
            out.append(f"\tcolumn {q(cn)}")
            out.append(f"\t\tdataType: {dt}")
            if fmt:
                out.append(f"\t\tformatString: {fmt}")
            if hidden:
                out.append("\t\tisHidden")
            if is_key:
                out.append("\t\tisKey")
            out.append("\t\tsummarizeBy: none")
            out.append(f"\t\tsourceColumn: {cn}")
            if sort_by:
                out.append(f"\t\tsortByColumn: {sort_by}")
            out.append("")
        out.append(f"\tpartition {q(name)} = m")
        out.append("\t\tmode: import")
        out.append("\t\tsource =")
        out.append(tab(m, 4))
        out.append("")
        (raw / "tables" / f"{name}.tmdl").write_text("\n".join(out) + "\n", encoding="utf-8")
    rel = []
    for ft, fc, tt, tc in RELATIONSHIPS:
        rel.append(f"relationship {sid('rel', ft, fc, tt, tc)}\n\tfromColumn: {q(ft)}.{q(fc)}\n\ttoColumn: {q(tt)}.{q(tc)}\n")
    (raw / "relationships.tmdl").write_text("\n".join(rel), encoding="utf-8")


# =====================================================================================
# 2 · Bericht (PBIR)
# =====================================================================================
SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/"
MEASURE_TABLE = "_Measures"
INK, ACCENT, TEAL, RED, GREY = "#0F1E2E", "#C25A2D", "#1E8F9E", "#D64541", "#6B7280"


def L(v):
    return {"expr": {"Literal": {"Value": v}}}


def s(text):
    return L("'" + text.replace("'", "''") + "'")


def color(hexv):
    return {"solid": {"color": s(hexv)}}


def fld(ref):
    table, prop = ref.split(".", 1)
    kind = "Measure" if table == MEASURE_TABLE else "Column"
    return {kind: {"Expression": {"SourceRef": {"Entity": table}}, "Property": prop}}


def proj(ref, active=False):
    table, prop = ref.split(".", 1)
    p = {"field": fld(ref), "queryRef": ref, "nativeQueryRef": prop}
    if active:
        p["active"] = True
    return p


def query(roles, sort=None):
    qs = {}
    for role, refs in roles.items():
        qs[role] = {"projections": [proj(r, active=(i == 0 and not r.startswith(MEASURE_TABLE)))
                                    for i, r in enumerate(refs)]}
    out = {"queryState": qs}
    if sort:
        out["sortDefinition"] = {"sort": [{"field": fld(r), "direction": d} for r, d in sort], "isDefaultSort": False}
    return out


def container(title, subtitle=None, subtitle_measure=None, border=True, background="#FFFFFF"):
    vco = {
        "title": [{"properties": {"show": L("true"), "text": s(title), "fontColor": color(INK), "fontSize": L("12D"),
                                  "bold": L("true")}}],
        "background": [{"properties": {"show": L("true"), "color": color(background), "transparency": L("0D")}}],
        "border": [{"properties": {"show": L("true" if border else "false"), "color": color("#E5E7EB"), "radius": L("8D")}}],
        "dropShadow": [{"properties": {"show": L("false")}}],
    }
    if subtitle or subtitle_measure:
        text = {"expr": fld(f"{MEASURE_TABLE}.{subtitle_measure}")} if subtitle_measure else s(subtitle)
        vco["subTitle"] = [{"properties": {"show": L("true"), "text": text, "fontColor": color(GREY), "fontSize": L("9D")}}]
    return vco


def visual(name, rect, z, vtype, q=None, objects=None, vco=None, tab_order=None):
    v = {"visualType": vtype}
    if q:
        v["query"] = q
    if objects:
        v["objects"] = objects
    if vco:
        v["visualContainerObjects"] = vco
    v["drillFilterOtherVisuals"] = True
    return {
        "$schema": SCHEMA + "item/report/definition/visualContainer/2.9.0/schema.json",
        "name": name,
        "position": {"x": rect["x"], "y": rect["y"], "z": z, "height": rect["h"], "width": rect["w"],
                     "tabOrder": z if tab_order is None else tab_order},
        "visual": v,
    }


def textbox(name, rect, z, paragraphs, background=None):
    runs = [{"textRuns": [{"value": txt, "textStyle": {"fontFamily": fam, "fontSize": size, "color": col}}]}
            for txt, fam, size, col in paragraphs]
    vco = {"title": [{"properties": {"show": L("false")}}],
           "border": [{"properties": {"show": L("false")}}],
           "background": [{"properties": {"show": L("true" if background else "false")} |
                           ({"color": color(background), "transparency": L("0D")} if background else {})}]}
    return visual(name, rect, z, "textbox", objects={"general": [{"properties": {"paragraphs": runs}}]}, vco=vco)


SEGOE = "'Segoe UI', wf_segoe-ui_normal, helvetica, arial, sans-serif"
SEGOE_SB = "'Segoe UI Semibold', wf_segoe-ui_semibold, helvetica, arial, sans-serif"
M_ = MEASURE_TABLE + "."


def build_visuals():
    rects = {v["id"]: v["rect"] for v in SPEC["pages"][0]["visuals"]}
    z = SPEC["zones"]
    vs = []
    # Kopfband und Fußleiste
    h = z["header"]
    vs.append(textbox("kopfband", {"x": h["x"], "y": h["y"], "w": h["w"], "h": h["h"]}, 0, [
        ("Weiterbildungs-Monitoring 2025", SEGOE_SB, "18pt", "#FFFFFF"),
        ("Muster Maschinenbau GmbH · Personalentwicklung · fiktive Trainingsdaten", SEGOE, "10pt", "#C9D2DA")],
        background=INK))
    f = z["footer"]
    vs.append(textbox("fussleiste", {"x": f["x"] + 16, "y": f["y"], "w": f["w"] - 32, "h": f["h"]}, 1, [
        ("Quelle: LMS-Export + HR-Stamm · Stand: Monatsende · Kennzahl-Definitionen: skripte/dax/measures.dax",
         SEGOE, "8pt", GREY)]))

    # KPI-Karten
    kpis = [("mk_wbt01", "Teilnahmequote", "Text Teilnahmequote"),
            ("mk_wbt02", "Ø Stunden je MA", "Text Stunden"),
            ("mk_wbt03", "Pflichtquote", "Text Pflichtquote"),
            ("mk_wbt04", "Kosten", "Text Kosten"),
            ("mk_wbt05", "Ø Zufriedenheit", "Text Zufriedenheit")]
    for i, (vid, meas, text) in enumerate(kpis):
        objects = {"labels": [{"properties": {"fontSize": L("24D"), "color": color(INK)}}],
                   "categoryLabels": [{"properties": {"show": L("false")}}]}
        vs.append(visual(vid, rects[vid], 10 + i, "card", query({"Values": [M_ + meas]}), objects,
                         container(meas, subtitle_measure=text)))

    def bars(vid, vtype, title, sub, cat, ys, sort, tooltips=None, z_=20):
        roles = {"Category": [cat], "Y": ys}
        if tooltips:
            roles["Tooltips"] = tooltips
        objects = {"labels": [{"properties": {"show": L("true"), "fontSize": L("8D")}}],
                   "legend": [{"properties": {"show": L("true" if len(ys) > 1 else "false"), "position": s("Top")}}],
                   "valueAxis": [{"properties": {"show": L("false")}}]}
        return visual(vid, rects[vid], z_, vtype, query(roles, sort), objects, container(title, subtitle=sub))

    vs.append(bars("mk_wbt07", "clusteredColumnChart", "Kosten vs. Budget je Quartal",
                   "Q2 sprengt das Budget – Vertriebsoffensive", "Kalender.Quartal",
                   [M_ + "Kosten", M_ + "Budget"], [("Kalender.Quartal", "Ascending")], z_=20))
    vs.append(bars("mk_wbt08", "clusteredBarChart", "Pflichtquote je Standort", "Ist vs. Ziel (95 %)",
                   "dim_mitarbeitende.Standort", [M_ + "Pflichtquote", M_ + "Ziel Pflichtquote"],
                   [(M_ + "Pflichtquote", "Ascending")], z_=21))
    vs.append(bars("mk_wbt09", "clusteredBarChart", "Ø Stunden je MA nach Bereich", "Ist vs. Ziel je Bereich",
                   "dim_bereich.Bereich", [M_ + "Ø Stunden je MA", M_ + "Ziel Ø Stunden je MA"],
                   [(M_ + "Ø Stunden je MA", "Descending")], z_=22))
    vs.append(visual("mk_wbt11", rects["mk_wbt11"], 23, "lineChart",
                     query({"Category": ["Kalender.Monat"], "Y": [M_ + "Stunden"]}, [("Kalender.Monat", "Ascending")]),
                     {"labels": [{"properties": {"show": L("true"), "fontSize": L("8D")}}],
                      "legend": [{"properties": {"show": L("false")}}]},
                     container("Weiterbildungsstunden je Monat", subtitle="abgeschlossene Kurse")))
    vs.append(bars("mk_wbt12", "clusteredBarChart", "Vollzeit vs. Teilzeit", "Teilnahmequote (Tooltip: Ø Stunden)",
                   "dim_mitarbeitende.Beschaeftigung", [M_ + "Teilnahmequote"],
                   [(M_ + "Teilnahmequote", "Descending")], tooltips=[M_ + "Ø Stunden je MA"], z_=24))
    vs.append(visual("mk_wbt13", rects["mk_wbt13"], 25, "tableEx",
                     query({"Values": ["dim_kurs.Kurstitel", M_ + "Teilnahmen", M_ + "Kosten", M_ + "Ø Zufriedenheit"]},
                           [(M_ + "Kosten", "Descending")]),
                     None, container("Kurse nach Kosten", subtitle="Teilnahmen · Kosten · Zufriedenheit")))

    # Filterbereich rechts
    fz = z["filter"]
    vs.append(textbox("filter_titel", {"x": fz["x"] + 8, "y": fz["y"] + 8, "w": fz["w"] - 16, "h": 28}, 30,
                      [("FILTER", SEGOE_SB, "10pt", GREY)]))
    for i, sl in enumerate(SPEC["zones"]["filter"]["slicers"]):
        rect = {"x": fz["x"] + 8, "y": fz["y"] + 40 + i * 64, "w": fz["w"] - 16, "h": 56}
        name = "slicer_" + sl["name"].lower()
        objects = {"data": [{"properties": {"mode": s("Dropdown")}}],
                   "header": [{"properties": {"show": L("true"), "fontColor": color(INK), "textSize": L("9D")}}]}
        vco = {"title": [{"properties": {"show": L("false")}}],
               "background": [{"properties": {"show": L("true"), "color": color("#FFFFFF"), "transparency": L("0D")}}],
               "border": [{"properties": {"show": L("true"), "color": color("#E5E7EB"), "radius": L("6D")}}]}
        vs.append(visual(name, rect, 31 + i, "slicer", query({"Values": [sl["ref"]]}), objects, vco))
    return vs


THEME = {
    "name": "Weiterbildung",
    "dataColors": ["#404040", "#A6B1B8", TEAL, RED, ACCENT, "#7A8C99", "#2F6B8A", "#C9A227"],
    "foreground": INK, "foregroundNeutralSecondary": GREY, "background": "#FFFFFF",
    "backgroundLight": "#F4F4F1", "tableAccent": TEAL, "good": TEAL, "bad": RED, "neutral": "#A6B1B8",
    "textClasses": {
        "title": {"fontFace": "Segoe UI Semibold", "fontSize": 12, "color": INK},
        "label": {"fontFace": "Segoe UI", "fontSize": 9, "color": INK},
        "callout": {"fontFace": "Segoe UI Semibold", "fontSize": 24, "color": INK},
    },
}


def write_report(base_theme):
    defn = RP / "definition"
    page_id = "ueberblick"
    vdir = defn / "pages" / page_id / "visuals"
    vdir.mkdir(parents=True, exist_ok=True)

    def dump(path, obj):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    dump(RP / "definition.pbir", {
        "$schema": SCHEMA + "item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {"byPath": {"path": f"../{NAME}.SemanticModel"}}})
    dump(RP / ".platform", {
        "$schema": SCHEMA + "gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "Report", "displayName": NAME},
        "config": {"version": "2.0", "logicalId": sid("report")}})
    dump(defn / "version.json", {"$schema": SCHEMA + "item/report/definition/versionMetadata/1.0.0/schema.json",
                                 "version": "2.0.0"})
    dump(defn / "report.json", {
        "$schema": SCHEMA + "item/report/definition/report/3.0.0/schema.json",
        "themeCollection": {
            "baseTheme": {"name": "CY24SU10", "reportVersionAtImport": {"visual": "1.8.95", "report": "2.0.95", "page": "1.3.95"},
                          "type": "SharedResources"},
            "customTheme": {"name": "Weiterbildung.json", "reportVersionAtImport": {"visual": "2.1.0", "report": "2.1.0", "page": "2.0.0"},
                            "type": "RegisteredResources"}},
        "resourcePackages": [
            {"name": "SharedResources", "type": "SharedResources",
             "items": [{"name": "CY24SU10", "path": "BaseThemes/CY24SU10.json", "type": "BaseTheme"}]},
            {"name": "RegisteredResources", "type": "RegisteredResources",
             "items": [{"name": "Weiterbildung.json", "path": "Weiterbildung.json", "type": "CustomTheme"}]}],
        "settings": {"useStylableVisualContainerHeader": True, "exportDataMode": "AllowSummarized",
                     "defaultDrillFilterOtherVisuals": True, "allowChangeFilterTypes": True,
                     "useEnhancedTooltips": True, "useDefaultAggregateDisplayName": True}})
    dump(defn / "pages" / "pages.json", {
        "$schema": SCHEMA + "item/report/definition/pagesMetadata/1.0.0/schema.json",
        "pageOrder": [page_id], "activePageName": page_id})
    dump(defn / "pages" / page_id / "page.json", {
        "$schema": SCHEMA + "item/report/definition/page/2.0.0/schema.json",
        "name": page_id, "displayName": "Überblick", "displayOption": "FitToPage",
        "height": SPEC["canvas"]["height"], "width": SPEC["canvas"]["width"],
        "objects": {"background": [{"properties": {"color": color("#F4F4F1"), "transparency": L("0D")}}]}})
    for v in build_visuals():
        dump(vdir / v["name"] / "visual.json", v)
    themes = RP / "StaticResources" / "SharedResources" / "BaseThemes"
    themes.mkdir(parents=True, exist_ok=True)
    shutil.copy(base_theme, themes / "CY24SU10.json")
    dump(RP / "StaticResources" / "RegisteredResources" / "Weiterbildung.json", THEME)


def main():
    base_theme = HERE / "resources" / "CY24SU10.json"
    # nur die erzeugten Teile ersetzen – README.md und pruefen.ps1 im Ordner bleiben stehen
    for d in (SM, RP):
        if d.exists():
            shutil.rmtree(d)
    OUT.mkdir(parents=True, exist_ok=True)
    raw = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/wb_tmdl_raw")
    if raw.exists():
        shutil.rmtree(raw)
    write_model(raw)

    # Modell mit TOM einlesen, prüfen und kanonisch in den PBIP-Ordner schreiben
    check = HERE / "TmdlCheck"
    r = subprocess.run(["dotnet", "run", "--project", str(check), "-c", "Release", "--",
                        str(raw), str(SM / "definition"), "--inventory", str(raw.parent / "wb_felder.json")],
                       capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr)
        sys.exit("Modellprüfung fehlgeschlagen")
    (SM / "definition.pbism").write_text(json.dumps({
        "$schema": SCHEMA + "item/semanticModel/definitionProperties/1.0.0/schema.json",
        "version": "4.2", "settings": {}}, indent=2) + "\n", encoding="utf-8")
    (SM / ".platform").write_text(json.dumps({
        "$schema": SCHEMA + "gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "SemanticModel", "displayName": NAME},
        "config": {"version": "2.0", "logicalId": sid("model")}}, indent=2) + "\n", encoding="utf-8")

    write_report(base_theme)
    (OUT / f"{NAME}.pbip").write_text(json.dumps({
        "$schema": SCHEMA + "pbip/pbipProperties/1.0.0/schema.json",
        "version": "1.0", "artifacts": [{"report": {"path": f"{NAME}.Report"}}],
        "settings": {"enableAutoRecovery": True}}, indent=2) + "\n", encoding="utf-8")
    (OUT / ".gitignore").write_text("**/.pbi/localSettings.json\n**/.pbi/cache.abf\n", encoding="utf-8")
    print("✓ PBIP geschrieben:", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
