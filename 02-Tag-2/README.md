# Tag 2 · Vom Datenmodell zur Kennzahl

An Tag 1 hattest du **eine** Tabelle – und am Ende eine Marge von 44,9 %, die nicht stimmt (richtig sind 32,0 %).
Heute baust du es so, wie echte Projekte gebaut werden: **mehrere Tabellen, ein Sternschema,
eine Kalendertabelle, Measures in DAX** – und zum Schluss einen **Plan-Ist-Vergleich** aus einer Excel-Kreuztabelle.

> ⬇️ **Lieber offline arbeiten?** [Dieses Übungsblatt als PDF mit Daten und Lösungen (ZIP)](https://github.com/Losveratos/Power-Starter-24-25-September/raw/main/00-Downloads/Starter-Training-Tag2.zip)

---

## Bevor du anfängst

**Du brauchst:** Power BI Desktop (siehe [Tag 1, Übung 0](../01-Tag-1/README.md#übung-0--power-bi-desktop-installieren-15-min)),
Internet, etwa **4 Stunden**. Tag 1 musst du nicht gemacht haben – aber du solltest wissen, wie man
*Daten abrufen*, den *Power Query-Editor* und die *Berichtsansicht* bedient. Unsicher? Mach vorher [Tag 1](../01-Tag-1/).

**Zeichen wie an Tag 1:** ✅ Kontrollpunkt · 🆘 Hängst du fest? · 📚 Mehr dazu (Knowledge Kitchen + Microsoft Learn).
Zwischendurch speichern: **Strg + S**.

**Die Daten:** dieselben Verkäufe wie an Tag 1 – diesmal so, wie sie im Warenwirtschaftssystem wirklich liegen:

| Datei | Was | Zeilen |
|---|---|---|
| [`fakt_verkaeufe.csv`](Daten/fakt_verkaeufe.csv) | ein Beleg je Zeile: Datum, Filiale, Produkt, Kunde, Menge, Rabatt | 2.877 |
| [`dim_produkt.csv`](Daten/dim_produkt.csv) | Produkt, Kategorie, Listenpreis, Einstandspreis | 18 |
| [`dim_kunde.csv`](Daten/dim_kunde.csv) | Kunde, Segment (Privat/Gewerbe), PLZ, Ort | 161 |
| [`dim_filiale.csv`](Daten/dim_filiale.csv) | Filiale, Bundesland, Eröffnung, Fläche | 4 |
| [`plan_2025.xlsx`](Daten/plan_2025.xlsx) | Umsatzplan: Filialen × Monate (Kreuztabelle!) | 4 |

Alle Adressen beginnen mit
```
https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/02-Tag-2/Daten/
```
…dahinter der Dateiname, z. B. `…/02-Tag-2/Daten/fakt_verkaeufe.csv`.

---

## Übung 7 · Vier Tabellen laden (30 min)

1. Power BI Desktop öffnen → **Datei → Neu** (leerer Bericht).
2. **Zuerst eine Einstellung:** **Datei → Optionen und Einstellungen → Optionen** → links unter **Aktuelle Datei** auf **Datenladevorgang** →
   Häkchen bei **Automatisches Datum/Uhrzeit** entfernen → **OK**. *(Wir bauen gleich eine eigene Kalendertabelle – die ist besser.)*
3. Für **jede** der vier CSV-Dateien einmal:
   1. **Start → Daten abrufen → Web** → Adresse + Dateiname einfügen → **OK** → **Anonym** → **Verbinden**.
   2. In der Vorschau **Daten transformieren** klicken.
   3. Rechts unter **Angewendete Schritte** den Schritt **Geänderter Typ** per **X** löschen (*Höher gestufte Header* bleibt!).
   4. Datentypen setzen wie in der Tabelle unten. **„Mit Gebietsschema"** heißt: Rechtsklick auf die Überschrift → **Typ ändern → Gebietsschema verwenden…** → Typ wählen, Gebietsschema **Englisch (USA)** → **OK**.
      Alle anderen: auf das Symbol links in der Überschrift klicken und den Typ wählen.
   5. Die Abfrage muss so heißen wie die Datei (links in der Liste **Abfragen**). Wenn nicht: Rechtsklick → **Umbenennen**.
4. Wenn alle vier geladen sind: **Start → Schließen & übernehmen**.

| Abfrage | Spalte | Typ |
|---|---|---|
| `fakt_verkaeufe` | Belegnummer, FilialeID, ProduktID, KundeID | Text |
| | Belegdatum | Datum |
| | Menge | Ganze Zahl |
| | **Rabatt** | Dezimalzahl **mit Gebietsschema** |
| `dim_produkt` | ProduktID, Produkt, Kategorie | Text |
| | **Listenpreis, Einstandspreis** | Dezimalzahl **mit Gebietsschema** |
| `dim_kunde` | alle Spalten, **auch PLZ** | Text |
| `dim_filiale` | FilialeID, Filiale, Bundesland | Text |
| | Eroeffnet | Datum |
| | Verkaufsflaeche_m2 | Ganze Zahl |

> **Die Falle:** Power BI hält die **PLZ** für eine Zahl – dann wird aus `04109` (Leipzig) die `4109`.
> Eine PLZ ist ein Schlüssel, keine Zahl zum Rechnen → immer **Text**. Dasselbe gilt für Artikel-, Kunden- und Personalnummern.

**✅ Kontrollpunkt:** Links **Tabellenansicht** (Gitter), rechts nacheinander jede Tabelle anklicken, unten steht die Zeilenzahl:
`fakt_verkaeufe` **2.877** · `dim_kunde` **161** · `dim_produkt` **18** · `dim_filiale` **4**.
Die PLZ der Leipziger Kunden beginnt mit **0**, der Rabatt steht als **0,05** (nicht 5), der Listenpreis vom Stadtrad als **649** (nicht 64.900).

🆘 **Hängst du fest?**
- *Rabatt steht als 5 oder 10, Preise sind 100-mal zu groß* → ohne Gebietsschema umgewandelt. **Start → Daten transformieren**, den Typ-Schritt löschen, mit Gebietsschema neu setzen.
- *Abfrage heißt „fakt_verkaeufe (2)"* → doppelt geladen. Die überzählige Abfrage links per Rechtsklick → **Löschen**.
- *Zu mühsam?* → Fertiger Code je Tabelle: [`Tag2_PowerQuery_CSV_laden.pq`](Loesungen/Tag2_PowerQuery_CSV_laden.pq) →
  **Start → Neue Quelle → Leere Abfrage → Erweiterter Editor** → einfügen → Dateiname und Typen laut Kommentar im Code anpassen.

📚 **Mehr dazu:** Kitchen: [Einsteiger-Guide · Power Query](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#pq) ·
Microsoft Learn: [Datentypen und Gebietsschema](https://learn.microsoft.com/de-de/power-query/data-types) ·
[Automatisches Datum/Uhrzeit](https://learn.microsoft.com/de-de/power-bi/transform-model/desktop-auto-date-time)

---

## Übung 8 · Beziehungen – das Sternschema (25 min)

1. Links das **dritte** Symbol: **Modellansicht**. Du siehst die vier Tabellen als Kästen.
2. Power BI hat vielleicht schon Linien gezogen. **Prüf jede Linie:** Doppelklick darauf → das Fenster zeigt, welche Spalten verbunden sind.
   Falsche Linien: anklicken → **Entf**.
3. Fehlende Beziehung anlegen: In `fakt_verkaeufe` das Feld **ProduktID** mit gedrückter Maustaste auf das Feld **ProduktID** in `dim_produkt` ziehen.
   Im Fenster prüfen: **Kardinalität: n:1**, **Kreuzfilterrichtung: Einfach** → **Speichern**/**OK**.
4. Genauso für die anderen beiden:

| Von (n-Seite) | Nach (1-Seite) |
|---|---|
| `fakt_verkaeufe[ProduktID]` | `dim_produkt[ProduktID]` |
| `fakt_verkaeufe[KundeID]` | `dim_kunde[KundeID]` |
| `fakt_verkaeufe[FilialeID]` | `dim_filiale[FilialeID]` |

5. Ordne die Kästen als **Stern** an: `fakt_verkaeufe` in die Mitte, die drei `dim_…` außen herum.

> `dim_kunde[StammFilialeID]` bekommt **keine** Beziehung – sonst gäbe es zwei Wege von Filiale zu Fakt.
> Merksatz: *Filter fließen von der 1- zur n-Seite, und es gibt immer genau einen Weg.*

**Test:** Zurück in die **Berichtsansicht** → **Tabelle** (Visual) → Häkchen bei `dim_produkt` **Kategorie** und bei `fakt_verkaeufe` **Menge**.

**✅ Kontrollpunkt:** Zubehör **2.286** · Werkstatt **677** · Bekleidung **567** · Fahrräder **436** · E-Bikes **249** · Gesamt **4.215**.

🆘 **Hängst du fest?**
- *In jeder Zeile steht 4.215* → Die Beziehung Produkt → Fakt fehlt oder verbindet falsche Spalten. Modellansicht prüfen.
- *Fenster meldet „n:n" (viele zu viele)* → Du hast in die falsche Richtung gezogen oder die Spalte in der `dim_…`-Tabelle ist nicht eindeutig. Abbrechen, von `fakt_…` nach `dim_…` ziehen.
- *Menge zeigt „Anzahl von Menge"* → rechts auf den Pfeil neben dem Feld → **Summe**.

📚 **Mehr dazu:** Kitchen: [Einsteiger-Guide · Datenmodellierung (Sternschema, Modell-Prinzipien)](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#model) ·
Microsoft Learn: [Sternschema](https://learn.microsoft.com/de-de/power-bi/guidance/star-schema) ·
[Beziehungen verstehen](https://learn.microsoft.com/de-de/power-bi/transform-model/desktop-relationships-understand) ·
[Beziehungen erstellen](https://learn.microsoft.com/de-de/power-bi/transform-model/desktop-create-and-manage-relationships)

---

## Übung 9 · Kalendertabelle (20 min)

1. [`Tag2_PowerQuery_Kalender.pq`](Loesungen/Tag2_PowerQuery_Kalender.pq) öffnen → oben rechts **Copy raw file** (📋).
2. In Power BI: **Start → Daten transformieren** → **Start → Neue Quelle → Leere Abfrage** → **Erweiterter Editor** →
   alles markieren und durch den kopierten Code ersetzen → **Fertig**.
3. Links die neue Abfrage per Rechtsklick → **Umbenennen** → `Kalender` → **Start → Schließen & übernehmen**.
4. **Als Datumstabelle markieren:** rechts im Bereich **Daten** auf `Kalender` klicken → oben **Tabellentools → Als Datumstabelle markieren** → Spalte **Datum** → **OK**.
5. **Beziehung:** Modellansicht → `fakt_verkaeufe[Belegdatum]` auf `Kalender[Datum]` ziehen (n:1, Einfach).
6. **Monate richtig sortieren:** Tabellenansicht → `Kalender` → Spalte **Monat** anklicken → **Spaltentools → Nach Spalte sortieren → MonatNr**.
   *(Sonst steht „Apr" vor „Jan" – alphabetisch.)* Dasselbe für **Wochentag** → nach **WochentagNr**.

**✅ Kontrollpunkt:** `Kalender` hat **365** Zeilen. Ein **Gruppiertes Säulendiagramm** mit `Kalender` **Monat** und `fakt_verkaeufe` **Menge** zeigt die Monate in der Reihenfolge **Jan → Dez**.

🆘 **Hängst du fest?**
- *„Als Datumstabelle markieren" ist grau* → Du hast nicht `Kalender` ausgewählt, oder die Spalte **Datum** hat nicht den Typ *Datum*.
- *Monate stehen alphabetisch* → Schritt 6 fehlt. Außerdem im Diagramm: **… → Achse sortieren → Monat** und **Aufsteigend sortieren**.
- *Alle Säulen gleich hoch* → Beziehung aus Schritt 5 fehlt.

📚 **Mehr dazu:** Kitchen: [Einsteiger-Guide · Datums-Dimension (Kalender)](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#model) ·
Microsoft Learn: [Datumstabellen](https://learn.microsoft.com/de-de/power-bi/transform-model/desktop-date-tables) ·
[Nach anderer Spalte sortieren](https://learn.microsoft.com/de-de/power-bi/create-reports/desktop-sort-by-column)

---

## Übung 10 · Measures statt Autosumme (45 min)

An Tag 1 hat Power BI selbst entschieden, wie es rechnet (Summe, dann Mittelwert) – und lag bei der Marge falsch.
Ab jetzt entscheidest du: mit **Measures**. Ein Measure ist eine benannte Rechenregel in der Formelsprache **DAX**.

**Eine Heimat für die Measures**
1. **Start → Daten eingeben** → unten bei **Name** `_Measures` eintragen → **Laden**. Rechts erscheint die Tabelle `_Measures`.

**Das erste Measure**
2. Rechts im Bereich **Daten** auf `_Measures` klicken → oben **Tabellentools → Neues Measure** (oder Rechtsklick auf `_Measures` → **Neues Measure**).
3. Oben erscheint eine **Bearbeitungsleiste** mit `Measure = `. Alles markieren und ersetzen durch:
   ```dax
   Umsatz =
   SUMX (
       fakt_verkaeufe,
       fakt_verkaeufe[Menge] * RELATED ( dim_produkt[Listenpreis] ) * ( 1 - fakt_verkaeufe[Rabatt] )
   )
   ```
   → **Enter** (bzw. das Häkchen links neben der Leiste). Zeilenumbruch in der Leiste: **Umschalt + Enter**.
   *In Worten: Für jeden Beleg Menge × Listenpreis × (1 − Rabatt) rechnen, dann alles addieren.*
4. Genauso drei weitere Measures anlegen (jedes einzeln: **Neues Measure** → einfügen → **Enter**):
   ```dax
   Kosten = SUMX ( fakt_verkaeufe, fakt_verkaeufe[Menge] * RELATED ( dim_produkt[Einstandspreis] ) )
   ```
   ```dax
   Deckungsbeitrag = [Umsatz] - [Kosten]
   ```
   ```dax
   Marge % = DIVIDE ( [Deckungsbeitrag], [Umsatz] )
   ```
5. **Formatieren:** Measure rechts anklicken → oben **Measuretools**:
   `Umsatz`, `Kosten`, `Deckungsbeitrag` → **Währung**, Dezimalstellen **0** · `Marge %` → **%**, Dezimalstellen **1**.
6. **Matrix** (Visual) → Zeilen: `dim_filiale` **Filiale** · Werte: `Umsatz`, `Marge %`.

**✅ Kontrollpunkt:**

| Filiale | Umsatz | Marge % |
|---|---:|---:|
| Hamburg | 371.601 € | 33,1 % |
| Köln | 276.562 € | **26,0 %** |
| München | 411.511 € | 34,3 % |
| Leipzig | 184.344 € | 33,3 % |
| **Gesamt** | **1.244.018 €** | **32,0 %** |

> **Warum 1.244.017,93 € und nicht 1.244.017,12 € wie an Tag 1?** Das Kassensystem hat jeden Beleg
> auf Cent gerundet, SUMX rechnet ungerundet. 81 Cent Differenz über 2.877 Belege – so sieht ein
> echter Abgleich zwischen zwei Systemen aus.

**Mehr Measures** – jeweils mit Kontrollzahl (alle Formeln komplett in [`Tag2_DAX_Measures.dax`](Loesungen/Tag2_DAX_Measures.dax)):

| Measure | Formel | ✅ Gesamt |
|---|---|---:|
| `Belege` | `COUNTROWS ( fakt_verkaeufe )` | 2.877 |
| `Kunden aktiv` | `DISTINCTCOUNT ( fakt_verkaeufe[KundeID] )` | 161 |
| `Ø Bon` | `DIVIDE ( [Umsatz], [Belege] )` | 432,40 € |
| `Umsatz E-Bikes` | `CALCULATE ( [Umsatz], dim_produkt[Kategorie] = "E-Bikes" )` | 724.796,87 € |
| `Umsatz kumuliert` | `CALCULATE ( [Umsatz], DATESYTD ( Kalender[Datum] ) )` | im Juni: 640.448,56 € |

*Für `Umsatz kumuliert` eine Tabelle mit `Kalender` **Monat** und dem Measure bauen – in der Zeile **Jun** steht die Kontrollzahl.*

**Die Köln-Frage, jetzt richtig:** **Liniendiagramm** → X-Achse `Kalender` **Monat** · Y-Achse `Marge %` · Legende `dim_filiale` **Filiale**.

**✅ Kontrollpunkt:** Köln liegt im **Mai** noch bei **32,5 %** und fällt im **Juni** auf **23,7 %** – danach bleibt es um 20 %.
Die anderen drei Filialen bleiben das ganze Jahr bei 30–38 %.
Mit einem **Datenschnitt** auf `dim_kunde` **Segment**: Gewerbe **29,7 %**, Privat **32,5 %** (Gesamt, ohne Filialfilter).

> **Merksatz:** Eine Quote ist nie der Durchschnitt von Quoten. *Summe oben ÷ Summe unten* – als Measure mit `DIVIDE`.

🆘 **Hängst du fest?**
- *Rote Wellenlinie / „Die Spalte … wurde nicht gefunden"* → Tabellen- oder Spaltenname weicht ab. Heißen deine Abfragen genau `fakt_verkaeufe`, `dim_produkt`? (Übung 7, Schritt 3.5)
- *„RELATED: Spalte existiert nicht oder hat keine Beziehung"* → Beziehung Fakt → Produkt fehlt (Übung 8).
- *Umsatz ist 100-mal zu groß oder Marge negativ* → Rabatt oder Preise ohne Gebietsschema geladen (Übung 7).
- *Measure landet in der falschen Tabelle* → Measure anklicken → **Measuretools → Starttabelle** → `_Measures`.
- *`Umsatz kumuliert` zeigt überall dasselbe* → Kalender nicht als Datumstabelle markiert oder ohne Beziehung (Übung 9).

📚 **Mehr dazu:** Kitchen: [Einsteiger-Guide · DAX (Measures vs. berechnete Spalten, CALCULATE, Anti-Patterns)](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#dax) ·
Microsoft Learn: [Eigene Measures erstellen (Tutorial)](https://learn.microsoft.com/de-de/power-bi/transform-model/desktop-tutorial-create-measures) ·
[DAX-Übersicht](https://learn.microsoft.com/de-de/dax/dax-overview) ·
[CALCULATE](https://learn.microsoft.com/de-de/dax/calculate-function-dax) ·
[DIVIDE](https://learn.microsoft.com/de-de/dax/divide-function-dax) ·
[Zeitintelligenz-Funktionen](https://learn.microsoft.com/de-de/dax/time-intelligence-functions-dax)

---

## Übung 11 · Plan-Ist aus einer Excel-Kreuztabelle (35 min)

Das Controlling liefert den Plan als Excel: **Filialen in Zeilen, Monate in Spalten**, oben ein Titel, rechts eine Summenspalte.
Für Menschen perfekt, für Power BI unbrauchbar. Die Lösung heißt **Entpivotieren**.

1. **Start → Daten abrufen → Web** → Adresse:
   ```
   https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/02-Tag-2/Daten/plan_2025.xlsx
   ```
   → **Anonym** → im **Navigator** links das Blatt **Plan 2025** anhaken → **Daten transformieren**.
2. Rechts unter *Angewendete Schritte* alles **nach „Navigation"** löschen (Power BI hat sonst schon die Titelzeile zur Überschrift gemacht).
3. **Start → Zeilen entfernen → Obere Zeilen entfernen** → `2` (Titel + Leerzeile) → **Start → Erste Zeile als Überschriften verwenden**.
4. Überschrift **Gesamt** anklicken → **Entf** (Spalte entfernen). Summen rechnet Power BI selbst.
5. Überschrift **Filiale** anklicken → **Transformieren → Spalten entpivotieren → Andere Spalten entpivotieren**.
   Aus 4 Zeilen × 12 Monatsspalten werden **48 Zeilen** mit den Spalten *Attribut* (Monat) und *Wert*.
6. Doppelklick auf *Attribut* → `Monat` · Doppelklick auf *Wert* → `Plan` · Typ von `Plan`: **Dezimalzahl**.
7. Aus dem Monatsnamen ein Datum machen: **Spalte hinzufügen → Benutzerdefinierte Spalte**, Name `Monatsanfang`, Formel:
   ```
   #date(2025, List.PositionOf({"Jan","Feb","Mär","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"}, [Monat]) + 1, 1)
   ```
   → **OK** → Typ der neuen Spalte: **Datum**.
8. Abfrage links umbenennen in `Plan` → **Schließen & übernehmen**.
9. **Beziehungen** (Modellansicht, beide n:1, Einfach): `Plan[Filiale]` → `dim_filiale[Filiale]` und `Plan[Monatsanfang]` → `Kalender[Datum]`.
10. **Measures** in `_Measures`:
    ```dax
    Plan = SUM ( Plan[Plan] )
    ```
    ```dax
    Δ Plan = [Umsatz] - [Plan]
    ```
    ```dax
    Δ Plan % = DIVIDE ( [Δ Plan], [Plan] )
    ```
11. **Matrix**: Zeilen `dim_filiale` **Filiale** · Werte `Umsatz`, `Plan`, `Δ Plan`, `Δ Plan %`.

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

🆘 **Hängst du fest?**
- *Nach dem Entpivotieren nur 4 Zeilen / falsche Spalten* → In Schritt 5 war nicht **Filiale** markiert, sondern die Monate. Schritt löschen, neu.
- *„Monatsanfang" zeigt Fehler* → Monatsnamen weichen ab (z. B. „Mrz" statt „Mär"). Filterpfeil bei **Monat** prüfen und die Liste in der Formel anpassen.
- *Plan ist in jeder Filiale gleich* → Beziehung `Plan[Filiale]` → `dim_filiale[Filiale]` fehlt.
- *Zu mühsam?* → [`Tag2_PowerQuery_Plan_entpivotieren.pq`](Loesungen/Tag2_PowerQuery_Plan_entpivotieren.pq) als Leere Abfrage einfügen, `Plan` nennen.

📚 **Mehr dazu:** Kitchen: [Praxis-Pfad · Exkurs „Warum deine Excel-Tabelle nicht passt"](https://datenwgknowledgekitchen.com/powerbi_praxis_pfad.html#exkurs) ·
Microsoft Learn: [Spalten entpivotieren](https://learn.microsoft.com/de-de/power-query/unpivot-column) ·
[Excel-Connector](https://learn.microsoft.com/de-de/power-query/connectors/excel)

---

## Übung 12 · Teilen – was nach dem Desktop kommt (Lesen, 20 min)

Veröffentlichen geht nur mit einem **Geschäfts- oder Schulkonto** und einer Lizenz. Deshalb hier zum Lesen:

| Schritt | Was passiert | Nachlesen |
|---|---|---|
| **Veröffentlichen** | **Start → Veröffentlichen** lädt Modell und Bericht in einen **Workspace** im Power BI Service (Browser). | [Microsoft: Aus Desktop veröffentlichen](https://learn.microsoft.com/de-de/power-bi/create-reports/desktop-upload-desktop-files) |
| **Semantikmodell vs. Bericht** | Im Service liegen zwei Dinge: das Modell (Daten + Measures) und der Bericht (die Seiten). Mehrere Berichte können ein Modell nutzen. | [Kitchen: Service & Sharing](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#service) |
| **Aktualisieren** | Der Service lädt die Daten nach Zeitplan neu. Liegen die Daten im Firmennetz (Dateiserver, Datenbank), braucht es ein **Gateway**. Bei unseren GitHub-Adressen nicht. | [Microsoft: Datenaktualisierung](https://learn.microsoft.com/de-de/power-bi/connect-data/refresh-data) · [Gateway](https://learn.microsoft.com/de-de/power-bi/connect-data/service-gateway-onprem) |
| **App** | Statt einzelner Links: aus dem Workspace eine **App** für die Leser veröffentlichen. | [Microsoft: Apps veröffentlichen](https://learn.microsoft.com/de-de/power-bi/collaborate-share/service-create-distribute-apps) |
| **Lizenzen** | Desktop ist kostenlos. Teilen braucht **Pro** (oder eine Premium/Fabric-Kapazität für die Leser). | [Kitchen: Lizenzen](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#arch) |

### Checkliste, bevor du etwas veröffentlichst

- [ ] Automatisches Datum/Uhrzeit aus, eigene Kalendertabelle markiert
- [ ] Sternschema, alle Beziehungen n:1 und einfach
- [ ] Jede Kennzahl ist ein Measure – keine impliziten Summen auf der Seite
- [ ] Quoten mit `DIVIDE` aus Summen, nie als Mittelwert
- [ ] Hilfsspalten (IDs, Sortierspalten) ausgeblendet: in der Modellansicht Rechtsklick → **In Berichtsansicht ausblenden**
- [ ] Jede Zahl gegen eine Kontrollzahl geprüft

---

## 🎉 Geschafft – wie weiter?

- 🧩 **[Fall Weiterbildungs-Monitoring](../03-Fall-Weiterbildung/)**: alles noch einmal an einem neuen Thema – plus Duplikate, Codierung, kaputte Schlüssel und Quoten mit dem richtigen Nenner. Mit fertiger Lösung zum Vergleichen.
- 🎬 [Videos zum Vertiefen](../04-Material/Videos.md) · 📄 [Handout](../04-Material/Handout.md)
- 🤖 Mit Claude Code weiterbauen: [Claude-Skills](../04-Material/Claude-Skills.md)

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
