#!/usr/bin/env python3
"""Demo-Kreuztabelle: 96 deutsche Bahnhöfe × 12 Monate 2025 (Reisende pro Monat).

Ausgangswerte: Reisende pro Tag je Bahnhof (Vorgabe des Trainers, gerundete öffentliche Größenordnungen).
Die Monatswerte sind SIMULIERT: Tageswert × Tage im Monat × Saisonfaktor × kleines Rauschen,
anschließend so skaliert, dass die Jahressumme genau Tageswert × 365 ergibt.

Die Tabelle ist absichtlich denormalisiert (Stadt, Bundesland, Größenklasse in jeder Zeile, Monate als Spalten),
damit man daran Normalisierung und Sternschema erklären kann.

Wird von daten_erzeugen.py aufgerufen, geht aber auch allein:
  python3 _Werkzeuge/fall-bahn/bahnhoefe_kreuztabelle.py
"""
import calendar
import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ZIEL = ROOT / "05-Fall-Bahn" / "Daten" / "1-Rohdaten" / "bahnhoefe_reisende_2025_kreuztabelle.csv"
JAHR = 2025
SEED = 2509

# Bahnhof, Reisende pro Tag, Stadt, Bundesland
BAHNHOEFE = [
    ("Aachen Hauptbahnhof", 25000, "Aachen", "Nordrhein-Westfalen"),
    ("Aschaffenburg Hauptbahnhof", 14000, "Aschaffenburg", "Bayern"),
    ("Augsburg Hauptbahnhof", 43500, "Augsburg", "Bayern"),
    ("Bamberg", 15000, "Bamberg", "Bayern"),
    ("Berlin Friedrichstraße", 262000, "Berlin", "Berlin"),
    ("Berlin Gesundbrunnen", 203000, "Berlin", "Berlin"),
    ("Berlin Hauptbahnhof", 329000, "Berlin", "Berlin"),
    ("Berlin Ostbahnhof", 100000, "Berlin", "Berlin"),
    ("Berlin Ostkreuz", 255000, "Berlin", "Berlin"),
    ("Berlin Potsdamer Platz", 30000, "Berlin", "Berlin"),
    ("Berlin Südkreuz", 179000, "Berlin", "Berlin"),
    ("Berlin Zoologischer Garten", 125000, "Berlin", "Berlin"),
    ("Berlin-Lichtenberg", 85000, "Berlin", "Berlin"),
    ("Berlin-Spandau", 45000, "Berlin", "Berlin"),
    ("Berlin-Wannsee", 30000, "Berlin", "Berlin"),
    ("Bielefeld Hauptbahnhof", 40000, "Bielefeld", "Nordrhein-Westfalen"),
    ("Bochum Hauptbahnhof", 65000, "Bochum", "Nordrhein-Westfalen"),
    ("Bonn Hauptbahnhof", 67000, "Bonn", "Nordrhein-Westfalen"),
    ("Braunschweig Hauptbahnhof", 66000, "Braunschweig", "Niedersachsen"),
    ("Bremen Hauptbahnhof", 147000, "Bremen", "Bremen"),
    ("Chemnitz Hauptbahnhof", 13000, "Chemnitz", "Sachsen"),
    ("Cottbus Hauptbahnhof", 12000, "Cottbus", "Brandenburg"),
    ("Darmstadt Hauptbahnhof", 40000, "Darmstadt", "Hessen"),
    ("Dortmund Hauptbahnhof", 130000, "Dortmund", "Nordrhein-Westfalen"),
    ("Dresden Hauptbahnhof", 60000, "Dresden", "Sachsen"),
    ("Dresden-Neustadt", 26000, "Dresden", "Sachsen"),
    ("Duisburg Hauptbahnhof", 130000, "Duisburg", "Nordrhein-Westfalen"),
    ("Düsseldorf Hauptbahnhof", 246000, "Düsseldorf", "Nordrhein-Westfalen"),
    ("Erfurt Hauptbahnhof", 46000, "Erfurt", "Thüringen"),
    ("Essen Hauptbahnhof", 152000, "Essen", "Nordrhein-Westfalen"),
    ("Flughafen BER", 120000, "Schönefeld", "Brandenburg"),
    ("Frankfurt (Main) Hauptbahnhof", 493000, "Frankfurt am Main", "Hessen"),
    ("Frankfurt (Main) Süd", 22500, "Frankfurt am Main", "Hessen"),
    ("Freiburg (Breisgau) Hauptbahnhof", 75000, "Freiburg im Breisgau", "Baden-Württemberg"),
    ("Fulda", 20000, "Fulda", "Hessen"),
    ("Fürth (Bayern) Hauptbahnhof", 10000, "Fürth", "Bayern"),
    ("Gelsenkirchen Hauptbahnhof", 17500, "Gelsenkirchen", "Nordrhein-Westfalen"),
    ("Gießen", 28000, "Gießen", "Hessen"),
    ("Göttingen", 49000, "Göttingen", "Niedersachsen"),
    ("Hagen Hauptbahnhof", 30000, "Hagen", "Nordrhein-Westfalen"),
    ("Halle (Saale) Hauptbahnhof", 40000, "Halle (Saale)", "Sachsen-Anhalt"),
    ("Hamburg Dammtor", 43000, "Hamburg", "Hamburg"),
    ("Hamburg Hauptbahnhof", 537000, "Hamburg", "Hamburg"),
    ("Hamburg-Altona", 138000, "Hamburg", "Hamburg"),
    ("Hamburg-Harburg", 80000, "Hamburg", "Hamburg"),
    ("Hamm (Westfalen) Hauptbahnhof", 27000, "Hamm", "Nordrhein-Westfalen"),
    ("Hanau Hauptbahnhof", 20000, "Hanau", "Hessen"),
    ("Hannover Hauptbahnhof", 261000, "Hannover", "Niedersachsen"),
    ("Heidelberg Hauptbahnhof", 42000, "Heidelberg", "Baden-Württemberg"),
    ("Heilbronn Hauptbahnhof", 14000, "Heilbronn", "Baden-Württemberg"),
    ("Herford", 12000, "Herford", "Nordrhein-Westfalen"),
    ("Hildesheim Hauptbahnhof", 30500, "Hildesheim", "Niedersachsen"),
    ("Ingolstadt Hauptbahnhof", 12500, "Ingolstadt", "Bayern"),
    ("Kaiserslautern Hauptbahnhof", 24000, "Kaiserslautern", "Rheinland-Pfalz"),
    ("Karlsruhe Hauptbahnhof", 72000, "Karlsruhe", "Baden-Württemberg"),
    ("Kassel Hauptbahnhof", 12000, "Kassel", "Hessen"),
    ("Kassel-Wilhelmshöhe", 30000, "Kassel", "Hessen"),
    ("Kiel Hauptbahnhof", 37000, "Kiel", "Schleswig-Holstein"),
    ("Koblenz Hauptbahnhof", 28000, "Koblenz", "Rheinland-Pfalz"),
    ("Köln Hauptbahnhof", 318000, "Köln", "Nordrhein-Westfalen"),
    ("Köln Messe/Deutz", 70000, "Köln", "Nordrhein-Westfalen"),
    ("Leipzig Hauptbahnhof", 135000, "Leipzig", "Sachsen"),
    ("Lübeck Hauptbahnhof", 34000, "Lübeck", "Schleswig-Holstein"),
    ("Ludwigshafen (Rhein) Hauptbahnhof", 16000, "Ludwigshafen am Rhein", "Rheinland-Pfalz"),
    ("Magdeburg Hauptbahnhof", 32000, "Magdeburg", "Sachsen-Anhalt"),
    ("Mainz Hauptbahnhof", 75000, "Mainz", "Rheinland-Pfalz"),
    ("Mannheim Hauptbahnhof", 118000, "Mannheim", "Baden-Württemberg"),
    ("Mönchengladbach Hauptbahnhof", 12000, "Mönchengladbach", "Nordrhein-Westfalen"),
    ("München Hauptbahnhof", 413000, "München", "Bayern"),
    ("München Ost", 174000, "München", "Bayern"),
    ("München-Pasing", 139000, "München", "Bayern"),
    ("Münster (Westfalen) Hauptbahnhof", 70000, "Münster", "Nordrhein-Westfalen"),
    ("Neumünster", 13000, "Neumünster", "Schleswig-Holstein"),
    ("Neuss Hauptbahnhof", 13000, "Neuss", "Nordrhein-Westfalen"),
    ("Neustadt (Weinstraße) Hauptbahnhof", 20000, "Neustadt an der Weinstraße", "Rheinland-Pfalz"),
    ("Nürnberg Hauptbahnhof", 210000, "Nürnberg", "Bayern"),
    ("Offenburg", 27000, "Offenburg", "Baden-Württemberg"),
    ("Oldenburg (Oldenburg) Hauptbahnhof", 25000, "Oldenburg", "Niedersachsen"),
    ("Osnabrück Hauptbahnhof", 20000, "Osnabrück", "Niedersachsen"),
    ("Paderborn Hauptbahnhof", 11500, "Paderborn", "Nordrhein-Westfalen"),
    ("Pforzheim Hauptbahnhof", 50000, "Pforzheim", "Baden-Württemberg"),
    ("Potsdam Hauptbahnhof", 70000, "Potsdam", "Brandenburg"),
    ("Rheine", 12000, "Rheine", "Nordrhein-Westfalen"),
    ("Rosenheim", 20000, "Rosenheim", "Bayern"),
    ("Rostock Hauptbahnhof", 24000, "Rostock", "Mecklenburg-Vorpommern"),
    ("Saarbrücken Hauptbahnhof", 29000, "Saarbrücken", "Saarland"),
    ("Solingen Hauptbahnhof", 16000, "Solingen", "Nordrhein-Westfalen"),
    ("Stuttgart Hauptbahnhof", 255000, "Stuttgart", "Baden-Württemberg"),
    ("Trier Hauptbahnhof", 18000, "Trier", "Rheinland-Pfalz"),
    ("Tübingen Hauptbahnhof", 50000, "Tübingen", "Baden-Württemberg"),
    ("Ulm Hauptbahnhof", 29000, "Ulm", "Baden-Württemberg"),
    ("Wiesbaden Hauptbahnhof", 46000, "Wiesbaden", "Hessen"),
    ("Wolfsburg Hauptbahnhof", 10000, "Wolfsburg", "Niedersachsen"),
    ("Worms Hauptbahnhof", 15000, "Worms", "Rheinland-Pfalz"),
    ("Wuppertal Hauptbahnhof", 40000, "Wuppertal", "Nordrhein-Westfalen"),
    ("Würzburg Hauptbahnhof", 28000, "Würzburg", "Bayern"),
]

