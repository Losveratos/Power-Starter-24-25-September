# AGENT-BRIEF · Weiterbildungs-Monitoring 2025

Erzeugt von MockupKitchen byDatenWG 0.4 am 2026-09-23 · Spec v3 · Hash `cb7b3760` · Sprache de. Maschinenlesbare Fassung: `mockup-spec.json`. Umsetzung mit dem Skill `mockup-to-powerbi`.

## Berichtskopf

- **Zielgruppe:** Geschäftsführung, Personalentwicklung, Betriebsrat
- **Ziel:** Monatlicher Blick, ob die Weiterbildungsziele 2025 erreicht werden und das Budget hält.
- **Entscheidung:** Wo steuern wir nach: Pflichtschulungen nachholen (Werk Ulm), Budget umschichten (Vertrieb), Kursangebot für Teilzeit öffnen?
- **Version:** 0.1 · **Datenstand:** monatlich, LMS-Export zum Monatsersten

## Canvas und Gestaltung

- 1 Seite(n), alle 1280 × 720 px. Skalierung ×1 gegenüber HD.
- Rand 16 px · Zwischenraum 12 px · Kachel-Innenabstand 8 px.
- Kacheln: Ecken 8 px, Stil „weiß mit feinem Rahmen", Kachelhintergrund #FFFFFF, Seitenhintergrund #F4F4F1.
- Kopfband-Stil „dark", Akzentfarbe #C25A2D. Schriften proportional zur Skalierung (Visual-Titel ≈ 12 pt).
- Gestaltung bevorzugt als Theme-Fragment umsetzen (visualStyles), Overrides je Visual nur für Ausnahmen.

## Zonen (Chrome, auf jeder Seite identisch)

| Zone | x | y | w | h | Inhalt |
|---|---|---|---|---|---|
| Kopfband (dark) | 0 | 0 | 1280 | 56 | Shape Ink-Farbe, weiße Schrift, Logo links (Höhe 32), Titel „Weiterbildungs-Monitoring 2025" · Untertitel „Muster Maschinenbau GmbH · Personalentwicklung" |
| Filter (Panel rechts) | 1100 | 56 | 180 | 640 | Slicer gestapelt: `dim_mitarbeitende.Standort`, `dim_bereich.Bereich`, `dim_mitarbeitende.Beschaeftigung`, `dim_kurs.Kategorie` |
| Fußleiste | 0 | 696 | 1280 | 24 | Textfeld 9 pt grau: „Quelle: LMS-Export + HR-Stamm · Stand: Monatsende · fiktive Trainingsdaten" |
| Inhaltsbereich | 16 | 72 | 1068 | 608 | alle Visuals liegen exakt hier drin |

## Seite 1 · Überblick

**Fragestellung:** Erreichen wir unsere Weiterbildungsziele 2025 – und wo müssen wir nachsteuern?

**Notizen:** Eine Seite für die GF. Details (Person, Kurs) bewusst nicht hier – personenbezogene Daten nur mit RLS.

### 1.1 Teilnahmequote `mk_wbt01`

- **Typ:** KPI-Kachel (ChartKitchen) (`kpi`) · **Engine:** ChartKitchen · ChartKitchen-Modus `cards` · natives Visual `card`
- **Position:** x=16, y=72, w=204, h=117 · **stabile ID:** `wbt01`
- **Untertitel / Einheit:** vs. Ziel
- **Datenrollen:**
  - Kennzahl: `_Measures.Teilnahmequote`
  - Ziel / Referenz: `_Measures.Ziel Teilnahmequote`
- **pbir-Buckets (card):** Values ← _Measures.Teilnahmequote
- **Analyse:** Polarität größer = besser (auto) · Δ-Basis PL (auto), Δ abs + rel · Einheit % · 1 Dezimalstellen
- **Workshop:** Must · Status abgestimmt
- **Notizen:** Anteil der Belegschaft mit mindestens einer freiwilligen Weiterbildung. Pflichtkurse zählen nicht mit.

