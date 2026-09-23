# Tag 2 · Vom Datenmodell zur Kennzahl

Gestern hattest du **eine** Tabelle – und am Ende eine falsche Marge (44,9 % statt 32,0 %).
Heute bauen wir es so, wie echte Projekte gebaut werden: **mehrere Tabellen, ein Sternschema,
eine Kalendertabelle, Measures in DAX** – und zum Schluss ein **Plan-Ist-Vergleich** aus einer Excel-Kreuztabelle.

Gleiche Firma, gleiche Verkäufe – nur so, wie sie im Warenwirtschaftssystem wirklich liegen:

| Datei | Was | Zeilen |
|---|---|---|
| [`fakt_verkaeufe.csv`](../daten/tag2/fakt_verkaeufe.csv) | ein Beleg je Zeile: Datum, Filiale, Produkt, Kunde, Menge, Rabatt | 2.877 |
| [`dim_produkt.csv`](../daten/tag2/dim_produkt.csv) | Produkt, Kategorie, Listenpreis, Einstandspreis | 18 |
| [`dim_kunde.csv`](../daten/tag2/dim_kunde.csv) | Kunde, Segment (Privat/Gewerbe), PLZ, Ort | 161 |
| [`dim_filiale.csv`](../daten/tag2/dim_filiale.csv) | Filiale, Bundesland, Eröffnung, Fläche | 4 |
| [`plan_2025.xlsx`](../daten/tag2/plan_2025.xlsx) | Umsatzplan: Filialen × Monate (Kreuztabelle!) | 4 |

Basis-URL für **Daten abrufen → Web**:
```
https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/daten/tag2/
```
…plus Dateiname, z. B. `…/daten/tag2/fakt_verkaeufe.csv`.

---

## Übung 7 · Vier Tabellen laden (25 min)

1. Neue, leere Datei. **Zuerst:** **Datei → Optionen → Aktuelle Datei → Datenladevorgang → „Automatisches Datum/Uhrzeit" aus.** (Wir bauen gleich eine eigene Kalendertabelle.)
2. Die vier CSVs laden (je **Daten abrufen → Web**, Anonym). Jeweils **Daten transformieren**.
3. Abfragen genau so nennen wie die Dateien: `fakt_verkaeufe`, `dim_produkt`, `dim_kunde`, `dim_filiale`.
4. Datentypen prüfen – IDs sind **Text**, Preise und Rabatt mit **Gebietsschema Englisch (USA)**.
5. **Die Falle:** In `dim_kunde` hat Power BI die **PLZ** vermutlich als Zahl erkannt. Aus `04109` (Leipzig) wird `4109`. PLZ ist ein Schlüssel, keine Zahl zum Rechnen → auf **Text** stellen.

Abkürzung: fertiger M-Code in [`snippets/powerquery/tag2_csv_von_github.pq`](../snippets/powerquery/tag2_csv_von_github.pq).

**✅ Kontrollpunkt:** In der Tabellenansicht: `fakt_verkaeufe` **2.877**, `dim_kunde` **161**, `dim_produkt` **18**, `dim_filiale` **4** Zeilen. Die PLZ der Leipziger Kunden beginnt mit **0**.

---

## Übung 8 · Beziehungen – das Sternschema (25 min)

Modellansicht (drittes Symbol links). Power BI hat vielleicht schon Linien gezogen – prüf sie, lösch falsche.

| Von (n-Seite) | Nach (1-Seite) |
|---|---|
| `fakt_verkaeufe[ProduktID]` | `dim_produkt[ProduktID]` |
| `fakt_verkaeufe[KundeID]` | `dim_kunde[KundeID]` |
| `fakt_verkaeufe[FilialeID]` | `dim_filiale[FilialeID]` |

Jede Beziehung: **n:1**, Kreuzfilterrichtung **Einfach**. Ordne die Tabellen als Stern an: Fakt in die Mitte, Dimensionen außen herum.

> `dim_kunde[StammFilialeID]` bekommt **keine** Beziehung – sonst gäbe es zwei Wege von Filiale zu Fakt. Merksatz: *Filter fließen von der 1- zur n-Seite, und es gibt immer genau einen Weg.*

Test: Tabelle-Visual mit `dim_produkt[Kategorie]` und `fakt_verkaeufe[Menge]` (Summe).

**✅ Kontrollpunkt:** Zubehör **2.286**, Werkstatt **677**, Bekleidung **567**, Fahrräder **436**, E-Bikes **249** · Gesamt **4.215**.

Steht überall 4.215? → Die Beziehung Produkt → Fakt fehlt oder zeigt in die falsche Richtung.

---

## Übung 9 · Kalendertabelle (20 min)

