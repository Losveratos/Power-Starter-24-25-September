#!/usr/bin/env python3
"""Erzeugt die Daten für den Fall „Weiterbildungs-Monitoring" (fiktive Muster Maschinenbau GmbH, 2025).

Ergebnis (relativ zum Fall-Ordner):
  daten/roh/weiterbildung_buchungen_2025.csv   LMS-Export, absichtlich unordentlich (Windows-1252, ;, deutsche Zahlen)
  daten/anreicherung/*.csv                      Dimensionen (UTF-8, sauber)
  daten/ziele/ziele_2025.xlsx + *.csv           Ziele als Kreuztabellen (Budget je Quartal, Zielwerte je Kennzahl)
  daten/kontrollzahlen.json                     alle Zahlen, die in der Anleitung vorkommen

Deterministisch (fester Seed). Aufruf aus dem Repo-Root:
  python3 cases/weiterbildungs-monitoring/tools/generate_data.py
Braucht openpyxl für die Excel-Datei.
"""
import csv
import datetime as dt
import json
import random
from collections import defaultdict
from pathlib import Path

CASE = Path(__file__).resolve().parent.parent
D_ROH = CASE / "daten" / "roh"
D_ANR = CASE / "daten" / "anreicherung"
D_ZIEL = CASE / "daten" / "ziele"
YEAR = 2025
rng = random.Random(2509)

# ---------------------------------------------------------------- Stammdaten
BEREICHE = [
    # id, name, ressort, kostenstelle, anzahl MA, Anteil je Standort (Zentrale, Kassel, Ulm)
    ("B01", "Produktion", "Technik", "4100", 150, (0.0, 0.45, 0.55)),
    ("B02", "Logistik", "Technik", "4300", 55, (0.0, 0.40, 0.60)),
    ("B03", "Entwicklung", "Technik", "5100", 60, (0.70, 0.30, 0.0)),
    ("B04", "Service", "Technik", "4500", 45, (0.30, 0.35, 0.35)),
    ("B05", "Vertrieb", "Kaufmännisch", "6100", 45, (0.80, 0.10, 0.10)),
    ("B06", "IT", "Kaufmännisch", "7100", 25, (1.0, 0.0, 0.0)),
    ("B07", "Verwaltung", "Kaufmännisch", "7300", 40, (0.85, 0.05, 0.10)),
]
STANDORTE = ["Zentrale Hannover", "Werk Kassel", "Werk Ulm"]

KURSE = [
    # nr, titel, kategorie, format, anbieter, pflicht, dauer_h, preis_je_tn (0 = intern)
    ("K-001", "Datenschutz-Grundlagen", "Pflicht & Compliance", "E-Learning", "intern", True, 1.0, 0),
    ("K-002", "Arbeitsschutz-Unterweisung", "Pflicht & Compliance", "Präsenz", "intern", True, 2.0, 0),
    ("K-003", "Verhaltenskodex & Compliance", "Pflicht & Compliance", "E-Learning", "intern", True, 1.0, 0),
    ("K-101", "Excel Aufbau", "IT & Digital", "Online", "extern", False, 8.0, 290),
    ("K-102", "Power BI Grundlagen", "IT & Digital", "Präsenz", "extern", False, 16.0, 890),
    ("K-103", "KI im Arbeitsalltag", "IT & Digital", "Online", "intern", False, 4.0, 0),
    ("K-104", "IT-Sicherheit für alle", "IT & Digital", "E-Learning", "intern", False, 2.0, 0),
    ("K-105", "Cloud-Architektur Zertifizierung", "IT & Digital", "Blended", "extern", False, 32.0, 2450),
    ("K-106", "SAP S/4 Anwendertraining", "IT & Digital", "Präsenz", "intern", False, 8.0, 0),
    ("K-201", "Führung Basis", "Führung", "Präsenz", "extern", False, 24.0, 1650),
    ("K-202", "Konfliktgespräche führen", "Führung", "Präsenz", "extern", False, 8.0, 690),
    ("K-203", "Feedback & Mitarbeitergespräch", "Führung", "Online", "intern", False, 4.0, 0),
    ("K-301", "Lean Production", "Fachlich", "Präsenz", "extern", False, 16.0, 980),
    ("K-302", "CNC-Programmierung", "Fachlich", "Präsenz", "extern", False, 24.0, 1390),
    ("K-303", "Schweißtechnik Auffrischung", "Fachlich", "Präsenz", "extern", False, 16.0, 740),
    ("K-304", "Qualitätsmanagement ISO 9001", "Fachlich", "Blended", "extern", False, 12.0, 820),
    ("K-305", "Projektmanagement Basis", "Fachlich", "Online", "extern", False, 16.0, 950),
    ("K-306", "Verhandlungstraining Vertrieb", "Fachlich", "Präsenz", "extern", False, 16.0, 1480),
    ("K-307", "Technischer Vertrieb Intensiv", "Fachlich", "Präsenz", "extern", False, 24.0, 2100),
    ("K-401", "Staplerschein", "Arbeitssicherheit", "Präsenz", "extern", False, 16.0, 420),
    ("K-402", "Erste Hilfe", "Arbeitssicherheit", "Präsenz", "extern", False, 9.0, 65),
    ("K-501", "Business English B1", "Sprachen", "Online", "extern", False, 20.0, 560),
    ("K-502", "Deutsch am Arbeitsplatz", "Sprachen", "Präsenz", "extern", False, 20.0, 380),
]
PFLICHT = [k[0] for k in KURSE if k[5]]