### 1.2 Ø Stunden je MA `mk_wbt02`

- **Typ:** KPI-Kachel (ChartKitchen) (`kpi`) · **Engine:** ChartKitchen · ChartKitchen-Modus `cards` · natives Visual `card`
- **Position:** x=232, y=72, w=204, h=117 · **stabile ID:** `wbt02`
- **Untertitel / Einheit:** vs. Ziel
- **Datenrollen:**
  - Kennzahl: `_Measures.Ø Stunden je MA`
  - Ziel / Referenz: `_Measures.Ziel Ø Stunden je MA`
- **pbir-Buckets (card):** Values ← _Measures.Ø Stunden je MA
- **Analyse:** Polarität größer = besser (auto) · Δ-Basis PL (auto), Δ abs + rel · Einheit h · 1 Dezimalstellen
- **Workshop:** Must · Status abgestimmt
- **Notizen:** Nenner ist der Headcount – Personen ohne Weiterbildung ziehen den Schnitt bewusst nach unten.

### 1.3 Pflichtquote `mk_wbt03`

- **Typ:** KPI-Kachel (ChartKitchen) (`kpi`) · **Engine:** ChartKitchen · ChartKitchen-Modus `cards` · natives Visual `card`
- **Position:** x=448, y=72, w=204, h=117 · **stabile ID:** `wbt03`
- **Untertitel / Einheit:** alle 3 Pflichtkurse
- **Datenrollen:**
  - Kennzahl: `_Measures.Pflichtquote`
  - Ziel / Referenz: `_Measures.Ziel Pflichtquote`
- **pbir-Buckets (card):** Values ← _Measures.Pflichtquote
- **Analyse:** Polarität größer = besser (auto) · Δ-Basis PL (auto), Δ abs + rel · Einheit % · 1 Dezimalstellen
- **Workshop:** Must · Status abgestimmt
- **Notizen:** Compliance-relevant: Datenschutz, Arbeitsschutz, Verhaltenskodex. Ziel 95 %.

### 1.4 Kosten `mk_wbt04`

- **Typ:** KPI-Kachel (ChartKitchen) (`kpi`) · **Engine:** ChartKitchen · ChartKitchen-Modus `cards` · natives Visual `card`
- **Position:** x=664, y=72, w=204, h=117 · **stabile ID:** `wbt04`
- **Untertitel / Einheit:** vs. Budget
- **Datenrollen:**
  - Kennzahl: `_Measures.Kosten`
  - Ziel / Referenz: `_Measures.Budget`
- **pbir-Buckets (card):** Values ← _Measures.Kosten
- **Analyse:** Polarität kleiner = besser · Δ-Basis PL (auto), Δ abs + rel · Einheit € · Anzeige K · 0 Dezimalstellen
- **Workshop:** Must · Status abgestimmt
- **Notizen:** Weniger ist besser (Polarität gesetzt): Überschreitung = rot.

### 1.5 Ø Zufriedenheit `mk_wbt05`

- **Typ:** KPI-Kachel (ChartKitchen) (`kpi`) · **Engine:** ChartKitchen · ChartKitchen-Modus `cards` · natives Visual `card`
- **Position:** x=880, y=72, w=204, h=117 · **stabile ID:** `wbt05`
- **Untertitel / Einheit:** Skala 1–5
- **Datenrollen:**
  - Kennzahl: `_Measures.Ø Zufriedenheit`
  - Ziel / Referenz: `_Measures.Ziel Zufriedenheit`
- **pbir-Buckets (card):** Values ← _Measures.Ø Zufriedenheit
- **Analyse:** Polarität größer = besser (auto) · Δ-Basis PL (auto), Δ abs + rel · 2 Dezimalstellen
- **Workshop:** Must · Status abgestimmt
- **Notizen:** Mittelwert ist hier richtig: jede Bewertung zählt gleich. Nur abgeschlossene, bewertete Kurse.

