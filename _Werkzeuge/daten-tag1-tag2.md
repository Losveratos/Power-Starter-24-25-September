# Übungsdaten · Rad & Tat GmbH

Fiktiver Fahrradhändler mit vier Filialen, Geschäftsjahr 2025. Alle Daten sind **simuliert** –
Namen, Kunden und Zahlen sind erfunden. Frei verwendbar (MIT-Lizenz dieses Repos).

## In Power BI laden

**Daten abrufen → Web** → Anmeldung **Anonym** → eine dieser Adressen:

| Datei | Tag | Web-Adresse |
|---|---|---|
| `tag1/verkaeufe_2025_roh.csv` | 1 | `https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/01-Tag-1/Daten/verkaeufe_2025_roh.csv` |
| `tag2/fakt_verkaeufe.csv` | 2 | `https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/02-Tag-2/Daten/fakt_verkaeufe.csv` |
| `tag2/dim_produkt.csv` | 2 | `https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/02-Tag-2/Daten/dim_produkt.csv` |
| `tag2/dim_kunde.csv` | 2 | `https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/02-Tag-2/Daten/dim_kunde.csv` |
| `tag2/dim_filiale.csv` | 2 | `https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/02-Tag-2/Daten/dim_filiale.csv` |
| `tag2/plan_2025.xlsx` | 2 | `https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/02-Tag-2/Daten/plan_2025.xlsx` |
| `tag2/plan_2025_kreuztabelle.csv` | ⭐ | `https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/02-Tag-2/Daten/plan_2025_kreuztabelle.csv` |

Firmen-Proxy blockt GitHub? Dateien auf GitHub anklicken → **Download raw file** → in Power BI über
**Text/CSV** bzw. **Excel-Arbeitsmappe** laden.

## Was steckt drin

### Tag 1 · `verkaeufe_2025_roh.csv` – ein Kassen-Export, absichtlich unordentlich
2.877 Belege · Spalten `Belegnummer, Belegdatum, Filiale, Kategorie, Produkt, Menge, Umsatz, Kosten`

Eingebaute Probleme: Kopfzeile des Exports über den Überschriften · 6 leere Zeilen · Leerzeichen
hinter Filialnamen · Kategorien teils kleingeschrieben · Punkt als Dezimalzeichen.

### Tag 2 · dieselben Verkäufe als Sternschema
| Datei | Schlüssel | Inhalt |
|---|---|---|
| `fakt_verkaeufe.csv` | Belegnummer | Belegdatum, FilialeID, ProduktID, KundeID, Menge, Rabatt (0–0,25) |
| `dim_produkt.csv` | ProduktID | 18 Produkte in 5 Kategorien, Listen- und Einstandspreis |
| `dim_kunde.csv` | KundeID | 161 Kunden, Segment Privat/Gewerbe, PLZ (Text! führende Null), Ort |
| `dim_filiale.csv` | FilialeID | 4 Filialen, Bundesland, Eröffnung, Verkaufsfläche |
| `plan_2025.xlsx` | – | Umsatzplan als Kreuztabelle (Filialen × Monate, mit Titel- und Summenzeile) |
| `plan_2025_kreuztabelle.csv` | – | derselbe Plan als CSV, Monate als Spalten `01`–`12` |

`Umsatz = Menge × Listenpreis × (1 − Rabatt)` · `Kosten = Menge × Einstandspreis`

### Die Geschichte in den Daten (für Trainer:innen – nicht vorab verraten 🤫)
Köln startet im **Juni** eine Rabattaktion (15–25 %), die nie beendet wird. Der Umsatz bleibt
unauffällig, die Marge fällt von 33,3 % auf 20,6 %. Im Plan-Ist sieht Köln deshalb sogar am besten aus.

## Kontrollzahlen

Alle Zahlen, die in den Übungen vorkommen, stehen maschinenlesbar in
[`kontrollzahlen.json`](kontrollzahlen-tag1-tag2.json).

## Neu erzeugen

```bash
pip install openpyxl
python3 _Werkzeuge/tag-daten_erzeugen.py
```
Fester Zufalls-Seed – die Daten und Kontrollzahlen bleiben gleich. Wer andere Daten will (mehr
Filialen, anderes Jahr), ändert die Konstanten oben im Skript.
