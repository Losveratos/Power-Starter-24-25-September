#!/usr/bin/env python3
"""Erzeugt die Übungsdaten für das Power-BI-Starter-Training (fiktive Firma „Rad & Tat GmbH").

Deterministisch (fester Seed): Wer das Skript erneut laufen lässt, bekommt dieselben
Daten und damit dieselben Kontrollzahlen (die CSVs sind byte-gleich; die .xlsx enthält
einen Zip-Zeitstempel und unterscheidet sich deshalb nur binär). Die Kontrollzahlen landen in
daten/kontrollzahlen.json und werden in den Übungen zitiert.

Aufruf (aus dem Repo-Root):  python3 tools/generate_data.py
Braucht für die Plan-Datei openpyxl (pip install openpyxl).
"""
import csv
import datetime as dt
import json
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT1 = ROOT / "daten" / "tag1"
OUT2 = ROOT / "daten" / "tag2"
YEAR = 2025
rng = random.Random(2425)

FILIALEN = [
    # id, name, bundesland, eröffnet, verkaufsfläche m²
    ("F1", "Hamburg", "Hamburg", "2012-04-01", 820),
    ("F2", "Köln", "Nordrhein-Westfalen", "2016-09-15", 640),
    ("F3", "München", "Bayern", "2014-03-01", 910),
    ("F4", "Leipzig", "Sachsen", "2021-05-01", 480),
]
FIL_WEIGHT = {"F1": 1.0, "F2": 0.85, "F3": 1.15, "F4": 0.6}

PRODUKTE = [
    # id, produkt, kategorie, listenpreis, einstandspreis
    ("P01", "Stadtrad Classic", "Fahrräder", 649.00, 410.00),
    ("P02", "Trekkingrad Tour", "Fahrräder", 899.00, 560.00),
    ("P03", "Gravelbike Kies", "Fahrräder", 1299.00, 830.00),
    ("P04", "Kinderrad 20 Zoll", "Fahrräder", 329.00, 205.00),
    ("P05", "E-Bike City", "E-Bikes", 2499.00, 1690.00),
    ("P06", "E-Bike Trekking", "E-Bikes", 3199.00, 2170.00),
    ("P07", "E-Lastenrad", "E-Bikes", 4990.00, 3490.00),
    ("P08", "Helm Urban", "Zubehör", 79.90, 38.00),
    ("P09", "Faltschloss", "Zubehör", 59.90, 27.50),
    ("P10", "Fahrradtasche", "Zubehör", 89.00, 44.00),
    ("P11", "Lichtset LED", "Zubehör", 39.90, 16.80),
    ("P12", "Luftpumpe", "Zubehör", 24.90, 9.90),
    ("P13", "Regenjacke", "Bekleidung", 129.00, 61.00),
    ("P14", "Radhose", "Bekleidung", 69.00, 29.00),
    ("P15", "Handschuhe", "Bekleidung", 29.90, 11.50),
    ("P16", "Inspektion Standard", "Werkstatt", 89.00, 52.00),
    ("P17", "Inspektion E-Bike", "Werkstatt", 149.00, 88.00),
    ("P18", "Schlauchwechsel", "Werkstatt", 19.90, 9.00),
]
# relative Kaufwahrscheinlichkeit je Produkt und typische Menge
PROD_WEIGHT = {"P01": 6, "P02": 5, "P03": 2, "P04": 3, "P05": 4, "P06": 3, "P07": 1,
               "P08": 9, "P09": 8, "P10": 6, "P11": 9, "P12": 7, "P13": 4, "P14": 4,
               "P15": 5, "P16": 8, "P17": 5, "P18": 9}
MAX_MENGE = {"Fahrräder": 1, "E-Bikes": 1, "Werkstatt": 1, "Zubehör": 3, "Bekleidung": 2}
# Saison: Faktor je Monat (Frühjahr/Sommer stark, Winter schwach)
SAISON = {1: 0.45, 2: 0.55, 3: 0.95, 4: 1.35, 5: 1.5, 6: 1.4, 7: 1.3, 8: 1.2,
          9: 1.0, 10: 0.8, 11: 0.6, 12: 0.75}

VORNAMEN = ["Anna", "Ben", "Clara", "David", "Elif", "Finn", "Greta", "Hannes", "Ida", "Jonas",
            "Kira", "Lukas", "Mia", "Noah", "Olga", "Paul", "Rana", "Sven", "Tara", "Umut"]
NACHNAMEN = ["Becker", "Schulz", "Yilmaz", "Wagner", "Nowak", "Hoffmann", "Krüger", "Lange",
             "Richter", "Wolf", "Kaya", "Braun", "Zimmermann", "Hartmann", "Schmitt"]