### 1.6 Kosten vs. Budget je Quartal `mk_wbt07`

- **Typ:** Säulen (AC vs Referenz) (`columns`) · **Engine:** ChartKitchen · ChartKitchen-Modus `columns` · natives Visual `clusteredColumnChart`
- **Position:** x=16, y=201, w=348, h=233 · **stabile ID:** `wbt07`
- **Untertitel / Einheit:** in T€
- **Szenario:** AC/PL
- **Datenrollen:**
  - Zeit / Periode: `Kalender.Quartal`
  - AC · Ist-Wert: `_Measures.Kosten`
  - Referenz (PL / PY / BU): `_Measures.Budget`
- **pbir-Buckets (clusteredColumnChart):** Category ← Kalender.Quartal · Y ← _Measures.Kosten, _Measures.Budget
- **Analyse:** Polarität kleiner = besser · Δ-Basis PL, Δ abs + rel · Einheit T€ · Anzeige K · Granularität quarter
- **Kernaussage (Titelzeile):** Q2 sprengt das Budget – Vertriebsoffensive mit Premium-Seminaren
- **Workshop:** Must · Status abgestimmt
- **Notizen:** Budget liegt nur auf Quartalsebene vor – nie nach Monat zeigen.

### 1.7 Pflichtquote je Standort `mk_wbt08`

- **Typ:** Balken (Kategorien, sortiert) (`bars`) · **Engine:** ChartKitchen · ChartKitchen-Modus `bars` · natives Visual `clusteredBarChart`
- **Position:** x=376, y=201, w=348, h=233 · **stabile ID:** `wbt08`
- **Untertitel / Einheit:** in % vs. Ziel
- **Szenario:** AC/PL
- **Datenrollen:**
  - Kategorie / Achse: `dim_mitarbeitende.Standort`
  - AC · Ist-Wert: `_Measures.Pflichtquote`
  - Referenz (PL / PY / BU): `_Measures.Ziel Pflichtquote`
- **pbir-Buckets (clusteredBarChart):** Category ← dim_mitarbeitende.Standort · Y ← _Measures.Pflichtquote, _Measures.Ziel Pflichtquote
- **Analyse:** Polarität größer = besser (auto) · Δ-Basis PL, Δ abs · Einheit % · Sortierung value asc
- **Kernaussage (Titelzeile):** Werk Ulm hängt beim Datenschutz-E-Learning zurück
- **Workshop:** Must · Status abgestimmt
- **Notizen:** Drill-Idee: Standort → Bereich → Pflichtkurs. Ulm/Produktion hat kaum PC-Arbeitsplätze.

### 1.8 Ø Stunden je MA nach Bereich `mk_wbt09`

- **Typ:** Balken (Kategorien, sortiert) (`bars`) · **Engine:** ChartKitchen · ChartKitchen-Modus `bars` · natives Visual `clusteredBarChart`
- **Position:** x=736, y=201, w=348, h=233 · **stabile ID:** `wbt09`
- **Untertitel / Einheit:** in h vs. Ziel
- **Szenario:** AC/PL
- **Datenrollen:**
  - Kategorie / Achse: `dim_bereich.Bereich`
  - AC · Ist-Wert: `_Measures.Ø Stunden je MA`
  - Referenz (PL / PY / BU): `_Measures.Ziel Ø Stunden je MA`
- **pbir-Buckets (clusteredBarChart):** Category ← dim_bereich.Bereich · Y ← _Measures.Ø Stunden je MA, _Measures.Ziel Ø Stunden je MA
- **Analyse:** Polarität größer = besser (auto) · Δ-Basis PL, Δ abs · Einheit h · Sortierung delta asc
- **Workshop:** Must · Status abgestimmt
- **Notizen:** Ziel je Bereich unterschiedlich (IT 28 h, Logistik 12 h) – deshalb Abweichung statt Rangfolge.

### 1.9 Weiterbildungsstunden je Monat `mk_wbt11`