# Reisende pro Tag im Monat relativ zum Jahresschnitt: Winterdelle im Januar, Pendler-Hoch im Frühjahr/Herbst,
# Sommerferien im August, Weihnachtsreiseverkehr im Dezember
SAISON = [0.92, 0.97, 1.00, 1.01, 1.03, 1.03, 0.99, 0.94, 1.03, 1.03, 1.02, 1.03]
# Flughafenbahnhof: Urlaubsverkehr – Sommer und Ferien stärker
SAISON_FLUGHAFEN = [0.88, 0.90, 0.97, 1.03, 1.03, 1.06, 1.12, 1.12, 1.04, 1.02, 0.92, 0.95]


def groessenklasse(pro_tag):
    if pro_tag >= 200_000:
        return "A · Metropolknoten (ab 200.000/Tag)"
    if pro_tag >= 50_000:
        return "B · Großstadtbahnhof (50.000–199.999/Tag)"
    return "C · Regionalbahnhof (unter 50.000/Tag)"


def monatswerte(pro_tag, saison, rng):
    tage = [calendar.monthrange(JAHR, m)[1] for m in range(1, 13)]
    roh = [pro_tag * t * s * rng.uniform(0.98, 1.02) for t, s in zip(tage, saison)]
    ziel = pro_tag * sum(tage)
    werte = [round(r * ziel / sum(roh)) for r in roh]
    werte[-1] += ziel - sum(werte)          # Rundungsrest in den Dezember
    return werte