FIRMEN = ["Kurierdienst Flink", "Stadtwerke Service", "Pflegedienst Lotse", "Café Speiche",
          "Architekturbüro Nord", "Physio am Park", "Bäckerei Korn", "Lieferheld Süd",
          "Hausmeister Kraft", "Agentur Pixel", "Blumen Blüte", "Handwerk Meyer"]
ORTE = {"F1": [("20095", "Hamburg"), ("22765", "Hamburg"), ("21073", "Hamburg"), ("25421", "Pinneberg")],
        "F2": [("50667", "Köln"), ("50937", "Köln"), ("51373", "Leverkusen"), ("50321", "Brühl")],
        "F3": [("80331", "München"), ("81541", "München"), ("85521", "Ottobrunn"), ("82008", "Unterhaching")],
        "F4": [("04109", "Leipzig"), ("04275", "Leipzig"), ("04416", "Markkleeberg"), ("04435", "Schkeuditz")]}


def kunden():
    rows, n = [], 1
    for fid, *_ in FILIALEN:
        count = int(45 * FIL_WEIGHT[fid])
        for _ in range(count):
            gewerbe = rng.random() < 0.15
            name = rng.choice(FIRMEN) if gewerbe else f"{rng.choice(VORNAMEN)} {rng.choice(NACHNAMEN)}"
            plz, ort = rng.choice(ORTE[fid])
            rows.append({"KundeID": f"K{n:04d}", "Kunde": name,
                         "Segment": "Gewerbe" if gewerbe else "Privat",
                         "PLZ": plz, "Ort": ort, "StammFilialeID": fid})
            n += 1
    return rows


def rabatt(fid, datum, segment):
    # Die Story: Köln startet im Juni eine Rabattaktion, die nie beendet wird.
    if fid == "F2" and datum.month >= 6:
        return rng.choice([0.15, 0.20, 0.20, 0.25])
    base = [0.0, 0.0, 0.0, 0.03, 0.05, 0.05, 0.10]
    if segment == "Gewerbe":
        base = [0.05, 0.08, 0.10, 0.10]
    return rng.choice(base)


