# Agenda · Power BI Starter-Training · 24.–25. September

> Zeiten sind ein Vorschlag (9:00–16:30). Jeder Block = kurzer Input, dann Hands-on mit der
> passenden Übung. Die Übungen haben Kontrollzahlen – wer schneller ist, macht die ⭐-Extras.

**Voraussetzungen:** Windows-Laptop mit **Power BI Desktop** (aktuelle Version), Internetzugang
(die Daten kommen direkt aus diesem Repo). Kein Power-BI-Konto nötig – außer für die Demo am Ende von Tag 2.

---

## Tag 1 · Donnerstag, 24.09. — Vom Kassen-Export zum ersten Bericht

| Zeit | Block | Inhalt | Übung |
|---|---|---|---|
| 09:00 | **Start** | Vorstellung, Erwartungen, Setup-Check an jedem Rechner | [Ü0](../01-Tag-1/README.md#übung-0--power-bi-desktop-installieren-15-min) |
| 09:30 | **Was ist Power BI?** | Desktop · Service · Mobile · Gateway in einem Bild; der Weg *Laden → Transformieren → Modellieren → Visualisieren → Teilen* | – |
| 10:00 | **Daten anbinden** | Konnektoren, Web vs. Datei, Anmeldung „Anonym", was die Vorschau zeigt | [Ü1](../01-Tag-1/README.md#übung-1--daten-anbinden-15-min) |
| 10:30 | *Pause* | | |
| 10:45 | **Power Query** | Angewendete Schritte = Rezept · Datentypen & Gebietsschema · 5 typische Export-Probleme | [Ü2](../01-Tag-1/README.md#übung-2--aufräumen-in-power-query-35-min) |
| 12:00 | *Mittag* | | |
| 13:00 | **Erste Visuals** | Karte, Balken, Linie · Dimension vs. Kennzahl · Datumshierarchie | [Ü3](../01-Tag-1/README.md#übung-3--erste-antworten-wie-viel-wo-wann-30-min) |
| 13:45 | **Interaktion** | Datenschnitt, Kreuzfilterung, „jedes Visual ist ein Filter" | [Ü4](../01-Tag-1/README.md#übung-4--filtern-15-min) |
| 14:15 | *Pause* | | |
| 14:30 | **Die Aggregations-Falle** | Summe vs. Mittelwert · warum beides bei Quoten falsch sein kann · die Köln-Story | [Ü5](../01-Tag-1/README.md#übung-5--nicht-jede-zahl-darf-man-addieren-25-min) |
| 15:15 | **Fertig machen** | Titel, Raster, Seitennamen, Speichern, PDF | [Ü6](../01-Tag-1/README.md#übung-6--fertig-machen-15-min) |
| 15:45 | **Reflexion** | Was war schwer? Eigene Datenquellen der Teilnehmenden: was davon passt, was nicht? | – |
| 16:15 | **Ausblick & Ende** | Cliffhanger: 44,9 % vs. 32,0 % – morgen lösen wir das | – |

⭐ **Extras für Schnelle:** Exkurs *Entpivotieren* mit [`plan_2025_kreuztabelle.csv`](../02-Tag-2/Daten/plan_2025_kreuztabelle.csv) · Karte „Anzahl Belege" · Balken nach Kategorie mit Datenschnitt Filiale.

---

## Tag 2 · Freitag, 25.09. — Vom Datenmodell zur Kennzahl

| Zeit | Block | Inhalt | Übung |
|---|---|---|---|
| 09:00 | **Recap** | Fragen von gestern · „Menschen lesen Kreuztabellen, Maschinen lange Tabellen" | – |
| 09:20 | **Warum mehrere Tabellen?** | Fakten vs. Dimensionen · Schlüssel · Datentyp-Falle PLZ | [Ü7](../02-Tag-2/README.md#übung-7--vier-tabellen-laden-30-min) |
| 10:00 | **Sternschema** | Beziehungen n:1, Filterrichtung, „immer genau ein Weg" | [Ü8](../02-Tag-2/README.md#übung-8--beziehungen--das-sternschema-25-min) |
| 10:30 | *Pause* | | |
| 10:45 | **Kalendertabelle** | Auto Date/Time aus · Kalender in M · als Datumstabelle markieren · Sortieren nach Spalte | [Ü9](../02-Tag-2/README.md#übung-9--kalendertabelle-20-min) |
| 11:15 | **DAX I: Measures** | Implizit vs. explizit · `SUM`, `SUMX`, `RELATED`, `DIVIDE` · Formatierung · Measure-Tabelle | [Ü10](../02-Tag-2/README.md#übung-10--measures-statt-autosumme-45-min) (1–4) |
| 12:15 | *Mittag* | | |
| 13:15 | **DAX II: Filterkontext** | `CALCULATE` · Anteil am Gesamt · `DATESYTD` · die Köln-Frage, diesmal richtig | [Ü10](../02-Tag-2/README.md#übung-10--measures-statt-autosumme-45-min) (5–6) |
| 14:15 | *Pause* | | |
| 14:30 | **Plan-Ist** | Excel-Kreuztabelle entpivotieren · zweite Faktentabelle · Granularität | [Ü11](../02-Tag-2/README.md#übung-11--plan-ist-aus-einer-excel-kreuztabelle-35-min) |
| 15:15 | **Teilen** | Veröffentlichen, Workspace, App, Aktualisierung, Gateway, Lizenzen (Demo) | [Ü12](../02-Tag-2/README.md#übung-12--teilen--was-nach-dem-desktop-kommt-lesen-20-min) |
| 15:45 | **Wie geht's weiter?** | Checkliste · [Videoempfehlungen](Videos.md) · [Claude-Skills](Claude-Skills.md) für den eigenen Report · eigene Projektideen | – |
| 16:15 | **Feedback & Ende** | | |

⭐ **Extras für Schnelle:** `Umsatz Vormonat` und `Δ Vormonat %` · Top-5-Produkte nach Deckungsbeitrag · Tooltip-Seite mit Marge je Kategorie · Datenschnitt `Segment` (Privat/Gewerbe).