- **Typ:** Liniendiagramm (nativ) (`nline`) · **Engine:** Nativ · natives Visual `lineChart`
- **Position:** x=16, y=446, w=348, h=234 · **stabile ID:** `wbt11`
- **Untertitel / Einheit:** abgeschlossene Kurse
- **Datenrollen:**
  - Zeit / Periode: `Kalender.Monat`
  - Werte: `_Measures.Stunden`
- **pbir-Buckets (lineChart):** Category ← Kalender.Monat · Y ← _Measures.Stunden
- **Analyse:** Polarität größer = besser (auto) · Δ-Basis PL (auto), Δ abs + rel · Granularität month
- **Workshop:** Should · Status abgestimmt
- **Notizen:** Saisonmuster: Sommerloch und Dezember. Hilft bei der Kursplanung 2026.

### 1.10 Vollzeit vs. Teilzeit `mk_wbt12`

- **Typ:** Balkendiagramm (nativ) (`nbar`) · **Engine:** Nativ · natives Visual `clusteredBarChart`
- **Position:** x=376, y=446, w=348, h=234 · **stabile ID:** `wbt12`
- **Untertitel / Einheit:** Teilnahmequote · Ø Stunden
- **Datenrollen:**
  - Kategorie / Achse: `dim_mitarbeitende.Beschaeftigung`
  - Werte: `_Measures.Teilnahmequote`, `_Measures.Ø Stunden je MA`
- **pbir-Buckets (clusteredBarChart):** Category ← dim_mitarbeitende.Beschaeftigung · Y ← _Measures.Teilnahmequote, _Measures.Ø Stunden je MA
- **Analyse:** Polarität größer = besser (auto) · Δ-Basis PL (auto), Δ abs + rel
- **Kernaussage (Titelzeile):** Teilzeitkräfte kommen nur halb so oft zum Zug
- **Workshop:** Should · Status abgestimmt
- **Notizen:** Fairness-Frage für GF und Betriebsrat: Kurszeiten passen nicht zu Teilzeitmodellen?

### 1.11 Top-Kurse nach Kosten `mk_wbt13`

- **Typ:** Matrix (nativ) (`matrix`) · **Engine:** Nativ · natives Visual `pivotTable`
- **Position:** x=736, y=446, w=348, h=234 · **stabile ID:** `wbt13`
- **Untertitel / Einheit:** Teilnahmen · Kosten · Zufriedenheit
- **Datenrollen:**
  - Zeilen: `dim_kurs.Kurstitel`
  - Werte: `_Measures.Teilnahmen`, `_Measures.Kosten`, `_Measures.Ø Zufriedenheit`
- **pbir-Buckets (pivotTable):** Rows ← dim_kurs.Kurstitel · Values ← _Measures.Teilnahmen, _Measures.Kosten, _Measures.Ø Zufriedenheit
- **Analyse:** Polarität größer = besser (auto) · Δ-Basis PL (auto), Δ abs + rel · Sortierung value desc · Top 8
- **Workshop:** Could · Status abgestimmt
- **Notizen:** Kosten und Zufriedenheit nebeneinander: Welche teuren Kurse lohnen sich?

## Kennzahlen-Steckbrief (gebundene Felder)

