# Daten · Fall Weiterbildungs-Monitoring

| Ordner | Datei | Inhalt |
|---|---|---|
| `1-Rohdaten` | `weiterbildung_buchungen_2025.csv` | Export aus dem Lernsystem – **absichtlich unordentlich** (Windows-1252, Semikolon) |
| `2-Anreicherung` | `dim_mitarbeitende.csv` · `dim_bereich.csv` · `dim_kurs.csv` | HR-Stamm (pseudonymisiert), Bereiche, Kurskatalog |
| `3-Ziele` | `ziele_2025.xlsx` (+ CSV-Fassungen) | Budget je Quartal und Zielwerte als Kreuztabellen – zum Entpivotieren |
| | `kontrollzahlen.json` | alle Zahlen aus der Anleitung |

**In Power BI laden:** Daten abrufen → **Web** → Anonym → Adresse + Unterordner + Dateiname:
```
https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/03-Fall-Weiterbildung/Daten/
```
z. B. `…/Daten/1-Rohdaten/weiterbildung_buchungen_2025.csv`.

Zurück zur [Anleitung](../README.md).
