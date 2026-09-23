# Tag 1 · Vom Kassen-Export zum ersten Bericht

**Die Aufgabe:** Du arbeitest im Controlling der **Rad & Tat GmbH**, einem Fahrradhändler mit
vier Filialen (Hamburg, Köln, München, Leipzig). Die Geschäftsführung will wissen:
*Wie viel haben wir 2025 umgesetzt, wo, wann – und fällt irgendwo etwas auf?*

Du bekommst dafür einen Export aus dem Kassensystem. Er ist, wie Exporte eben sind: unordentlich.

**Datei:** [`daten/tag1/verkaeufe_2025_roh.csv`](../daten/tag1/verkaeufe_2025_roh.csv)

> Jede Übung endet mit einem **✅ Kontrollpunkt**. Stimmt deine Zahl, bist du richtig.
> Stimmt sie nicht, steht darunter die häufigste Ursache. Die Lösung als M-Code liegt in
> [`snippets/powerquery/tag1_verkaeufe_bereinigen.pq`](../snippets/powerquery/tag1_verkaeufe_bereinigen.pq).

---

## Übung 0 · Setup-Check (10 min)

1. Power BI Desktop starten (Microsoft Store oder [Download bei Microsoft](https://powerbi.microsoft.com/de-de/desktop/)). Nur Windows.
2. Anmeldefenster wegklicken – für heute brauchst du kein Konto.
3. **Datei → Optionen und Einstellungen → Optionen → Regionale Einstellungen:** Gebietsschema für Import steht auf *Deutsch (Deutschland)*? Dann gilt der Hinweis in Übung 2, Handgriff 6–8 genau so für dich.

**✅ Kontrollpunkt:** Leere weiße Berichtsfläche, oben das Menüband *Datei · Start · Einfügen · Modellierung · Ansicht · Hilfe*.

---

## Übung 1 · Daten anbinden (15 min)

1. **Start → Daten abrufen → Web**.
2. URL einfügen:
   ```
   https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/daten/tag1/verkaeufe_2025_roh.csv
   ```
3. Anmeldung: **Anonym** → **Verbinden**.
4. In der Vorschau **Daten transformieren** klicken (nicht *Laden*). Der Power Query-Editor öffnet sich.
5. Rechts unter **Angewendete Schritte** hat Power BI eventuell schon selbst Schritte angelegt
   (*Höher gestufte Header*, *Geänderter Typ*). **Lösch alles außer „Quelle"** – klick auf das X
   vor dem Schritt. Wir wollen jeden Handgriff selbst machen und verstehen.

> Kein Internet oder Firmen-Proxy? Datei herunterladen und über **Daten abrufen → Text/CSV** laden. Rest bleibt gleich.

**✅ Kontrollpunkt:** Die Spalten heißen `Column1` bis `Column8`. In der ersten Zeile steht
`Export RT-Kasse v4.2 | Rad & Tat GmbH | …`, in der zweiten `Belegnummer`, `Belegdatum`, …

---

## Übung 2 · Aufräumen in Power Query (35 min)

In der Datei stecken fünf typische Export-Probleme: eine Müllzeile oben, keine richtigen
Überschriften, leere Zeilen mittendrin, Leerzeichen hinter Filialnamen, uneinheitliche
Groß-/Kleinschreibung – und Zahlen mit **Punkt** als Dezimalzeichen.

| # | Handgriff | Wo |
|---|---|---|
| 1 | Müllzeile weg | **Start → Zeilen entfernen → Obere Zeilen entfernen** → `1` |
| 2 | Überschriften | **Start → Erste Zeile als Überschriften verwenden** |
| 3 | Leere Zeilen weg | **Start → Zeilen entfernen → Leere Zeilen entfernen** |
| 4 | Leerzeichen | Spalte **Filiale** markieren → **Transformieren → Format → Kürzen** |
| 5 | Schreibweise | Spalte **Kategorie** markieren → **Transformieren → Format → Jedes Wort großschreiben** |
| 6 | Datum | **Belegdatum** → Rechtsklick → **Typ ändern → Gebietsschema verwenden…** → *Datum*, *Englisch (USA)* |
| 7 | Zahlen | **Umsatz** und **Kosten** → Rechtsklick → **Typ ändern → Gebietsschema verwenden…** → *Dezimalzahl*, *Englisch (USA)* |
| 8 | Ganzzahl | **Menge** → Symbol links im Spaltenkopf → *Ganze Zahl* |

> **Warum „Gebietsschema"?** In der Datei steht `616.55`. Ein deutsches Windows liest den Punkt
> als Tausendertrennzeichen – aus 616,55 € würden 61.655 €. Mit *Englisch (USA)* sagst du:
> „Diese Datei kommt aus einem System, das den Punkt als Komma benutzt."

Prüfen: Klick bei **Filiale** und **Kategorie** auf den kleinen Pfeil im Spaltenkopf – dort siehst du alle vorkommenden Werte.

Dann **Start → Schließen & übernehmen**.

**✅ Kontrollpunkt:**
- Tabellenansicht (Gittersymbol links) → unten steht **2.877 Zeilen**.
- **Filiale** hat genau **4** Werte, **Kategorie** genau **5** (Bekleidung, E-Bikes, Fahrräder, Werkstatt, Zubehör).

Stimmt nicht?
- *Mehr als 4 Filialen* → Handgriff 4 fehlt (`Köln` und `Köln␣` sind für Power BI zwei Filialen).
- *Mehr als 5 Kategorien* → Handgriff 5 fehlt.
- *2.883 Zeilen* → Handgriff 3 fehlt (6 leere Zeilen stecken noch drin).
- *Spalten heißen „Export RT-Kasse …" oder „B100001"* → Handgriff 1 und 2 vertauscht.

---

## Übung 3 · Erste Antworten: wie viel, wo, wann? (30 min)

Berichtsansicht (oberstes Symbol links).

1. **Karte** (Symbol mit „123") → Feld **Umsatz**.
2. **Gestapeltes Balkendiagramm** → **Filiale** + **Umsatz**. Absteigend sortiert?
3. **Liniendiagramm** → **Belegdatum** + **Umsatz**. In der X-Achse **Jahr, Quartal, Tag** per X entfernen, nur **Monat** bleibt.

**✅ Kontrollpunkt:**
- Karte: **1,24 Mio.** (genau: 1.244.017,12 €)
- Balken: **München** oben (411,51 Tsd.), **Leipzig** unten (184,34 Tsd.)
- Linie: Tiefpunkt **Januar**, Höchstwert **Mai** (162,34 Tsd.), kleiner Buckel im **Dezember** (Weihnachtsgeschäft)

Steht auf der Karte **124,4 Mio.**? → Handgriff 7 ohne Gebietsschema gemacht; zurück in Power Query.

> **Neues Wort – Dimension & Kennzahl.** Die *Kennzahl* ist, was du misst (Umsatz). Die
> *Dimension* ist, wonach du aufteilst (Filiale, Monat). Jedes Diagramm = eine Kennzahl, aufgeteilt nach einer Dimension.

---

## Übung 4 · Filtern (15 min)

1. **Datenschnitt** → Feld **Kategorie**.
2. Klick auf **E-Bikes** – beobachte **alle** Visuals gleichzeitig.
3. Auswahl aufheben. Dann im Balkendiagramm direkt auf den Balken **Leipzig** klicken.

**✅ Kontrollpunkt:**
- Mit **E-Bikes** im Datenschnitt zeigt die Karte **724,8 Tsd.** – mehr als die Hälfte des Umsatzes.
- Mit Balken **Leipzig** zeigt die Karte **184,34 Tsd.**

Danach: Auswahl aufheben (auf eine leere Stelle klicken).

---

## Übung 5 · Nicht jede Zahl darf man addieren (25 min)

Die Geschäftsführung fragt nach der **Marge**. Die gibt es in der Datei nicht – also rechnen wir sie.

1. **Start → Daten transformieren** (zurück in Power Query).
2. **Spalte hinzufügen → Benutzerdefinierte Spalte**, Name `Marge`, Formel:
   ```
   ([Umsatz] - [Kosten]) / [Umsatz]
   ```
   Typ danach auf **Dezimalzahl** setzen. **Schließen & übernehmen**.
3. Neue **Karte** → Feld **Marge**.

**Erst der Fehler:** Die Karte zeigt rund **1.291** (angezeigt als *1,29 Tsd.*). Eine Marge von 129.100 %? Power BI hat alle
2.877 Einzelmargen **addiert** – das macht es bei jeder Zahlenspalte automatisch.

4. Im Feld **Wert** auf den Pfeil neben *Summe von Marge* → **Mittelwert**. Als Prozent formatieren.

**✅ Kontrollpunkt:** **44,9 %**.

> ⚠️ **Cliffhanger für morgen:** Auch 44,9 % ist falsch. Ein Mittelwert über Zeilen zählt den
> 20-€-Schlauchwechsel genauso wie das 5.000-€-Lastenrad. Richtig ist
> *Summe Deckungsbeitrag ÷ Summe Umsatz* = **32,0 %**. Das rechnen wir an Tag 2 mit einem **Measure**.
> Für die Frage „fällt irgendwo etwas auf?" reicht der Mittelwert aber schon:

5. **Liniendiagramm** → **Belegdatum** (nur Monat) + **Marge** (Mittelwert).
6. **Filiale** ins Feld **Legende** ziehen.

**✅ Kontrollpunkt – die Antwort:** Bis Mai laufen alle vier Linien bei rund 46 %.
Ab **Juni** bricht **Köln** auf rund 36 % ein und bleibt unten. Der Umsatz in Köln sieht dabei
unauffällig aus – deshalb ist es in Übung 3 niemandem aufgefallen. *Hypothese für die Chefin: In Köln läuft seit Juni eine Rabattaktion, die niemand beendet hat.*

---

## Übung 6 · Fertig machen (15 min)

1. **Einfügen → Textfeld** → `Rad & Tat · Verkäufe 2025`, Schriftgröße 24–28.
2. Aufräumen: nichts überlappt, nichts ragt über den Rand. Raster: Titel oben · Karten links · Balken rechts · Linien unten · Datenschnitt in eine Ecke.
3. Seite unten umbenennen: Doppelklick auf *Seite 1* → `Überblick`.
4. **Datei → Speichern unter** → `rad_und_tat_tag1.pbix`. **Die Datei brauchst du morgen nicht** – Tag 2 startet mit einem neuen Modell.
5. **Datei → Exportieren → In PDF exportieren**.

**✅ Kontrollpunkt:** Ein PDF mit Titel, drei Karten/Diagrammen, zwei Linien und dem Datenschnitt.

---

### Glossar Tag 1

| Wort | In einem Satz |
|---|---|
| Zeile / Spalte | Eine Zeile ist ein Vorgang (ein Beleg), eine Spalte eine Eigenschaft jedes Vorgangs. |
| Transformation | Ein Handgriff in Power Query, der die Daten formt, ohne die Quelldatei anzufassen. |
| Angewendete Schritte | Das Rezept: wird bei jeder Aktualisierung neu abgearbeitet. |
| Gebietsschema | Sagt Power BI, wie Zahlen und Datumswerte in der Quelle geschrieben sind. |
| Visual | Ein einzelnes Bild auf der Seite. |
| Dimension / Kennzahl | Wonach du aufteilst / was du misst. |
| Filter | Schränkt ein, welche Zeilen zählen – wirkt auf alle Visuals gleichzeitig. |
| Aggregation | Wie viele Zeilen zu einer Zahl werden: Summe, Mittelwert, Anzahl … |