| Feld | Alias (Fachbereich) | Definition laut Modell | Format | Einheit | Owner | Quelle | Ziel | bestätigt |
|---|---|---|---|---|---|---|---|---|
| `_Measures.Teilnahmequote` | Teilnahmequote | Personen mit ≥ 1 abgeschlossener freiwilliger Weiterbildung ÷ Headcount | 0.0% | % | Personalentwicklung | LMS + HR-Stamm | 75 % | ja |
| `_Measures.Ziel Teilnahmequote` | – | – | 0.0% | – | – | – | – | nein |
| `_Measures.Ø Stunden je MA` | Weiterbildungsstunden pro Kopf | Stunden ÷ Headcount (alle Personen, auch ohne Weiterbildung) | #,##0.0 | h | Personalentwicklung | LMS | je Bereich (12–28 h) | ja |
| `_Measures.Ziel Ø Stunden je MA` | – | nach Headcount gewichtet | #,##0.0 | – | – | – | – | nein |
| `_Measures.Pflichtquote` | Pflichtschulungsquote | Personen, die alle Pflichtkurse abgeschlossen haben ÷ Headcount | 0.0% | % | Compliance / Arbeitssicherheit | LMS + HR-Stamm | 95 % | ja |
| `_Measures.Ziel Pflichtquote` | – | – | 0.0% | – | – | – | – | nein |
| `_Measures.Kosten` | Weiterbildungskosten | Summe Kosten inkl. No-Show und Stornogebühren | #,##0 | € | Controlling | LMS (Kosten je Buchung) | ≤ Budget | nein |
| `_Measures.Budget` | – | – | #,##0 | – | – | – | – | nein |
| `_Measures.Ø Zufriedenheit` | Kurszufriedenheit | Mittelwert der Bewertungen 1–5 | 0.00 | 1–5 | Personalentwicklung | LMS-Feedback | 4,0 | ja |
| `_Measures.Ziel Zufriedenheit` | – | – | 0.0 | – | – | – | – | nein |
| `Kalender.Quartal` | – | – | – | – | – | – | – | nein |
| `dim_mitarbeitende.Standort` | – | – | – | – | – | – | – | nein |
| `dim_bereich.Bereich` | – | – | – | – | – | – | – | nein |
| `Kalender.Monat` | – | – | – | – | – | – | – | nein |
| `_Measures.Stunden` | – | Weiterbildungsstunden aus abgeschlossenen Buchungen | #,##0 | – | – | – | – | nein |
| `dim_mitarbeitende.Beschaeftigung` | – | Vollzeit / Teilzeit | – | – | – | – | – | nein |
| `dim_kurs.Kurstitel` | – | – | – | – | – | – | – | nein |
| `_Measures.Teilnahmen` | – | Buchungen mit Status abgeschlossen | #,##0 | – | – | – | – | nein |
| `dim_kurs.Kategorie` | – | – | – | – | – | – | – | nein |

## Regeln für die Umsetzung

- Positionen und Größen exakt übernehmen; nichts „optisch nachjustieren". Rundungen ±1 px sind ok.
- Visual-Namen im PBIR = `id` aus der Spec (stabil über Läufe hinweg); ein zweiter Lauf ist ein Delta, kein Neubau.
- Chrome-Zonen auf jeder Seite identisch anlegen; Nav-Buttons auf allen Seiten, aktive Seite als deaktivierter Akzent-Button.
- Kein Visual außerhalb des Inhaltsbereichs, keine Überlappung; Chrome-Zonen bleiben visualfrei.
- Text-Kacheln mit `content` als Shape mit Text bauen (Textbox per CLI bleibt leer).
- Analyse-Angaben je Kachel umsetzen: Polarität (invert), Δ-Basis, Sortierung, Top-N, Einheit/Dezimalen, Granularität; `auto`-Werte sind Vorschläge, keine Entscheidungen.
- ChartKitchen-Visuals nur über eine vorhandene Referenz-Instanz replizieren, nie visual.json raten. Fehlt die Instanz: Platzhalter und Hinweis.
- Native Visuals je Seite mit `pbir add visual "<Report>.Report/<Seite>.Page" --from-json pbir-visuals.<Seite>.json` anlegen; Visuals mit leeren Pflichtrollen sind dort nicht enthalten.
- Neue Felder zuerst im Semantikmodell anlegen (`te`), dann `te validate --errors-only`, erst danach binden. Umbenennungswünsche (Alias) nur nach Freigabe umsetzen.
- Farben/Schrift kommen aus dem Theme; dieser Brief regelt Struktur, Bindung und Design-Entscheidungen.