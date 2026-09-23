# Handout · Power BI Starter

*Zwei Seiten zum Mitnehmen. Ausführlich: [Einsteiger-Guide](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html).*

---

## 1 · Das große Bild

```
 Quelle            Power Query          Modell               Bericht              Service
 (CSV, Excel,  →   aufräumen,      →    Tabellen,       →    Visuals,        →    teilen,
  Datenbank)       Typen setzen         Beziehungen,         Filter,              aktualisieren
                   (Sprache: M)         Measures (DAX)       Seiten               (Workspace, App)
 └──────────────── Power BI Desktop (kostenlos, Windows) ────────────────┘   └ braucht Lizenz ┘
```

| Teil | Wofür | Merksatz |
|---|---|---|
| **Power BI Desktop** | Bauen | Kostenlos, nur Windows, monatliches Update installieren |
| **Power BI Service** | Teilen & aktualisieren | Browser; Veröffentlichen braucht ein Geschäftskonto + Pro/PPU oder Fabric-Kapazität |
| **Gateway** | Service ↔ lokale Daten | Nur nötig, wenn Daten hinter der Firewall liegen (Dateiserver, lokale DB) |

---

## 2 · Power Query – die fünf Export-Probleme

| Problem | Handgriff |
|---|---|
| Müllzeilen oben | Zeilen entfernen → Obere Zeilen entfernen |
| Keine Überschriften | Erste Zeile als Überschriften verwenden |
| Leere Zeilen | Zeilen entfernen → Leere Zeilen entfernen |
| Leerzeichen / Schreibweise | Transformieren → Format → Kürzen / Jedes Wort großschreiben |
| Zahlen & Datum falsch gelesen | Rechtsklick → Typ ändern → **Gebietsschema verwenden…** (Punkt als Dezimalzeichen → *Englisch (USA)*) |

**Regeln:**
- Die *Angewendeten Schritte* sind ein **Rezept**, kein Protokoll. Sie laufen bei jeder Aktualisierung neu.
- **Datentypen früh und bewusst setzen.** IDs, PLZ, Artikelnummern sind **Text**.
- Automatische Schritte (*Geänderter Typ*) nicht blind übernehmen.
- **Menschen lesen Kreuztabellen, Maschinen lange Tabellen.** Monate als Spalten → *Andere Spalten entpivotieren*.

---

## 3 · Das Modell – Sternschema

```
            dim_produkt
                 │ 1
                 │
 dim_kunde ─1──n─ fakt_verkaeufe ─n──1─ dim_filiale
                 │ n
                 │
               1 Kalender
```

- **Fakt** = Ereignisse (Belege, Buchungen): lang, Schlüssel + Zahlen.
- **Dimension** = beschreibt ein Ding: je Schlüssel **genau eine** Zeile.
- Beziehungen **n:1**, Filterrichtung **einfach**. Von jeder Dimension genau **ein** Weg zum Fakt.
- **Eigene Kalendertabelle**, als Datumstabelle markiert. *Automatisches Datum/Uhrzeit* **aus**.
- Textspalten wie *Monat* über **Nach Spalte sortieren** an eine Zahl (*MonatNr*) hängen.

---

## 4 · DAX – die ersten zehn Funktionen

| Funktion | Wofür | Beispiel |
|---|---|---|
| `SUM` | Spalte summieren | `Menge = SUM ( fakt[Menge] )` |
| `SUMX` | Zeile für Zeile rechnen, dann summieren | `SUMX ( fakt, fakt[Menge] * RELATED ( dim_produkt[Preis] ) )` |
| `RELATED` | Wert aus der 1-Seite holen | siehe oben |
| `COUNTROWS` | Zeilen zählen | `Belege = COUNTROWS ( fakt )` |
| `DISTINCTCOUNT` | Verschiedene zählen | `Kunden = DISTINCTCOUNT ( fakt[KundeID] )` |
| `DIVIDE` | Teilen ohne Fehler bei 0 | `Marge % = DIVIDE ( [DB], [Umsatz] )` |
| `CALCULATE` | Measure mit geändertem Filter | `CALCULATE ( [Umsatz], dim_produkt[Kategorie] = "E-Bikes" )` |
| `ALL` / `ALLSELECTED` | Filter entfernen | `DIVIDE ( [Umsatz], CALCULATE ( [Umsatz], ALLSELECTED ( dim_filiale ) ) )` |
| `DATESYTD` | Jahr bis heute | `CALCULATE ( [Umsatz], DATESYTD ( Kalender[Datum] ) )` |
| `DATEADD` | Zeitraum verschieben | `CALCULATE ( [Umsatz], DATEADD ( Kalender[Datum], -1, MONTH ) )` |