def main():
    rng = random.Random(SEED)
    monate = [f"{JAHR}-{m:02d}" for m in range(1, 13)]
    zeilen = []
    for name, pro_tag, stadt, land in BAHNHOEFE:
        saison = SAISON_FLUGHAFEN if name.startswith("Flughafen") else SAISON
        zeilen.append([name, stadt, land, groessenklasse(pro_tag), *monatswerte(pro_tag, saison, rng)])
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    # UTF-8 mit BOM, damit auch Excel die Umlaute beim Doppelklick richtig zeigt
    with ZIEL.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";", lineterminator="\r\n")
        w.writerow(["Bahnhof", "Stadt", "Bundesland", "Größenklasse", *monate])
        w.writerows(zeilen)
    jahr = sum(sum(z[4:]) for z in zeilen)
    return {
        "datei": ZIEL.name,
        "bahnhoefe": len(zeilen),
        "zeilen_entpivotiert": len(zeilen) * 12,
        "reisende_pro_tag_summe": sum(b[1] for b in BAHNHOEFE),
        "reisende_2025_summe": jahr,
        "reisende_je_monat": {m: sum(z[4 + i] for z in zeilen) for i, m in enumerate(monate)},
        "bundeslaender": len({b[3] for b in BAHNHOEFE}),
        "staedte": len({b[2] for b in BAHNHOEFE}),
        "groessenklassen": {k: sum(1 for b in BAHNHOEFE if groessenklasse(b[1]) == k)
                            for k in sorted({groessenklasse(b[1]) for b in BAHNHOEFE})},
        "hamburg_hbf_2025": next(sum(z[4:]) for z in zeilen if z[0] == "Hamburg Hauptbahnhof"),
        "bundesland_top": max(((l, sum(sum(z[4:]) for z in zeilen if z[2] == l)) for l in {b[3] for b in BAHNHOEFE}),
                              key=lambda t: t[1]),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(main(), ensure_ascii=False, indent=2))
