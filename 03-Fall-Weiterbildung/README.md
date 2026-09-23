# Fall · Weiterbildungs-Monitoring

**Zum Selbermachen nach dem Training – etwa 3 Stunden, in Etappen machbar.**

Die **Muster Maschinenbau GmbH** (fiktiv, 420 Mitarbeitende, drei Standorte) will wissen, ob sie ihre
Weiterbildungsziele 2025 erreicht. Die Personalentwicklung liefert dir drei Dinge, wie sie im echten
Leben kommen: einen **unordentlichen Export aus dem Lernsystem (LMS)**, **Stammdaten aus dem HR-System** und
die **Ziele als Excel-Kreuztabelle**. Daraus baust du ein Modell und eine Übersichtsseite.

Du übst dabei alles aus den beiden Trainingstagen noch einmal – plus vier neue Handgriffe:
**Datei-Codierung**, **Duplikate**, **kaputte Schlüssel** (führende Nullen) und **Quoten mit dem richtigen Nenner**.

> ⬇️ **Alles in einem Paket:** [Anleitung als PDF + Daten + Skripte (ZIP)](https://github.com/Losveratos/Power-Starter-24-25-September/raw/main/00-Downloads/Fall-Weiterbildungs-Monitoring.zip)

---

## Bevor du anfängst

**Du brauchst:** Power BI Desktop auf Windows ([Installation: Tag 1, Übung 0](../01-Tag-1/README.md#übung-0--power-bi-desktop-installieren-15-min)),
Internet, etwa **4 Stunden** – gern in Etappen, nach jedem Schritt speichern (**Strg + S**).

**Vorwissen:** Dieser Fall setzt voraus, was an [Tag 1](../01-Tag-1/) und [Tag 2](../02-Tag-2/) drankam. Die Klickwege
stehen hier deshalb kürzer – bei jedem Schritt steht, in welcher Übung du sie ausführlich findest.

| Zeichen | Bedeutung |
|---|---|
| ✅ **Kontrollpunkt** | Diese Zahl muss bei dir stehen. |
| 🆘 **Hängst du fest?** | Häufige Fehler und wie du sie behebst. |
| ⏭ **Überspringen** | Fertiges Skript für diesen Schritt – einfügen, Kontrollzahl prüfen, weiter. |
| 📚 **Mehr dazu** | [Knowledge Kitchen](https://datenwgknowledgekitchen.com/) und Microsoft Learn zum Nachlesen. |

Alle Kontrollzahlen stehen auch in [`Daten/kontrollzahlen.json`](Daten/kontrollzahlen.json). Die komplette Lösung als
Power-BI-Datei liegt in [`PowerBI-Loesung`](PowerBI-Loesung/) – zum Vergleichen, wenn du fertig bist.

---

## Was liegt hier?

| Ordner | Inhalt |
|---|---|
| [`Daten/1-Rohdaten/`](Daten/1-Rohdaten/) | `weiterbildung_buchungen_2025.csv` – LMS-Export, **absichtlich unordentlich** |
| [`Daten/2-Anreicherung/`](Daten/2-Anreicherung/) | `dim_mitarbeitende.csv` (HR-Stamm, pseudonymisiert) · `dim_bereich.csv` · `dim_kurs.csv` |
| [`Daten/3-Ziele/`](Daten/3-Ziele/) | `ziele_2025.xlsx` mit zwei Blättern (Budget je Quartal, Zielwerte je Kennzahl) + dieselben Tabellen als CSV |
| [`Loesungen/PowerQuery/`](Loesungen/PowerQuery/) | M-Code für jeden Lade- und Aufräumschritt – zum Überspringen |
| [`Loesungen/DAX/`](Loesungen/DAX/) | alle Measures mit Kontrollzahlen |
| [`Mockup/`](Mockup/) | Seitenentwurf aus der MockupKitchen – das Ziel dieses Falls |
| [`PowerBI-Loesung/`](PowerBI-Loesung/) | die fertige Lösung als Power-BI-Projekt zum Vergleichen |

Basis-Adresse für **Daten abrufen → Web** (Anmeldung **Anonym**):
```
https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/03-Fall-Weiterbildung/Daten/
```
…plus Unterordner und Dateiname, z. B. `…/Daten/1-Rohdaten/weiterbildung_buchungen_2025.csv`.

---

## Das Ziel: diese Seite

![Mockup der Seite „Überblick"](Mockup/page-1-uberblick.png)

*Skizze aus der [MockupKitchen](https://datenwgknowledgekitchen.com/mockup-kitchen.html) – die Zahlen im Bild sind Platzhalter, die echten rechnest du aus.*

**Frage der Seite:** *Erreichen wir unsere Weiterbildungsziele 2025 – und wo müssen wir nachsteuern?*

Oben fünf Kennzahlen mit Ziel (Teilnahmequote, Ø Stunden je MA, Pflichtquote, Kosten vs. Budget,
Zufriedenheit), darunter die drei Stellen, an denen man nachsteuert: **Budget je Quartal**,
**Pflichtquote je Standort**, **Stunden je Bereich** – und unten Saison, Vollzeit/Teilzeit und die teuersten Kurse.
Die Begründung jeder Kachel steht in der [Workshop-Doku](Mockup/WORKSHOP-DOKU.md).

---

## Schritt 1 · Den Rohexport ansehen (10 min)

Schau dir die Rohdatei zuerst als Text an – **nicht in Excel** (Excel „repariert" beim Öffnen und versteckt die Probleme):
[`weiterbildung_buchungen_2025.csv`](Daten/1-Rohdaten/weiterbildung_buchungen_2025.csv) anklicken – GitHub zeigt sie als Tabelle; oben auf **Code** klicken
zeigt den reinen Text. *(Offline: im entpackten ZIP Rechtsklick auf die Datei → **Öffnen mit → Editor**.)* Was fällt auf?

- Trennzeichen ist das **Semikolon**, Zahlen haben ein **Komma** (`7,5`), Kosten ein **€-Zeichen** (`1.234,50 €`).
- Datumswerte stehen als `TT.MM.JJJJ`.
- Die `Personalnr` hat **keine führenden Nullen** (`238`) – im HR-Stamm heißt dieselbe Person `00238`.
- Der `Status` ist mal `abgeschlossen`, mal `ABGESCHLOSSEN `, mal `teilgenommen`.
- Ganz unten steht eine Summenzeile. Manche Buchungen stehen **doppelt** drin.
- Die Datei ist in **Windows-1252** gespeichert, nicht in UTF-8.

---

## Schritt 2 · Rohdaten aufräumen (45 min)

1. Neuer Bericht (**Datei → Neu**) → **Start → Daten abrufen → Web** → Adresse
   ```
   https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/03-Fall-Weiterbildung/Daten/1-Rohdaten/weiterbildung_buchungen_2025.csv
   ```
   → **OK** → **Anonym** → **Verbinden**.
2. Im Vorschaufenster oben **Dateiursprung: 1252: Westeuropäisch (Windows)** und **Trennzeichen: Semikolon** wählen.
   Probier vorher einmal *65001: Unicode (UTF-8)* – dann siehst du, was mit `Präsenz` und `Datensätze` passiert.
3. **Daten transformieren.** Unter *Angewendete Schritte* alles nach **Höher gestufte Header** löschen.
4. Die Handgriffe:

| # | Problem | Handgriff |
|---|---|---|
| 1 | Summenzeile am Ende | **Start → Zeilen entfernen → Untere Zeilen entfernen** → `1` |
| 2 | Doppelte Buchungen | Spalte **BuchungsID** markieren → **Start → Zeilen entfernen → Duplikate entfernen** |
| 3 | Kurstitel doppelt (steht auch im Kurskatalog) | Spalte **Kurstitel** entfernen |
| 4 | Führende Nullen fehlen | **Spalte hinzufügen → Benutzerdefinierte Spalte** → Name `Personalnr_neu`, Formel `Text.PadStart([Personalnr], 5, "0")` → **OK**. Dann die alte Spalte **Personalnr** entfernen (Überschrift anklicken → **Entf**) und die neue per Doppelklick in `Personalnr` umbenennen. *(„Präfix hinzufügen" hilft nicht – mal fehlen 2, mal 3 Nullen.)* |
| 5 | Status uneinheitlich | **Status** markieren → **Transformieren → Format → Kürzen**, dann **Format → Kleinbuchstaben**, dann je Paar Rechtsklick → **Werte ersetzen**: `teilgenommen` → `abgeschlossen`, `no show` und `nicht erschienen` → `No-Show`, `no-show` → `No-Show` |
| 6 | Euro-Zeichen | Rechtsklick auf **Kosten** → **Werte ersetzen** → *Zu suchender Wert:* ` €` (Leerzeichen + €) → *Ersetzen durch:* leer lassen → **OK** |
| 7 | Leeres Feedback | Rechtsklick auf **Feedback** → **Werte ersetzen** → *Zu suchender Wert:* leer lassen → *Ersetzen durch:* `null` → **OK** |
| 8 | Datentypen | Datumsspalten → **Datum**, **Stunden** → Dezimalzahl, **Kosten** → Währung, **Feedback** → Ganze Zahl. Diesmal **ohne** Gebietsschema-Umweg – die Datei ist deutsch wie dein Windows |

5. Abfrage `fakt_buchungen` nennen.

**✅ Kontrollpunkt:** **1.712 Zeilen**, 10 Spalten. Filterpfeil bei **Status** zeigt genau vier Werte:
`abgeschlossen` (1.587) · `storniert` (69) · `No-Show` (53) · `angemeldet` (3).

🆘 **Hängst du fest?**
- *1.736 Zeilen?* → Duplikate noch drin (Handgriff 2).
- *1.713 Zeilen?* → Summenzeile noch drin (Handgriff 1). *1.737* → beides.
- *Mehr als vier Status-Werte?* → Kürzen oder Kleinbuchstaben vergessen.

⏭ **Überspringen:** [`01_fakt_buchungen.pq`](Loesungen/PowerQuery/01_fakt_buchungen.pq)

📚 **Mehr dazu:** Kitchen: [Power Query · Staging (Datentypen, Schlüssel bereinigen)](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#pq) ·
Microsoft Learn: [Text/CSV-Connector](https://learn.microsoft.com/de-de/power-query/connectors/text-csv) ·
[Mit Duplikaten arbeiten](https://learn.microsoft.com/de-de/power-query/working-with-duplicates) ·
[Datentypen und Gebietsschema](https://learn.microsoft.com/de-de/power-query/data-types)

---

## Schritt 3 · Anreichern: Dimensionen laden und Schlüssel prüfen (30 min)

1. Die drei CSVs laden (je **Daten abrufen → Web** → `https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/03-Fall-Weiterbildung/Daten/2-Anreicherung/` + Dateiname → **Daten transformieren**) (UTF-8, Komma, Punkt als Dezimalzeichen – also **FTE** mit Gebietsschema *Englisch (USA)*).
2. Abfragen nennen: `dim_mitarbeitende`, `dim_bereich`, `dim_kurs`.
3. **Personalnr ist Text!** Sonst wird aus `00238` die Zahl `238` – und nichts passt mehr zusammen.
4. **Prüfen, ob die Schlüssel passen:** `fakt_buchungen` markieren → **Start → Abfragen zusammenführen als neue Abfrage** →
   unten `dim_mitarbeitende`, beide Male Spalte **Personalnr** markieren → Join-Art **Linker Anti (nur Zeilen in erster Tabelle)**.
   Das Ergebnis sind alle Buchungen **ohne** passende Person. Danach die Prüfabfrage mit Rechtsklick → *Laden aktivieren* abschalten.

**✅ Kontrollpunkt:** `dim_mitarbeitende` **420**, `dim_bereich` **7**, `dim_kurs` **23** Zeilen (davon **3** mit `Pflicht = Ja`).
Die Anti-Join-Prüfung ergibt **0 Zeilen**. Nimm testweise Handgriff 4 aus Schritt 2 heraus: Dann sind es **alle 1.712** – so sieht ein kaputter Schlüssel aus.

🆘 **Hängst du fest?**
- *FTE steht als 50 oder 75 statt 0,5 / 0,75* → FTE ohne Gebietsschema umgewandelt: Rechtsklick → **Typ ändern → Gebietsschema verwenden…** → Dezimalzahl, *Englisch (USA)*.
- *Personalnr ohne führende Nullen (z. B. 238)* → Power BI hat sie als Zahl erkannt. Typ-Schritt löschen, Spalte als **Text** setzen.
- *„Abfragen zusammenführen" ist grau* → Du bist nicht im Power Query-Editor oder `fakt_buchungen` ist nicht links markiert.

⏭ **Überspringen:** [`02a_dim_mitarbeitende.pq`](Loesungen/PowerQuery/02a_dim_mitarbeitende.pq) ·
[`02b_dim_bereich.pq`](Loesungen/PowerQuery/02b_dim_bereich.pq) · [`02c_dim_kurs.pq`](Loesungen/PowerQuery/02c_dim_kurs.pq) ·
[`03_pruefung_anti_join.pq`](Loesungen/PowerQuery/03_pruefung_anti_join.pq)

📚 **Mehr dazu:** Microsoft Learn: [Abfragen zusammenführen – Überblick](https://learn.microsoft.com/de-de/power-query/merge-queries-overview) ·
[Linker Anti-Join](https://learn.microsoft.com/de-de/power-query/merge-queries-left-anti)

---

## Schritt 4 · Ziele entpivotieren (30 min)

Die Personalentwicklung plant in Excel – **Bereiche in Zeilen, Quartale bzw. Kennzahlen in Spalten**.
Für Menschen perfekt, für Power BI unbrauchbar. Zwei Blätter, zweimal derselbe Handgriff.

**Blatt „Budget 2025":**
1. **Daten abrufen → Web** → Adresse `https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/03-Fall-Weiterbildung/Daten/3-Ziele/ziele_2025.xlsx` → **Anonym** → im Navigator Blatt **Budget 2025** anhaken → **Daten transformieren**. Rechts alle Schritte nach *Navigation* löschen.
2. **Obere Zeilen entfernen** `2` → **Erste Zeile als Überschriften**.
3. Zeile **Gesamt** herausfiltern, Spalte **Summe** entfernen – Summen rechnet Power BI selbst.
4. **Bereich** markieren → **Transformieren → Spalten entpivotieren → Andere Spalten entpivotieren**. *Attribut* → `Quartal`, *Wert* → `Budget`.
5. **Benutzerdefinierte Spalte** `Quartalsanfang`: `#date(2025, (Number.From(Text.End([Quartal], 1)) - 1) * 3 + 1, 1)`, Typ Datum. Abfrage `Budget` nennen.

**Blatt „Zielwerte 2025":** dasselbe ohne Gesamt/Summe. *Attribut* → `Kennzahl`, *Wert* → `Zielwert` (Dezimalzahl). Abfrage `Zielwerte` nennen.

**✅ Kontrollpunkt:** `Budget` **28 Zeilen**, Summe **274.500 €**. `Zielwerte` **28 Zeilen**; die Teilnahmequote steht als **0,75**, nicht als 75 – das „%" in Excel war nur Formatierung.

🆘 **Hängst du fest?** Klickweg ausführlich: [Tag 2, Übung 11](../02-Tag-2/README.md#übung-11--plan-ist-aus-einer-excel-kreuztabelle-35-min).
*Zeile „Gesamt" herausfiltern:* Filterpfeil bei **Bereich** → Häkchen bei *Gesamt* entfernen → **OK**.
*Nur 7 statt 28 Zeilen:* Beim Entpivotieren war nicht **Bereich** markiert.
*`Quartalsanfang` zeigt Fehler:* Die Quartalsspalte heißt noch *Attribut* – erst umbenennen, dann die Formel.

⏭ **Überspringen:** [`04_budget_entpivotieren.pq`](Loesungen/PowerQuery/04_budget_entpivotieren.pq) · [`05_zielwerte_entpivotieren.pq`](Loesungen/PowerQuery/05_zielwerte_entpivotieren.pq)

📚 **Mehr dazu:** Kitchen: [Praxis-Pfad · Exkurs „Warum deine Excel-Tabelle nicht passt"](https://datenwgknowledgekitchen.com/powerbi_praxis_pfad.html#exkurs) ·
Microsoft Learn: [Spalten entpivotieren](https://learn.microsoft.com/de-de/power-query/unpivot-column)

---

## Schritt 5 · Kalender und Beziehungen (25 min)

1. **Automatisches Datum/Uhrzeit aus:** **Datei → Optionen und Einstellungen → Optionen → Aktuelle Datei → Datenladevorgang** → Häkchen entfernen.
2. **Kalender:** [`06_kalender.pq`](Loesungen/PowerQuery/06_kalender.pq) als Leere Abfrage einfügen, `Kalender` nennen, **als Datumstabelle markieren**,
   `Monat` nach `MonatNr` sortieren. *(Ausführlich: [Tag 2, Übung 9](../02-Tag-2/README.md#übung-9--kalendertabelle-20-min).)*
3. **Beziehungen** in der Modellansicht ziehen, alle **n:1**, Filterrichtung **einfach** *(ausführlich: [Tag 2, Übung 8](../02-Tag-2/README.md#übung-8--beziehungen--das-sternschema-25-min))*:

| Von (n) | Nach (1) |
|---|---|
| `fakt_buchungen[Personalnr]` | `dim_mitarbeitende[Personalnr]` |
| `fakt_buchungen[Kursnr]` | `dim_kurs[Kursnr]` |
| `fakt_buchungen[Kursbeginn]` | `Kalender[Datum]` |
| `dim_mitarbeitende[BereichID]` | `dim_bereich[BereichID]` |
| `Budget[Bereich]` | `dim_bereich[Bereich]` |
| `Budget[Quartalsanfang]` | `Kalender[Datum]` |
| `Zielwerte[Bereich]` | `dim_bereich[Bereich]` |

> `dim_bereich` hängt an `dim_mitarbeitende` statt direkt am Fakt – eine kleine **Schneeflocke**. Das ist hier in
> Ordnung, weil Budget und Ziele eine eigene Bereichstabelle brauchen. Wer es ganz sauber will, führt `Bereich` per
> *Abfragen zusammenführen* in `dim_mitarbeitende` mit und lässt `dim_bereich` nur für Budget und Ziele stehen.

**✅ Kontrollpunkt:** Tabelle `dim_bereich[Bereich]` × Anzahl `dim_mitarbeitende[Personalnr]`: Produktion **150**, Logistik **55**, Entwicklung **60**, Service **45**, Vertrieb **45**, IT **25**, Verwaltung **40**.

🆘 **Hängst du fest?**
- *Überall 420* → Beziehung `dim_mitarbeitende[BereichID]` → `dim_bereich[BereichID]` fehlt.
- *Power BI will „n:n" anlegen* → Die Spalte auf der 1-Seite ist nicht eindeutig. Bei `Budget` → `dim_bereich` muss die Zeile *Gesamt* raus sein (Schritt 4).
- *Beziehung Budget → Kalender geht nicht* → `Quartalsanfang` ist noch kein **Datum**.

📚 **Mehr dazu:** Kitchen: [Datenmodellierung · Sternschema, Kalender, Modell-Prinzipien](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#model) ·
Microsoft Learn: [Sternschema](https://learn.microsoft.com/de-de/power-bi/guidance/star-schema) ·
[Beziehungen verstehen](https://learn.microsoft.com/de-de/power-bi/transform-model/desktop-relationships-understand) ·
[Datumstabellen](https://learn.microsoft.com/de-de/power-bi/transform-model/desktop-date-tables)

---

## Schritt 6 · Grundgrößen (20 min)

1. **Start → Daten eingeben** → Name `_Measures` → **Laden**. *(Ausführlich: [Tag 2, Übung 10](../02-Tag-2/README.md#übung-10--measures-statt-autosumme-45-min).)*
2. `_Measures` anklicken → **Tabellentools → Neues Measure** → Formel einfügen → **Enter**. Nacheinander:
   ```dax
   Headcount = COUNTROWS ( dim_mitarbeitende )
   ```
   ```dax
   Buchungen = COUNTROWS ( fakt_buchungen )
   ```
   ```dax
   Teilnahmen = CALCULATE ( [Buchungen], fakt_buchungen[Status] = "abgeschlossen" )
   ```
   ```dax
   Stunden = CALCULATE ( SUM ( fakt_buchungen[Stunden] ), fakt_buchungen[Status] = "abgeschlossen" )
   ```
   ```dax
   Kosten = SUM ( fakt_buchungen[Kosten] )
   ```
3. Jedes Measure in eine **Karte** ziehen und ablesen.

**✅ Kontrollpunkt:** Headcount **420** · Buchungen **1.712** · Teilnahmen **1.587** · Stunden **6.894** · Kosten **272.678,91 €**

🆘 **Hängst du fest?**
- *Teilnahmen = 0* → Der Status heißt bei dir anders (z. B. „Abgeschlossen" groß). Schritt 2, Handgriff 5 prüfen.
- *Kosten viel zu hoch* → Kosten sind noch Text mit €-Zeichen oder falsch umgewandelt. Schritt 2, Handgriffe 6 und 8.

📚 **Mehr dazu:** Microsoft Learn: [Eigene Measures erstellen (Tutorial)](https://learn.microsoft.com/de-de/power-bi/transform-model/desktop-tutorial-create-measures) ·
Kitchen: [Einsteiger-Guide · DAX (Measures vs. berechnete Spalten)](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#dax)

---

## Schritt 7 · Quoten mit dem richtigen Nenner (40 min)

Die wichtigste Lektion dieses Falls: **Wer ist „alle"?**

- `Ø Stunden je MA = DIVIDE ( [Stunden], [Headcount] )` – geteilt durch **alle** 420, nicht nur durch die, die in der
  Buchungstabelle vorkommen. Wer nie auf einer Schulung war, gehört zur Belegschaft und muss den Schnitt drücken.
- `Teilnahmequote` = Personen mit mindestens einer **freiwilligen** abgeschlossenen Weiterbildung ÷ Headcount (`DISTINCTCOUNT` + `CALCULATE`).
- `Pflichtquote` = Personen, die **alle drei** Pflichtkurse abgeschlossen haben ÷ Headcount. Das ist das anspruchsvollste
  Measure: `FILTER` über die Mitarbeitenden, je Person zählen, wie viele Pflichtkurse sie hat. Lies es in
  [`measures.dax`](Loesungen/DAX/measures.dax) Zeile für Zeile.
- `Ø Zufriedenheit = AVERAGE ( fakt_buchungen[Feedback] )` – hier ist der Mittelwert **richtig**: jede Bewertung zählt gleich.
  Leere Bewertungen sind `null` und werden nicht mitgezählt (deshalb Handgriff 7 in Schritt 2).

**✅ Kontrollpunkt (gesamt):** Ø Stunden je MA **16,41** · Teilnahmequote **63,3 %** · Pflichtquote **79,5 %** · Stornoquote **4,0 %** · No-Show-Quote **3,1 %** · Ø Zufriedenheit **3,78**

**Und nach Standort** (Matrix `dim_mitarbeitende[Standort]` × `Pflichtquote`):

| Standort | Headcount | Pflichtquote | Ø Stunden je MA |
|---|---:|---:|---:|
| Zentrale Hannover | 156 | 92,3 % | 16,24 |
| Werk Kassel | 119 | 88,2 % | 17,08 |
| **Werk Ulm** | 145 | **58,6 %** | 16,06 |

Nimm `dim_kurs[Kurstitel]` dazu: In Ulm fehlt vor allem **Datenschutz-Grundlagen** – ein E-Learning, und in
Produktion und Logistik gibt es kaum PC-Arbeitsplätze. Nur **62,3 %** dort haben es abgeschlossen.

**Vollzeit vs. Teilzeit** (`dim_mitarbeitende[Beschaeftigung]`): Ø Stunden **17,86 h** vs. **9,79 h**, Teilnahmequote **69,0 %** vs. **37,3 %**.

**So kommst du an die Zahlen:** alle Measures aus [`measures.dax`](Loesungen/DAX/measures.dax) (Abschnitt *Schritt 7*) einzeln anlegen,
dann eine **Matrix** mit Zeilen `dim_mitarbeitende` **Standort** und den Measures als Werte.

🆘 **Hängst du fest?**
- *Ø Stunden je MA ist viel höher (z. B. 26)* → Du teilst durch die Personen aus der Buchungstabelle statt durch `[Headcount]`. Genau das ist die Falle dieses Schritts.
- *Pflichtquote 0 %* → `dim_kurs[Pflicht]` enthält „Ja"/„Nein" – prüf die Schreibweise im Measure. Oder die Beziehung `fakt_buchungen[Kursnr]` → `dim_kurs[Kursnr]` fehlt.
- *Teilnahmequote über 100 %* → Die Beziehung `fakt_buchungen[Personalnr]` → `dim_mitarbeitende[Personalnr]` fehlt oder die Personalnummern haben keine führenden Nullen (Schritt 2, Handgriff 4).

📚 **Mehr dazu:** Kitchen: [DAX · CALCULATE, Filterkontext, Anti-Patterns](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#dax) ·
Microsoft Learn: [DIVIDE](https://learn.microsoft.com/de-de/dax/divide-function-dax) ·
[CALCULATE](https://learn.microsoft.com/de-de/dax/calculate-function-dax) ·
[Variablen in DAX](https://learn.microsoft.com/de-de/dax/best-practices/dax-variables)

---

## Schritt 8 · Ziele und Budget (30 min)

- `Budget`, `Δ Budget`, `Budget-Ausschöpfung` – einfache Summen über die entpivotierte Tabelle.
- `Ziel Ø Stunden je MA` & Co.: Jeder Bereich hat ein eigenes Ziel. Für **mehrere** Bereiche zusammen wird das Ziel
  **nach Headcount gewichtet** (`SUMX` über die Bereiche) – sonst zählt die IT mit 25 Leuten so viel wie die Produktion mit 150.

**✅ Kontrollpunkt:** Budget **274.500 €** · Budget-Ausschöpfung **99,3 %** · Ziel Ø Stunden **16,5** · Ziel Teilnahmequote **75,0 %** · Ziel Pflichtquote **95,0 %**

Gesamt sieht das Budget gut aus. Aber:

| | Kosten | Budget | Ausschöpfung |
|---|---:|---:|---:|
| **Q2** (alle Bereiche) | 116.223 € | 77.000 € | **151 %** |
| **Vertrieb** (Jahr) | 45.039 € | 37.000 € | **121,7 %** |
| Vertrieb nur Q2 | 39.543 € | 10.500 € | 377 % |

*Die Vertriebsoffensive im Frühjahr hat Premium-Seminare gebucht – im Jahressaldo versteckt, im Quartal unübersehbar.*

> Budget liegt nur je **Quartal** vor. Zeig es nie nach Monat – dort wäre es falsch verteilt (Granularität).

**So kommst du an die Zahlen:** Measures aus [`measures.dax`](Loesungen/DAX/measures.dax) (Abschnitt *Schritt 8*) anlegen, dann
eine **Matrix** mit Zeilen `Kalender` **Quartal** und Werten `Kosten`, `Budget`, `Budget-Ausschöpfung` – und eine zweite mit `dim_bereich` **Bereich**.

🆘 **Hängst du fest?**
- *Budget ist in jedem Quartal gleich / leer* → Beziehung `Budget[Quartalsanfang]` → `Kalender[Datum]` fehlt.
- *Budget ist in jedem Bereich 274.500 €* → Beziehung `Budget[Bereich]` → `dim_bereich[Bereich]` fehlt.
- *Ziel-Measures leer* → Die Kennzahlnamen in `Zielwerte[Kennzahl]` müssen exakt stimmen (z. B. `Ø Stunden je MA` mit Ø).

📚 **Mehr dazu:** Kitchen: [Visualisierung & IBCS · Plan-Ist-Notation](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#viz) ·
Microsoft Learn: [SUMX](https://learn.microsoft.com/de-de/dax/sumx-function-dax)

---

## Schritt 9 · Die Seite bauen (45 min)

Bau die Seite nach dem [Mockup](Mockup/page-1-uberblick.png). Die Kachel-Liste mit Feldern steht in der
[Workshop-Doku](Mockup/WORKSHOP-DOKU.md), die Maße in [`AGENT-BRIEF.md`](Mockup/AGENT-BRIEF.md).

**Schritt für Schritt mit Bordmitteln:**
1. **Oben fünf Karten** nebeneinander: `Teilnahmequote`, `Ø Stunden je MA`, `Pflichtquote`, `Kosten`, `Ø Zufriedenheit`.
2. **Darunter drei Diagramme:**
   - *Gruppiertes Säulendiagramm:* X-Achse `Kalender` **Quartal**, Y-Achse `Kosten` und `Budget`.
   - *Gruppiertes Balkendiagramm:* Y-Achse `dim_mitarbeitende` **Standort**, X-Achse `Pflichtquote` und `Ziel Pflichtquote`.
   - *Gruppiertes Balkendiagramm:* Y-Achse `dim_bereich` **Bereich**, X-Achse `Ø Stunden je MA` und `Ziel Ø Stunden je MA`.
3. **Unten:** *Liniendiagramm* `Kalender` **Monat** × `Stunden` · *Balkendiagramm* **Beschaeftigung** × `Teilnahmequote` · *Tabelle* **Kurstitel**, `Teilnahmen`, `Kosten`, `Ø Zufriedenheit` (nach Kosten absteigend sortieren).
4. **Rechts vier Datenschnitte:** Standort, Bereich, Beschaeftigung, Kategorie – im Format-Bereich auf **Dropdown** stellen.
5. **Kopfzeile:** Textfeld `Weiterbildungs-Monitoring 2025`.

**✅ Kontrollpunkt:** Die Karten zeigen **63,3 %** · **16,4** · **79,5 %** · **272.679 €** · **3,78**. Datenschnitt *Werk Ulm* → Pflichtquote **58,6 %**.

- **Nur mit Bordmitteln:** KPI-Kacheln als *Karte (neu)* mit Referenzbeschriftung, Balken und Säulen als *Gruppiertes Balken-/Säulendiagramm* mit Ist und Ziel.
- **Mit ChartKitchen:** Die Kacheln mit Szenario-Notation (Ist vs. Ziel, Abweichung) sind im Mockup für das Visual
  [ChartKitchen byDatenWG](https://datenwgknowledgekitchen.com/chartkitchen-schnellstart.html) vorgesehen.
- **Lösung ansehen:** Das fertige Power-BI-Projekt liegt in [`PowerBI-Loesung/`](PowerBI-Loesung/) – `.pbip` öffnen, aktualisieren, vergleichen.
- **Mit Claude Code:** Speichere dein Modell als **PBIP** und sag im Repo: *„Setz das Mockup `03-Fall-Weiterbildung/Mockup/mockup-spec.json` in meinem Bericht um."* – der Skill `mockup-to-powerbi` baut die Seite (siehe [Claude-Skills](../04-Material/Claude-Skills.md)).
- **Weiterskizzieren:** [MockupKitchen](https://datenwgknowledgekitchen.com/mockup-kitchen.html) öffnen → **Öffnen** → [`weiterbildungs-monitoring.mockup.json`](Mockup/weiterbildungs-monitoring.mockup.json). Dort kannst du Kacheln ändern oder eine Detailseite ergänzen.

📚 **Mehr dazu:** Kitchen: [Einsteiger-Guide · Visualisierung & IBCS](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#viz) ·
[Interaktivität · Drillthrough, Tooltips, bedingte Formatierung](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#inter) ·
Microsoft Learn: [Karten-Visual](https://learn.microsoft.com/de-de/power-bi/visuals/power-bi-visualization-card) ·
[Datenschnitte](https://learn.microsoft.com/de-de/power-bi/visuals/power-bi-visualization-slicers)

---

## ⚠️ Personaldaten

Weiterbildungsdaten sind **personenbezogen**. In diesem Fall sind sie erfunden und pseudonymisiert (nur Personalnummern).
Im echten Leben gilt:

- Die Übersichtsseite zeigt **keine Einzelpersonen** – Bereich, Standort und Kurs reichen für die Steuerung.
- Bei kleinen Gruppen (z. B. 3 Teilzeitkräfte in der IT) lässt sich trotzdem auf Personen schließen. Mindestgröße vereinbaren.
- Führungskräfte sehen nur ihren Bereich → **Row-Level Security**. Betriebsrat und Datenschutz früh einbinden.

📚 **Mehr dazu:** Kitchen: [Row-Level Security](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html#rls) ·
Microsoft Learn: [RLS-Leitfaden](https://learn.microsoft.com/de-de/power-bi/guidance/rls-guidance)

---

## ⭐ Wenn du noch Lust hast

- **Detailseite je Bereich** per Drillthrough: Kurse, Stunden, offene Pflichtschulungen.
- **Anzahl offener Pflichtschulungen** als Measure: `[Headcount] - [Pflicht erfüllt]`.
- **Kosten je Teilnahmestunde** nach Kategorie – welche Kurse sind teuer, welche nur lang?
- **Eintrittsjahr** aus `dim_mitarbeitende[Eintritt]`: Bekommen neue Kolleg:innen mehr Weiterbildung?
- Das Budget per Feldparameter wahlweise nach Bereich oder Quartal zeigen.

---

## Für Trainer:innen

```bash
pip install openpyxl playwright
python3 _Werkzeuge/fall-weiterbildung/generate_data.py                  # Daten + kontrollzahlen.json
python3 _Werkzeuge/fall-weiterbildung/build_mockup.py ../PowerBI-Kitchen-   # Mockup mit der echten MockupKitchen
```
Die Geschichten in den Daten: Werk Ulm hängt beim Datenschutz-E-Learning hinterher · der Vertrieb sprengt im Q2 das
Budget · Teilzeitkräfte bekommen nur halb so viel Weiterbildung · E-Learnings werden schlechter bewertet als Präsenzkurse.