def main():
    OUT1.mkdir(parents=True, exist_ok=True)
    OUT2.mkdir(parents=True, exist_ok=True)
    kd = kunden()
    kd_by_fil = defaultdict(list)
    for k in kd:
        kd_by_fil[k["StammFilialeID"]].append(k)
    prod = {p[0]: p for p in PRODUKTE}
    fil = {f[0]: f for f in FILIALEN}
    pids, pw = list(PROD_WEIGHT), list(PROD_WEIGHT.values())

    fakt = []
    beleg = 100000
    day = dt.date(YEAR, 1, 1)
    while day.year == YEAR:
        if day.weekday() != 6:  # sonntags geschlossen
            for fid, *_ in FILIALEN:
                lam = 2.4 * FIL_WEIGHT[fid] * SAISON[day.month] * (1.35 if day.weekday() == 5 else 1.0)
                n = sum(1 for _ in range(12) if rng.random() < lam / 12)
                for _ in range(n):
                    beleg += 1
                    k = rng.choice(kd_by_fil[fid]) if rng.random() < 0.9 else rng.choice(kd)
                    pid = rng.choices(pids, pw)[0]
                    menge = rng.randint(1, MAX_MENGE[prod[pid][2]])
                    fakt.append({"Belegnummer": f"B{beleg}", "Belegdatum": day.isoformat(),
                                 "FilialeID": fid, "ProduktID": pid, "KundeID": k["KundeID"],
                                 "Menge": menge, "Rabatt": rabatt(fid, day, k["Segment"])})
        day += dt.timedelta(days=1)

    # ---------- Tag 2: sauberes Sternschema ----------
    def write(path, rows, fields, **kw):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields, **kw)
            w.writeheader()
            w.writerows(rows)

    write(OUT2 / "fakt_verkaeufe.csv", fakt,
          ["Belegnummer", "Belegdatum", "FilialeID", "ProduktID", "KundeID", "Menge", "Rabatt"])
    write(OUT2 / "dim_produkt.csv",
          [{"ProduktID": p[0], "Produkt": p[1], "Kategorie": p[2], "Listenpreis": f"{p[3]:.2f}",
            "Einstandspreis": f"{p[4]:.2f}"} for p in PRODUKTE],
          ["ProduktID", "Produkt", "Kategorie", "Listenpreis", "Einstandspreis"])
    write(OUT2 / "dim_kunde.csv", kd, ["KundeID", "Kunde", "Segment", "PLZ", "Ort", "StammFilialeID"])
    write(OUT2 / "dim_filiale.csv",
          [{"FilialeID": f[0], "Filiale": f[1], "Bundesland": f[2], "Eroeffnet": f[3],
            "Verkaufsflaeche_m2": f[4]} for f in FILIALEN],
          ["FilialeID", "Filiale", "Bundesland", "Eroeffnet", "Verkaufsflaeche_m2"])

    # ---------- Tag 1: dieselben Verkäufe als unordentlicher Kassen-Export ----------
    flat = []
    for r in fakt:
        p = prod[r["ProduktID"]]
        umsatz = round(r["Menge"] * p[3] * (1 - r["Rabatt"]), 2)
        kosten = round(r["Menge"] * p[4], 2)
        flat.append((r, p, umsatz, kosten))

    blank_at = set(rng.sample(range(len(flat)), 6))
    with open(OUT1 / "verkaeufe_2025_roh.csv", "w", newline="", encoding="utf-8") as f:
        f.write("Export RT-Kasse v4.2 | Rad & Tat GmbH | erstellt 2026-01-02 06:00 | alle Filialen\n")
        w = csv.writer(f)
        w.writerow(["Belegnummer", "Belegdatum", "Filiale", "Kategorie", "Produkt", "Menge", "Umsatz", "Kosten"])
        for i, (r, p, umsatz, kosten) in enumerate(flat):
            filname = fil[r["FilialeID"]][1]
            if rng.random() < 0.08:
                filname += rng.choice([" ", "  "])       # Problem: Leerzeichen am Ende
            kat = p[2].lower() if rng.random() < 0.07 else p[2]  # Problem: Kleinschreibung
            w.writerow([r["Belegnummer"], r["Belegdatum"], filname, kat, p[1], r["Menge"],
                        f"{umsatz:.2f}", f"{kosten:.2f}"])
            if i in blank_at:
                f.write(",,,,,,,\n")                      # Problem: leere Zeilen

    # ---------- Tag 2: Plan als Excel-Kreuztabelle ----------
    ist = defaultdict(float)
    for r, p, umsatz, _ in flat:
        ist[(r["FilialeID"], int(r["Belegdatum"][5:7]))] += umsatz
    plan = {}
    saison_summe = sum(SAISON.values())
    for fid, *_ in FILIALEN:
        # Plan = Vorjahresbasis × Wachstumsziel, verteilt nach Saisonkurve, auf 500 € gerundet
        jahr = sum(ist[(fid, m)] for m in range(1, 13)) * rng.uniform(1.02, 1.09)
        for m in range(1, 13):
            plan[(fid, m)] = int(round(jahr * SAISON[m] / saison_summe / 500.0)) * 500
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
        wb = Workbook()
        ws = wb.active
        ws.title = "Plan 2025"
        ws["A1"] = "Umsatzplan 2025 je Filiale (in €) – Stand Controlling 15.12.2024"
        ws["A1"].font = Font(bold=True, size=13)
        monate = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
        ws.append([])
        ws.append(["Filiale"] + monate + ["Gesamt"])
        for c in ws[3]:
            c.font = Font(bold=True)
        for fid, name, *_ in FILIALEN:
            vals = [plan[(fid, m)] for m in range(1, 13)]
            ws.append([name] + vals + [sum(vals)])
        # deterministische Datei: feste Metadaten
        wb.properties.creator = "Rad & Tat Controlling"
        wb.properties.created = dt.datetime(2024, 12, 15, 9, 0)
        wb.properties.modified = dt.datetime(2024, 12, 15, 9, 0)
        wb.save(OUT2 / "plan_2025.xlsx")
    except ImportError:
        print("! openpyxl fehlt – plan_2025.xlsx nicht erzeugt")
    write(OUT2 / "plan_2025_kreuztabelle.csv",
          [{"Filiale": fil[fid][1], **{f"{m:02d}": plan[(fid, m)] for m in range(1, 13)}}
           for fid in fil],
          ["Filiale"] + [f"{m:02d}" for m in range(1, 13)])

    # ---------- Kontrollzahlen ----------
    def agg(key):
        d = defaultdict(lambda: [0.0, 0.0])
        for r, p, u, k in flat:
            kk = key(r, p)
            d[kk][0] += u
            d[kk][1] += k
        return {kk: {"Umsatz": round(v[0], 2), "Kosten": round(v[1], 2),
                     "Marge_pct": round(100 * (v[0] - v[1]) / v[0], 1)} for kk, v in sorted(d.items())}

    tu = sum(x[2] for x in flat)
    tk = sum(x[3] for x in flat)
    avg_marge = sum((u - k) / u for _, _, u, k in flat) / len(flat)
    kz = {
        "zeilen_roh_datei_inkl_kopf_und_leer": len(flat) + 2 + len(blank_at),
        "zeilen_nach_bereinigung": len(flat),
        "umsatz_gesamt": round(tu, 2),
        # Tag 2 rechnet Umsatz per SUMX ungerundet aus Menge × Listenpreis × (1 − Rabatt):
        "umsatz_gesamt_sumx_ungerundet": round(sum(
            r["Menge"] * prod[r["ProduktID"]][3] * (1 - r["Rabatt"]) for r in fakt), 2),
        "kosten_gesamt": round(tk, 2),
        "marge_gesamt_pct": round(100 * (tu - tk) / tu, 1),
        "marge_falsch_mittelwert_der_zeilen_pct": round(100 * avg_marge, 1),
        "menge_gesamt": sum(r["Menge"] for r, *_ in flat),
        "belege": len(fakt),
        "kunden": len(kd),
        "je_filiale": {fil[k][1]: v for k, v in agg(lambda r, p: r["FilialeID"]).items()},
        "je_kategorie": agg(lambda r, p: p[2]),
        "koeln_vor_und_ab_juni": {
            h: v for (f, h), v in agg(lambda r, p: (
                r["FilialeID"], "Jan–Mai" if int(r["Belegdatum"][5:7]) <= 5 else "Jun–Dez")).items()
            if f == "F2"},
        "je_monat": {f"{k:02d}": v["Umsatz"] for k, v in agg(lambda r, p: int(r["Belegdatum"][5:7])).items()},
        "plan_gesamt": sum(plan.values()),
        "plan_je_filiale": {fil[fid][1]: sum(plan[(fid, m)] for m in range(1, 13)) for fid in fil},
    }
    kz["abweichung_ist_plan"] = round(tu - kz["plan_gesamt"], 2)

    # Tag 2: Kontrollzahlen so, wie die DAX-Measures sie liefern (SUMX, ungerundet)
    def u(r):
        return r["Menge"] * prod[r["ProduktID"]][3] * (1 - r["Rabatt"])

    def k(r):
        return r["Menge"] * prod[r["ProduktID"]][4]

    def measures(rows):
        um, ko = sum(map(u, rows)), sum(map(k, rows))
        return {"Umsatz": round(um, 2), "Kosten": round(ko, 2), "Marge_pct": round(100 * (um - ko) / um, 1)}

    seg = {x["KundeID"]: x["Segment"] for x in kd}
    ist_fil = {fid: sum(u(r) for r in fakt if r["FilialeID"] == fid) for fid in fil}
    kz["tag2_dax"] = {
        "Umsatz": round(sum(map(u, fakt)), 2),
        "Kosten": round(sum(map(k, fakt)), 2),
        "Marge_pct": measures(fakt)["Marge_pct"],
        "Belege": len(fakt),
        "Kunden_aktiv": len({r["KundeID"] for r in fakt}),
        "Kunden_ohne_Kauf": len({x["KundeID"] for x in kd} - {r["KundeID"] for r in fakt}),
        "Oe_Bon": round(sum(map(u, fakt)) / len(fakt), 2),
        "Umsatz_E_Bikes": round(sum(u(r) for r in fakt if prod[r["ProduktID"]][2] == "E-Bikes"), 2),
        "je_segment": {sg: measures([r for r in fakt if seg[r["KundeID"]] == sg]) for sg in ("Privat", "Gewerbe")},
        "koeln_jun_dez": measures([r for r in fakt if r["FilialeID"] == "F2" and int(r["Belegdatum"][5:7]) >= 6]),
        "umsatz_kumuliert_bis_30_06": round(sum(u(r) for r in fakt if r["Belegdatum"] <= f"{YEAR}-06-30"), 2),
        "plan_abweichung": round(sum(map(u, fakt)) - kz["plan_gesamt"], 2),
        "plan_abweichung_pct": round(100 * (sum(map(u, fakt)) - kz["plan_gesamt"]) / kz["plan_gesamt"], 1),
        "plan_abweichung_je_filiale": {
            fil[fid][1]: round(ist_fil[fid] - kz["plan_je_filiale"][fil[fid][1]], 2) for fid in fil},
    }
    (ROOT / "daten" / "kontrollzahlen.json").write_text(
        json.dumps(kz, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(kz, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