# Welche Bereiche welche Kurse typischerweise buchen (Gewicht)
AFFINITAET = {
    "Produktion": {"K-301": 4, "K-302": 3, "K-303": 3, "K-304": 2, "K-401": 2, "K-402": 3, "K-502": 2, "K-103": 1, "K-106": 1},
    "Logistik": {"K-401": 6, "K-402": 3, "K-106": 3, "K-301": 2, "K-502": 2, "K-101": 1},
    "Entwicklung": {"K-305": 3, "K-304": 2, "K-102": 2, "K-103": 3, "K-501": 3, "K-101": 1, "K-105": 1},
    "Service": {"K-402": 3, "K-304": 2, "K-501": 3, "K-106": 2, "K-103": 1, "K-202": 1},
    "Vertrieb": {"K-306": 5, "K-307": 4, "K-501": 3, "K-101": 2, "K-102": 1, "K-103": 2},
    "IT": {"K-105": 4, "K-102": 3, "K-104": 2, "K-103": 3, "K-305": 2},
    "Verwaltung": {"K-101": 5, "K-102": 3, "K-106": 3, "K-103": 2, "K-305": 1, "K-501": 1},
}
FUEHRUNG = {"K-201": 4, "K-202": 3, "K-203": 4}


def mitarbeitende():
    rows, n = [], 1
    for bid, bname, _, _, anzahl, verteilung in BEREICHE:
        for i in range(anzahl):
            standort = rng.choices(STANDORTE, verteilung)[0]
            fk = i % 12 == 0                                   # ca. jede zwölfte Person führt
            azubi = (not fk) and bname in ("Produktion", "Logistik", "Verwaltung") and rng.random() < 0.07
            rolle = "Führungskraft" if fk else ("Auszubildende" if azubi else "Mitarbeitende")
            teilzeit = (not azubi) and rng.random() < (0.28 if bname in ("Verwaltung", "Vertrieb", "Service") else 0.12)
            fte = rng.choice([0.5, 0.6, 0.75, 0.8]) if teilzeit else 1.0
            alter = "unter 30" if azubi else rng.choices(["unter 30", "30–44", "45–54", "55+"], [18, 38, 26, 18])[0]
            von = {"unter 30": 2016, "30–44": 2004, "45–54": 1996, "55+": 1990}[alter]
            eintritt = dt.date(rng.randint(von, 2024), rng.randint(1, 12), 1)
            if azubi:
                eintritt = dt.date(rng.choice([2023, 2024]), 9, 1)
            rows.append({"Personalnr": f"{n:05d}", "BereichID": bid, "Standort": standort, "Rolle": rolle,
                         "Beschaeftigung": "Teilzeit" if teilzeit else "Vollzeit", "FTE": f"{fte:.2f}",
                         "Altersgruppe": alter, "Eintritt": eintritt.isoformat()})
            n += 1
    return rows


FEIERTAGE = {"01-01", "04-18", "04-21", "05-01", "05-29", "06-09", "10-03", "12-24", "12-25", "12-26", "12-31"}


def zufallstag(von_monat=1, bis_monat=12):
    start = dt.date(YEAR, von_monat, 1)
    ende = dt.date(YEAR, bis_monat, 28)
    while True:
        d = start + dt.timedelta(days=rng.randint(0, (ende - start).days))
        if d.weekday() < 5 and d.strftime("%m-%d") not in FEIERTAGE:
            return d