1. **Start → Neue Quelle → Leere Abfrage → Erweiterter Editor** → Inhalt von [`snippets/powerquery/kalender.pq`](../snippets/powerquery/kalender.pq) einfügen. Abfrage `Kalender` nennen. **Schließen & übernehmen.**
2. Tabelle `Kalender` markieren → **Tabellentools → Als Datumstabelle markieren** → Spalte `Datum`.
3. Beziehung: `fakt_verkaeufe[Belegdatum]` → `Kalender[Datum]` (n:1).
4. Spalte `Monat` markieren → **Spaltentools → Nach Spalte sortieren → MonatNr**. (Sonst steht *Apr* vor *Jan*.)
5. Dasselbe für `Wochentag` → nach `WochentagNr`.

**✅ Kontrollpunkt:** `Kalender` hat **365** Zeilen. Ein Säulendiagramm *Kalender[Monat]* × *Menge* zeigt die Monate in der Reihenfolge Jan → Dez.

---

## Übung 10 · Measures statt Autosumme (45 min)

Gestern hat Power BI selbst entschieden, wie es rechnet (Summe, dann Mittelwert). Ab jetzt entscheidest du: mit **Measures**.

1. **Start → Daten eingeben** → leere Tabelle `_Measures` → **Laden**. Hier landen alle Measures.
2. Tabelle `_Measures` markieren → **Neues Measure**. Nacheinander (Vorlagen in [`snippets/dax/measures_tag2.dax`](../snippets/dax/measures_tag2.dax)):

```dax
Umsatz =
SUMX (
    fakt_verkaeufe,
    fakt_verkaeufe[Menge] * RELATED ( dim_produkt[Listenpreis] ) * ( 1 - fakt_verkaeufe[Rabatt] )
)

Kosten = SUMX ( fakt_verkaeufe, fakt_verkaeufe[Menge] * RELATED ( dim_produkt[Einstandspreis] ) )

Deckungsbeitrag = [Umsatz] - [Kosten]

Marge % = DIVIDE ( [Deckungsbeitrag], [Umsatz] )
```

3. Formatieren: `Umsatz`, `Kosten`, `Deckungsbeitrag` → Währung, 0 Nachkommastellen; `Marge %` → Prozent, 1 Nachkommastelle.
4. **Matrix**: Zeilen `dim_filiale[Filiale]`, Werte `Umsatz`, `Marge %`.

**✅ Kontrollpunkt:**

| Filiale | Umsatz | Marge % |
|---|---:|---:|
| Hamburg | 371.601 € | 33,1 % |
| Köln | 276.562 € | **26,0 %** |
| München | 411.511 € | 34,3 % |
| Leipzig | 184.344 € | 33,3 % |
| **Gesamt** | **1.244.018 €** | **32,0 %** |

> **Warum 1.244.017,93 € und nicht 1.244.017,12 € wie gestern?** Das Kassensystem hat jeden Beleg
> auf Cent gerundet, SUMX rechnet ungerundet. 81 Cent Differenz über 2.877 Belege – so sieht ein
> echter Abgleich zwischen zwei Systemen aus. Gut, dass du sie gefunden hast, bevor der Controller es tut.

5. Mehr Measures – jeweils mit Kontrollzahl:

| Measure | Formel (Kurzform) | ✅ Gesamt |
|---|---|---:|
| `Belege` | `COUNTROWS ( fakt_verkaeufe )` | 2.877 |
| `Kunden aktiv` | `DISTINCTCOUNT ( fakt_verkaeufe[KundeID] )` | 161 |
| `Ø Bon` | `DIVIDE ( [Umsatz], [Belege] )` | 432,40 € |
| `Umsatz E-Bikes` | `CALCULATE ( [Umsatz], dim_produkt[Kategorie] = "E-Bikes" )` | 724.796,87 € |
| `Umsatz kumuliert` | `CALCULATE ( [Umsatz], DATESYTD ( Kalender[Datum] ) )` | im Juni: 640.448,56 € |

6. **Die Köln-Frage, jetzt richtig:** Liniendiagramm `Kalender[Monat]` × `Marge %`, Legende `dim_filiale[Filiale]`.

**✅ Kontrollpunkt:** Köln Jan–Mai **33,3 %**, Jun–Dez **20,6 %**. Mit Datenschnitt `dim_kunde[Segment]`: Gewerbe **29,7 %**, Privat **32,5 %**.

> **Merksatz:** Eine Quote ist nie der Durchschnitt von Quoten. *Summe oben ÷ Summe unten* – als Measure mit `DIVIDE`.

---

## Übung 11 · Plan-Ist aus einer Excel-Kreuztabelle (35 min)

Das Controlling liefert den Plan als Excel: **Filialen in Zeilen, Monate in Spalten**, oben ein Titel, rechts eine Summenspalte. Für Menschen perfekt, für Power BI unbrauchbar.

1. **Daten abrufen → Web** → `…/daten/tag2/plan_2025.xlsx` → Blatt **Plan 2025** → **Daten transformieren**.
   Rechts unter *Angewendete Schritte* alles nach **Navigation** löschen (Power BI hat sonst schon die Titelzeile zur Überschrift gemacht).
