# Daten · Tag 2

Dieselben Verkäufe wie an Tag 1 – diesmal sauber, als Sternschema, plus ein Umsatzplan aus Excel.

| Datei | Inhalt | Zeilen |
|---|---|---:|
| `fakt_verkaeufe.csv` | ein Beleg je Zeile: Datum, Filiale, Produkt, Kunde, Menge, Rabatt | 2.877 |
| `dim_produkt.csv` | Produkt, Kategorie, Listenpreis, Einstandspreis | 18 |
| `dim_kunde.csv` | Kunde, Segment, PLZ (**als Text laden!**), Ort | 161 |
| `dim_filiale.csv` | Filiale, Bundesland, Eröffnung, Fläche | 4 |
| `plan_2025.xlsx` | Umsatzplan als Excel-Kreuztabelle (Filialen × Monate) | 4 |
| `plan_2025_kreuztabelle.csv` | derselbe Plan als CSV (Extra-Übung Entpivotieren) | 4 |

**In Power BI laden:** Daten abrufen → **Web** → Anonym → Adresse + Dateiname:
```
https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/02-Tag-2/Daten/
```
z. B. `…/02-Tag-2/Daten/fakt_verkaeufe.csv`. Kein Internet? Datei anklicken → **Download** (⬇) → **Text/CSV** bzw. **Excel-Arbeitsmappe**.

Zurück zur [Übung](../README.md).