def main():
    for d in (D_ROH, D_ANR, D_ZIEL):
        d.mkdir(parents=True, exist_ok=True)
    ma = mitarbeitende()
    bereich_of = {b[0]: b[1] for b in BEREICHE}
    kurs = {k[0]: k for k in KURSE}

    buchungen = []
    bid_counter = 250000

    def buche(p, knr, beginn, status=None):
        nonlocal bid_counter
        bid_counter += rng.randint(1, 3)
        k = kurs[knr]
        dauer_tage = max(1, int(round(k[6] / 8)))
        ende = beginn + dt.timedelta(days=dauer_tage - 1)
        buchdatum = beginn - dt.timedelta(days=rng.randint(7, 60))
        if status is None:
            status = rng.choices(["abgeschlossen", "storniert", "No-Show"], [84, 11, 5])[0]
        if beginn > dt.date(YEAR, 12, 15) and status == "abgeschlossen" and rng.random() < 0.5:
            status = "angemeldet"
        stunden = k[6] if status == "abgeschlossen" else 0.0
        if status == "abgeschlossen" and k[6] >= 8 and rng.random() < 0.08:
            stunden = k[6] - rng.choice([2.0, 4.0])             # früher gegangen
        preis = k[7] * rng.uniform(0.95, 1.05) if k[7] else 0.0
        if p["_vertrieb_premium"] and knr in ("K-306", "K-307"):
            preis *= 1.35                                         # Vertrieb bucht Premium-Anbieter
        kosten = {"abgeschlossen": preis, "angemeldet": 0.0, "No-Show": preis,
                  "storniert": preis * 0.5 if rng.random() < 0.3 else 0.0}[status]
        fb = ""
        if status == "abgeschlossen" and rng.random() < 0.72:
            basis = 4.3 if k[4] == "extern" else 3.9
            if k[3] == "E-Learning":
                basis = 3.5
            fb = str(min(5, max(1, round(rng.gauss(basis, 0.8)))))
        buchungen.append({"BuchungsID": bid_counter, "Personalnr": p["Personalnr"], "Kursnr": knr,
                          "Buchungsdatum": buchdatum, "Kursbeginn": beginn, "Kursende": ende,
                          "Status": status, "Stunden": stunden, "Kosten": round(kosten, 2), "Feedback": fb})

    for p in ma:
        bname = bereich_of[p["BereichID"]]
        p["_vertrieb_premium"] = bname == "Vertrieb"
        # Pflichtschulungen – die Geschichte: Werk Ulm hinkt beim Datenschutz hinterher (E-Learning ohne PC-Arbeitsplatz)
        for knr in PFLICHT:
            quote = 0.95
            if p["Standort"] == "Werk Ulm" and bname in ("Produktion", "Logistik") and knr == "K-001":
                quote = 0.55
            if p["Rolle"] == "Auszubildende":
                quote = 0.99
            if rng.random() < quote:
                buche(p, knr, zufallstag(1, 11), "abgeschlossen")
            elif rng.random() < 0.4:
                buche(p, knr, zufallstag(3, 12), rng.choice(["storniert", "No-Show"]))
        # freiwillige / fachliche Weiterbildung
        lam = 1.3
        if p["Rolle"] == "Führungskraft":
            lam = 2.4
        if p["Beschaeftigung"] == "Teilzeit":
            lam *= 0.45                                            # Teilzeit kommt seltener zum Zug
        if p["Altersgruppe"] == "55+":
            lam *= 0.7
        n_kurse = sum(1 for _ in range(6) if rng.random() < lam / 6)
        pool = dict(AFFINITAET[bname])
        if p["Rolle"] == "Führungskraft":
            pool.update(FUEHRUNG)
        pool["K-104"] = pool.get("K-104", 0) + 1
        for _ in range(n_kurse):
            knr = rng.choices(list(pool), list(pool.values()))[0]
            monat = rng.choices(range(1, 13), [5, 8, 10, 9, 9, 7, 3, 2, 10, 11, 9, 4])[0]
            if bname == "Vertrieb" and knr in ("K-306", "K-307"):
                monat = rng.choice([4, 5, 6, 6])                   # Vertriebsoffensive im Q2
            buche(p, knr, zufallstag(monat, monat))

    buchungen.sort(key=lambda b: (b["Buchungsdatum"], b["BuchungsID"]))

    # ---------------------------------------------------------------- Anreicherung (sauber, UTF-8)
    def write(path, rows, fields, **kw):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", **kw)
            w.writeheader()
            w.writerows(rows)

    write(D_ANR / "dim_mitarbeitende.csv", ma,
          ["Personalnr", "BereichID", "Standort", "Rolle", "Beschaeftigung", "FTE", "Altersgruppe", "Eintritt"])
    write(D_ANR / "dim_bereich.csv",
          [{"BereichID": b[0], "Bereich": b[1], "Ressort": b[2], "Kostenstelle": b[3]} for b in BEREICHE],
          ["BereichID", "Bereich", "Ressort", "Kostenstelle"])
    write(D_ANR / "dim_kurs.csv",
          [{"Kursnr": k[0], "Kurstitel": k[1], "Kategorie": k[2], "Format": k[3], "Anbieter": k[4],
            "Pflicht": "Ja" if k[5] else "Nein", "Dauer_h": f"{k[6]:.1f}", "Listenpreis": f"{k[7]:.2f}"} for k in KURSE],
          ["Kursnr", "Kurstitel", "Kategorie", "Format", "Anbieter", "Pflicht", "Dauer_h", "Listenpreis"])

    # ---------------------------------------------------------------- Rohdaten (unordentlich)
    STATUS_VARIANTEN = {
        "abgeschlossen": ["abgeschlossen"] * 12 + ["Abgeschlossen", "ABGESCHLOSSEN ", "teilgenommen"],
        "storniert": ["storniert"] * 5 + ["Storniert", "storniert "],
        "No-Show": ["No-Show"] * 4 + ["no show", "Nicht erschienen"],
        "angemeldet": ["angemeldet"],
    }
    de_num = lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    de_date = lambda d: d.strftime("%d.%m.%Y")
    dup_idx = set(rng.sample(range(len(buchungen)), 24))
    zeilen_export = 0
    with open(D_ROH / "weiterbildung_buchungen_2025.csv", "w", newline="", encoding="cp1252") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["BuchungsID", "Personalnr", "Kursnr", "Kurstitel", "Buchungsdatum", "Kursbeginn", "Kursende",
                    "Status", "Stunden", "Kosten", "Feedback"])
        for i, b in enumerate(buchungen):
            row = [b["BuchungsID"], str(int(b["Personalnr"])),            # Problem: führende Nullen fehlen
                   b["Kursnr"], kurs[b["Kursnr"]][1], de_date(b["Buchungsdatum"]), de_date(b["Kursbeginn"]),
                   de_date(b["Kursende"]), rng.choice(STATUS_VARIANTEN[b["Status"]]),
                   de_num(b["Stunden"]).replace(",00", "") if b["Stunden"] == int(b["Stunden"]) else de_num(b["Stunden"]),
                   de_num(b["Kosten"]) + " €", b["Feedback"]]
            w.writerow(row)
            zeilen_export += 1
            if i in dup_idx:                                           # Problem: doppelt exportiert
                w.writerow(row)
                zeilen_export += 1
        f.write(f"Summe;{zeilen_export} Datensätze;;;;;;;;;\r\n")          # Problem: Summenzeile am Ende

    # ---------------------------------------------------------------- Kennzahlen je Bereich (für Ziele + Kontrolle)
    ma_by = {p["Personalnr"]: p for p in ma}
    headcount_bereich = defaultdict(int)
    for p in ma:
        headcount_bereich[bereich_of[p["BereichID"]]] += 1
    kosten_bq = defaultdict(float)
    for b in buchungen:
        q = (b["Kursbeginn"].month - 1) // 3 + 1
        kosten_bq[(bereich_of[ma_by[b["Personalnr"]]["BereichID"]], q)] += b["Kosten"]

    # Budget: aus dem Vorjahresbedarf geplant – gleichmäßig über die Quartale, auf 500 € gerundet
    budget = {}
    for _, bname, *_ in BEREICHE:
        jahr = sum(kosten_bq[(bname, q)] for q in range(1, 5))
        faktor = 0.82 if bname == "Vertrieb" else rng.uniform(0.98, 1.12)
        verteilung = (0.24, 0.28, 0.18, 0.30)
        for q in range(1, 5):
            budget[(bname, q)] = int(round(jahr * faktor * verteilung[q - 1] / 500.0)) * 500

    zielwerte = {}
    for _, bname, *_ in BEREICHE:
        zielwerte[bname] = {
            "Ø Stunden je MA": {"Produktion": 14, "Logistik": 12, "Entwicklung": 20, "Service": 16,
                                "Vertrieb": 22, "IT": 28, "Verwaltung": 14}[bname],
            "Teilnahmequote": 0.75,
            "Pflichtquote": 0.95,
            "Zufriedenheit": 4.0,
        }

    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
        wb = Workbook()
        ws = wb.active
        ws.title = "Budget 2025"
        ws["A1"] = "Weiterbildungsbudget 2025 je Bereich (in €) – Personalentwicklung, Stand 10.12.2024"
        ws["A1"].font = Font(bold=True, size=13)
        ws.append([])
        ws.append(["Bereich", "Q1", "Q2", "Q3", "Q4", "Summe"])
        for c in ws[3]:
            c.font = Font(bold=True)
        for _, bname, *_ in BEREICHE:
            vals = [budget[(bname, q)] for q in range(1, 5)]
            ws.append([bname] + vals + [sum(vals)])
        ws.append(["Gesamt"] + [sum(budget[(b[1], q)] for b in BEREICHE) for q in range(1, 5)]
                  + [sum(budget.values())])
        for c in ws[ws.max_row]:
            c.font = Font(bold=True)

        ws2 = wb.create_sheet("Zielwerte 2025")
        ws2["A1"] = "Zielwerte Weiterbildung 2025 je Bereich"
        ws2["A1"].font = Font(bold=True, size=13)
        ws2.append([])
        kz_namen = ["Ø Stunden je MA", "Teilnahmequote", "Pflichtquote", "Zufriedenheit"]
        ws2.append(["Bereich"] + kz_namen)
        for c in ws2[3]:
            c.font = Font(bold=True)
        for _, bname, *_ in BEREICHE:
            ws2.append([bname] + [zielwerte[bname][k] for k in kz_namen])
            r = ws2.max_row
            ws2.cell(r, 3).number_format = "0%"
            ws2.cell(r, 4).number_format = "0%"
            ws2.cell(r, 5).number_format = "0.0"
        wb.properties.creator = "Personalentwicklung"
        wb.properties.created = dt.datetime(2024, 12, 10, 9, 0)
        wb.properties.modified = dt.datetime(2024, 12, 10, 9, 0)
        wb.save(D_ZIEL / "ziele_2025.xlsx")
    except ImportError:
        print("! openpyxl fehlt – ziele_2025.xlsx nicht erzeugt")

    with open(D_ZIEL / "budget_2025_kreuztabelle.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Bereich", "Q1", "Q2", "Q3", "Q4"])
        for _, bname, *_ in BEREICHE:
            w.writerow([bname] + [budget[(bname, q)] for q in range(1, 5)])
    with open(D_ZIEL / "zielwerte_2025_kreuztabelle.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Bereich", "Ø Stunden je MA", "Teilnahmequote", "Pflichtquote", "Zufriedenheit"])
        for _, bname, *_ in BEREICHE:
            z = zielwerte[bname]
            w.writerow([bname, z["Ø Stunden je MA"], z["Teilnahmequote"], z["Pflichtquote"], z["Zufriedenheit"]])

    # ---------------------------------------------------------------- Kontrollzahlen
    done = [b for b in buchungen if b["Status"] == "abgeschlossen"]

    def kennzahlen(personen, bu):
        pn = {p["Personalnr"] for p in personen}
        bu = [b for b in bu if b["Personalnr"] in pn]
        d = [b for b in bu if b["Status"] == "abgeschlossen"]
        hc = len(pn)
        pflicht_ok = 0
        for p in pn:
            erledigt = {b["Kursnr"] for b in d if b["Personalnr"] == p and b["Kursnr"] in PFLICHT}
            pflicht_ok += len(erledigt) == len(PFLICHT)
        fb = [int(b["Feedback"]) for b in d if b["Feedback"]]
        return {
            "Headcount": hc,
            "Buchungen": len(bu),
            "Teilnahmen": len(d),
            "Stunden": round(sum(b["Stunden"] for b in d), 1),
            "Kosten": round(sum(b["Kosten"] for b in bu), 2),
            "Oe_Stunden_je_MA": round(sum(b["Stunden"] for b in d) / hc, 2) if hc else None,
            "Teilnahmequote_pct": round(100 * len({b["Personalnr"] for b in d if b["Kursnr"] not in PFLICHT}) / hc, 1) if hc else None,
            "Pflichtquote_pct": round(100 * pflicht_ok / hc, 1) if hc else None,
            "Stornoquote_pct": round(100 * sum(b["Status"] == "storniert" for b in bu) / len(bu), 1) if bu else None,
            "NoShow_Quote_pct": round(100 * sum(b["Status"] == "No-Show" for b in bu) / len(bu), 1) if bu else None,
            "Oe_Zufriedenheit": round(sum(fb) / len(fb), 2) if fb else None,
            "Kosten_je_MA": round(sum(b["Kosten"] for b in bu) / hc, 2) if hc else None,
        }

    je_bereich = {}
    for _, bname, *_ in BEREICHE:
        pers = [p for p in ma if bereich_of[p["BereichID"]] == bname]
        k = kennzahlen(pers, buchungen)
        k["Budget"] = sum(budget[(bname, q)] for q in range(1, 5))
        k["Budget_Ausschoepfung_pct"] = round(100 * k["Kosten"] / k["Budget"], 1)
        je_bereich[bname] = k
    kz = {
        "roh_zeilen_inkl_kopf_und_summe": zeilen_export + 2,
        "roh_duplikate": len(dup_idx),
        "buchungen_nach_bereinigung": len(buchungen),
        "status_verteilung": {s: sum(b["Status"] == s for b in buchungen)
                              for s in ("abgeschlossen", "storniert", "No-Show", "angemeldet")},
        "gesamt": kennzahlen(ma, buchungen),
        "budget_gesamt": sum(budget.values()),
        "budget_je_quartal": {f"Q{q}": sum(budget[(b[1], q)] for b in BEREICHE) for q in range(1, 5)},
        "kosten_je_quartal": {f"Q{q}": round(sum(kosten_bq[(b[1], q)] for b in BEREICHE), 2) for q in range(1, 5)},
        "vertrieb_q2": {"Kosten": round(kosten_bq[("Vertrieb", 2)], 2), "Budget": budget[("Vertrieb", 2)]},
        "je_bereich": je_bereich,
        "je_standort": {s: kennzahlen([p for p in ma if p["Standort"] == s], buchungen) for s in STANDORTE},
        "je_beschaeftigung": {s: kennzahlen([p for p in ma if p["Beschaeftigung"] == s], buchungen)
                              for s in ("Vollzeit", "Teilzeit")},
        "je_rolle": {s: kennzahlen([p for p in ma if p["Rolle"] == s], buchungen)
                     for s in ("Mitarbeitende", "Führungskraft", "Auszubildende")},
        "pflichtkurs_quote_pct": {
            knr: round(100 * len({b["Personalnr"] for b in done if b["Kursnr"] == knr}) / len(ma), 1) for knr in PFLICHT},
        "ulm_produktion_logistik_datenschutz_pct": round(100 * len(
            {b["Personalnr"] for b in done if b["Kursnr"] == "K-001"
             and ma_by[b["Personalnr"]]["Standort"] == "Werk Ulm"
             and bereich_of[ma_by[b["Personalnr"]]["BereichID"]] in ("Produktion", "Logistik")})
            / sum(1 for p in ma if p["Standort"] == "Werk Ulm"
                  and bereich_of[p["BereichID"]] in ("Produktion", "Logistik")), 1),
        "kosten_je_kategorie": {kat: round(sum(b["Kosten"] for b in buchungen if kurs[b["Kursnr"]][2] == kat), 2)
                                for kat in sorted({k[2] for k in KURSE})},
        "stunden_je_monat": {f"{m:02d}": round(sum(b["Stunden"] for b in done if b["Kursbeginn"].month == m), 1)
                             for m in range(1, 13)},
        "zielwerte": zielwerte,
        # Gesamtziel = nach Headcount gewichteter Mittelwert der Bereichsziele (so rechnet das DAX-Measure)
        "ziel_gesamt_gewichtet": {
            kn: round(sum(zielwerte[b[1]][kn] * sum(1 for p in ma if p["BereichID"] == b[0]) for b in BEREICHE) / len(ma), 4)
            for kn in ("Ø Stunden je MA", "Teilnahmequote", "Pflichtquote")},
        "budget_ausschoepfung_gesamt_pct": round(100 * sum(b["Kosten"] for b in buchungen) / sum(budget.values()), 1),
    }
    (CASE / "daten" / "kontrollzahlen.json").write_text(json.dumps(kz, ensure_ascii=False, indent=2) + "\n",
                                                        encoding="utf-8")
    print(json.dumps({k: kz[k] for k in ("roh_zeilen_inkl_kopf_und_summe", "buchungen_nach_bereinigung",
                                         "status_verteilung", "gesamt", "budget_gesamt", "vertrieb_q2",
                                         "pflichtkurs_quote_pct", "ulm_produktion_logistik_datenschutz_pct")},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