2. **Obere Zeilen entfernen** → `2` (Titel + Leerzeile). **Erste Zeile als Überschriften verwenden**.
3. Spalte **Gesamt** entfernen – Summen rechnet Power BI selbst.
4. Spalte **Filiale** markieren → **Transformieren → Spalten entpivotieren → Andere Spalten entpivotieren**. Aus 4 Zeilen × 12 Monatsspalten werden **48 Zeilen** mit *Attribut* (Monat) und *Wert*.
5. Umbenennen: *Attribut* → `Monat`, *Wert* → `Plan`. `Plan` als Währung.
6. Aus dem Monatsnamen ein Datum machen: **Spalte hinzufügen → Benutzerdefinierte Spalte** `Monatsanfang`:
   ```
   #date(2025, List.PositionOf({"Jan","Feb","Mär","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"}, [Monat]) + 1, 1)
   ```
   Typ **Datum**. Abfrage `Plan` nennen. (Komplett: [`snippets/powerquery/plan_entpivotieren.pq`](../snippets/powerquery/plan_entpivotieren.pq))
7. Beziehungen: `Plan[Filiale]` → `dim_filiale[Filiale]` und `Plan[Monatsanfang]` → `Kalender[Datum]` (beide n:1).
8. Measures:
   ```dax
   Plan = SUM ( Plan[Plan] )
   Δ Plan = [Umsatz] - [Plan]
   Δ Plan % = DIVIDE ( [Δ Plan], [Plan] )
   ```

**✅ Kontrollpunkt:**

| Filiale | Plan | Δ Plan |
|---|---:|---:|
| Hamburg | 389.000 € | −17.399 € |
| Köln | 282.000 € | −5.438 € |
| München | 422.000 € | −10.489 € |
| Leipzig | 195.000 € | −10.656 € |
| **Gesamt** | **1.288.000 €** | **−43.982 € (−3,4 %)** |

> **Schau genauer hin:** Köln verfehlt den Plan am wenigsten – dank Rabattaktion. Plan-Ist allein
> hätte Köln gelobt. Erst `Marge %` daneben zeigt, dass der Umsatz teuer gekauft ist.
> Genau dafür baut man Berichte mit mehr als einer Kennzahl.

> Der Plan liegt auf **Monatsebene**. Zeig ihn deshalb nie nach Tag oder Wochentag – dort wäre er
> falsch verteilt. Das ist der Klassiker „unterschiedliche Granularität".

---

## Übung 12 · Teilen – was nach dem Desktop kommt (Demo, 30 min)

Keine Übung am eigenen Rechner (dafür braucht es ein Geschäftskonto mit Lizenz), sondern gemeinsam:

- **Veröffentlichen** → Workspace im Power BI Service
- **Semantikmodell vs. Bericht** – was liegt wo?
- **Aktualisierung planen** – und wann ein **Gateway** nötig ist (lokale Dateien/Datenbanken; bei unseren GitHub-URLs nicht)
- **App** aus dem Workspace statt Links auf einzelne Berichte
- **Lizenzen in einem Satz:** Desktop ist kostenlos · Teilen braucht Pro (oder Premium/Fabric-Kapazität für die Leser)

### Checkliste, bevor du etwas veröffentlichst

- [ ] Automatisches Datum/Uhrzeit aus, eigene Kalendertabelle markiert
- [ ] Sternschema, alle Beziehungen n:1 und einfach
- [ ] Jede Kennzahl ist ein Measure – keine impliziten Summen auf der Seite
- [ ] Quoten mit `DIVIDE` aus Summen, nie als Mittelwert
- [ ] Hilfsspalten (IDs, Sortierspalten) in der Berichtsansicht ausgeblendet
- [ ] Jede Zahl gegen eine Kontrollzahl geprüft

---

### Glossar Tag 2

| Wort | In einem Satz |
|---|---|
| Faktentabelle | Die Tabelle mit den Ereignissen (Belege) – lang, schmal, mit Schlüsseln und Mengen. |
| Dimensionstabelle | Beschreibt ein Ding (Produkt, Kunde, Filiale) – je Schlüssel genau eine Zeile. |
| Sternschema | Fakt in der Mitte, Dimensionen außen, jede Beziehung n:1. |
| Beziehung | Verbindet zwei Tabellen über einen Schlüssel; Filter fließen von 1 nach n. |
| Measure | Eine benannte Rechenregel in DAX, die im aktuellen Filter ausgewertet wird. |
| Filterkontext | Alles, was gerade filtert: Zeile der Matrix, Datenschnitt, Klick im Visual. |
| `CALCULATE` | Rechnet ein Measure mit verändertem Filterkontext. |
| Entpivotieren | Macht aus einer breiten Kreuztabelle eine lange Tabelle. |
| Granularität | Die Detailstufe einer Tabelle (Beleg je Tag vs. Plan je Monat). |
