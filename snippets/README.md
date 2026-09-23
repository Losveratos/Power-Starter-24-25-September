# Snippets · zum Kopieren und Weitergeben

Hier landet alles, was im Training oder danach geteilt wird: Power-Query-Code, DAX-Measures,
kleine Vorlagen. Jede Datei ist für sich lauffähig und oben kommentiert (wofür, wo einfügen).

## Inhalt

| Datei | Was | Wo einfügen |
|---|---|---|
| [`powerquery/tag1_verkaeufe_bereinigen.pq`](powerquery/tag1_verkaeufe_bereinigen.pq) | Lösung Tag 1: Kassen-Export komplett aufräumen | Power Query → Leere Abfrage → Erweiterter Editor |
| [`powerquery/tag2_csv_von_github.pq`](powerquery/tag2_csv_von_github.pq) | CSV aus diesem Repo mit richtigen Typen laden | dito |
| [`powerquery/kalender.pq`](powerquery/kalender.pq) | Kalendertabelle 2025 in M | dito |
| [`powerquery/plan_entpivotieren.pq`](powerquery/plan_entpivotieren.pq) | Excel-Kreuztabelle → lange Tabelle | dito |
| [`dax/measures_tag2.dax`](dax/measures_tag2.dax) | alle Measures aus Tag 2 | Modellierung → Neues Measure (je Measure einzeln) |
| [`dax/kalender_dax.dax`](dax/kalender_dax.dax) | Kalender als berechnete DAX-Tabelle | Modellierung → Neue Tabelle |

## So kopierst du ein Snippet
Datei anklicken → oben rechts **Copy raw file** (📋) → in Power BI einfügen.

## Neues Snippet ablegen (für Trainer:innen)
- **Power Query** → `snippets/powerquery/<thema>.pq` · **DAX** → `snippets/dax/<thema>.dax`
- Sonstiges (Theme-JSON, Excel-Vorlage, Screenshot) → `snippets/sonstiges/`
- Für eine bestimmte Person oder Gruppe → `snippets/fuer/<name-oder-firma>/`
- Erste Zeilen immer: `// Wofür · Wo einfügen · Voraussetzungen`
- Dateinamen klein, ohne Leerzeichen und Umlaute (`umsatz_vorjahr.dax`, nicht `Umsatz Vorjahr.dax`)
- Datei hier in der Tabelle eintragen, damit man sie findet

Direkt im Browser geht das auf GitHub mit **Add file → Upload files** oder **Create new file**.