**Regeln:**
- **Jede Zahl auf der Seite ist ein Measure.** Keine Spalte direkt ins Visual ziehen.
- **Quoten = Summe ÷ Summe**, nie Mittelwert von Quoten. (Tag 1: 44,9 % ✗ · Tag 2: 32,0 % ✓)
- Measures in eine eigene Tabelle `_Measures`, sofort formatieren.
- **Filterkontext:** Ein Measure wird für jede Zelle neu gerechnet – mit allem, was dort gerade filtert.

---

## 5 · Bericht – Handwerk

- Eine Seite beantwortet **eine Frage**. Titel = die Frage oder die Antwort.
- Oben links das Wichtigste (Leserichtung). Karten → Überblick, Balken → Vergleich, Linie → Zeitverlauf.
- **Balken sortieren**, Achsen bei 0 beginnen lassen, Farbe sparsam – eine Akzentfarbe für „schau hier".
- Jedes Visual filtert die anderen – **Interaktionen bearbeiten**, wenn das stört.
- Vor dem Teilen: **jede Zahl gegen eine Kontrollzahl** prüfen.

---

## 6 · Tastenkürzel & Handgriffe

| Was | Wie |
|---|---|
| Visual duplizieren | `Strg + C`, `Strg + V` |
| Mehrere Visuals ausrichten | `Strg` + Klick → Format → Ausrichten |
| Measure-Formel umbrechen | `Umschalt + Enter` in der Bearbeitungsleiste |
| Formel kommentieren / formatieren | `//` am Zeilenanfang · [daxformatter.com](https://www.daxformatter.com/) |
| Wert im Visual prüfen | Rechtsklick → *Als Tabelle anzeigen* |
| Abfrage neu laden | Power Query → Rechtsklick auf Abfrage → *Vorschau aktualisieren* |

---

## 7 · Glossar

| Wort | In einem Satz |
|---|---|
| Transformation | Ein Handgriff in Power Query; die Quelle bleibt unverändert. |
| Gebietsschema | Sagt Power BI, wie Zahlen/Datumswerte in der Quelle geschrieben sind. |
| Visual | Ein einzelnes Bild auf der Seite. |
| Dimension / Kennzahl | Wonach du aufteilst / was du misst. |
| Aggregation | Wie viele Zeilen zu einer Zahl werden (Summe, Mittelwert, Anzahl …). |
| Fakt / Dimension (Tabelle) | Ereignisse / Beschreibungen. |
| Beziehung | Verbindet Tabellen über Schlüssel; Filter fließen von 1 nach n. |
| Measure | Benannte DAX-Rechenregel, im aktuellen Filterkontext ausgewertet. |
| Filterkontext | Alles, was eine Zelle gerade filtert. |
| Granularität | Detailstufe einer Tabelle (Tag vs. Monat). |
| Semantikmodell | Das veröffentlichte Modell im Service (früher „Dataset"). |
| Workspace / App | Arbeitsbereich zum Bauen / verpacktes Paket zum Konsumieren. |

---

## 8 · Zum Nachschlagen

| Thema | Knowledge Kitchen (deutsch, praxisnah) | Microsoft Learn (offizielle Doku) |
|---|---|---|
| Erste Schritte | [Praxis-Pfad: Dein erstes Dashboard](https://datenwgknowledgekitchen.com/powerbi_praxis_pfad.html) | [Erste Schritte mit Power BI Desktop](https://learn.microsoft.com/de-de/power-bi/fundamentals/desktop-getting-started) |
| Power Query | [Einsteiger-Guide · Power Query](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#pq) | [Datentypen und Gebietsschema](https://learn.microsoft.com/de-de/power-query/data-types) · [Spalten entpivotieren](https://learn.microsoft.com/de-de/power-query/unpivot-column) |
| Datenmodell | [Einsteiger-Guide · Datenmodellierung](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#model) | [Sternschema](https://learn.microsoft.com/de-de/power-bi/guidance/star-schema) · [Datumstabellen](https://learn.microsoft.com/de-de/power-bi/transform-model/desktop-date-tables) |
| DAX | [Einsteiger-Guide · DAX](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#dax) | [Measures erstellen (Tutorial)](https://learn.microsoft.com/de-de/power-bi/transform-model/desktop-tutorial-create-measures) · [DAX-Übersicht](https://learn.microsoft.com/de-de/dax/dax-overview) |
| Visualisierung | [Einsteiger-Guide · Visualisierung & IBCS](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#viz) | [Überblick über Visualisierungen](https://learn.microsoft.com/de-de/power-bi/visuals/power-bi-visualizations-overview) |
| Teilen | [Einsteiger-Guide · Service & Sharing](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#service) | [Aus Desktop veröffentlichen](https://learn.microsoft.com/de-de/power-bi/create-reports/desktop-upload-desktop-files) |

