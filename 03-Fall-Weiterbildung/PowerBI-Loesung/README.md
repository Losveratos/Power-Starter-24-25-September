# Power-BI-Projekt · Weiterbildungs-Monitoring

Die **fertige Lösung** zum [Fall Weiterbildungs-Monitoring](../) als
Power-BI-Projekt (PBIP): Modell mit allen Abfragen, Beziehungen und Measures plus die Berichtsseite „Überblick"
nach dem [Mockup](../Mockup/page-1-uberblick.png).

## Öffnen

1. [**Projekt als ZIP herunterladen**](https://github.com/Losveratos/Power-Starter-24-25-September/raw/main/00-Downloads/Loesung-Weiterbildungs-Monitoring-PowerBI.zip) → Rechtsklick → *Alle extrahieren* – **alle** Unterordner werden gebraucht, nicht aus der ZIP heraus öffnen.
2. `Weiterbildungs-Monitoring.pbip` doppelklicken → öffnet sich in Power BI Desktop (aktuelle Version, Windows).
3. Das Projekt enthält **keine Daten**, nur die Bauanleitung. Also: **Start → Aktualisieren**.
   Bei der Frage nach Anmeldedaten für `raw.githubusercontent.com` → **Anonym** → **Verbinden**.
   Bei der Frage nach Datenschutzebenen → **Öffentlich**.
4. Fertig. Die Zahlen müssen zu den Kontrollzahlen passen (siehe unten).

> Die Daten kommen direkt aus diesem GitHub-Repo (Branch `main`). Der Parameter **`DatenQuelle`**
> (*Daten transformieren → Parameter verwalten*) enthält die Basis-Adresse. Wer offline arbeiten will,
> legt einen eigenen Web-Server an oder stellt die Abfragen auf *Datei* um.

## Was drin ist

**Modell** (`Weiterbildungs-Monitoring.SemanticModel/`, TMDL)

| Tabelle | Inhalt | Quelle |
|---|---|---|
| `fakt_buchungen` | 1.712 Buchungen, bereinigt | LMS-Rohexport (Schritt 2 des Falls) |
| `dim_mitarbeitende` · `dim_bereich` · `dim_kurs` | HR-Stamm, Bereiche, Kurskatalog | Anreicherung |
| `Budget` · `Zielwerte` | entpivotierte Kreuztabellen | `ziele_2025.xlsx` |
| `Kalender` | 2025, als Datumstabelle markiert | in M erzeugt |
| `_Measures` | 29 Measures in 4 Ordnern | [`measures.dax`](../Loesungen/DAX/measures.dax) |

Automatisches Datum/Uhrzeit ist aus, implizite Measures sind abgeschaltet (*discourageImplicitMeasures*) –
jede Zahl im Bericht kommt aus einem Measure.

**Bericht** (`Weiterbildungs-Monitoring.Report/`, PBIR) – eine Seite, 1280 × 720, Positionen 1:1 aus dem Mockup
([Wireframe aus den Berichtsdateien](wireframe-ueberblick.svg)):

- Kopfband, Fußleiste, Filterbereich mit vier Dropdown-Slicern (Standort, Bereich, Beschäftigung, Kategorie)
- fünf Karten mit **dynamischem Untertitel** (Ziel und Abweichung kommen aus Measures)
- Kosten vs. Budget je Quartal · Pflichtquote je Standort · Ø Stunden je Bereich (jeweils Ist vs. Ziel)
- Stunden je Monat · Vollzeit vs. Teilzeit · Kurse nach Kosten
- eigenes Theme `Weiterbildung.json` (Ist dunkelgrau, Ziel hellgrau, Teal/Rot für gut/schlecht)

Nur Standard-Visuals, keine Custom Visuals – läuft in jedem Tenant.

## Kontrollzahlen nach dem Aktualisieren

| Karte | Wert | Untertitel |
|---|---:|---|
| Teilnahmequote | 63,3 % | Ziel 75,0 % · Δ −11,7 Pp |
| Ø Stunden je MA | 16,4 | Ziel 16,5 h · Δ −0,1 h |
| Pflichtquote | 79,5 % | Ziel 95,0 % · Δ −15,5 Pp |
| Kosten | 272.679 € | Budget 274.500 € · 99,3 % ausgeschöpft |
| Ø Zufriedenheit | 3,78 | Ziel 4,0 |

Pflichtquote Werk Ulm **58,6 %** · Q2 Kosten **116.223 €** bei 77.000 € Budget · Teilzeit Teilnahmequote **37,3 %**.
Alle Zahlen: [`kontrollzahlen.json`](../Daten/kontrollzahlen.json).

## Wie es gebaut und geprüft wurde

Erzeugt mit [`_Werkzeuge/pbip/build_weiterbildung_pbip.py`](../../_Werkzeuge/pbip/build_weiterbildung_pbip.py), ohne Handarbeit an den Dateien:

- **Modell:** mit der Microsoft-Bibliothek **TOM** (`Microsoft.AnalysisServices`, dieselbe Basis wie Tabular Editor)
  eingelesen, geprüft (Beziehungen, Datentypen, Datumstabelle, Sortierung) und als TMDL kanonisch neu geschrieben.
- **Bericht:** jede Datei gegen die **offiziellen Microsoft-JSON-Schemas** validiert, jeder Feldbezug gegen das Modell
  geprüft (wie `pbir validate --fields`). Visual-Aufbau nach echten Desktop-Exporten.

**Noch nicht gelaufen:** die CLIs `te` und `pbir` selbst – in der Umgebung, in der das Projekt entstand, gibt es sie nicht
(`pbir-cli` nur für Windows/macOS, `te` nur mit Tabular-Editor-Konto). Unter Windows prüfst du mit
[`pruefen.ps1`](pruefen.ps1). **Und: einmal in Power BI Desktop öffnen und aktualisieren**, bevor du das Projekt weitergibst.

## Weiterarbeiten

- Als `.pbix` speichern: *Datei → Speichern unter → Power BI-Datei*.
- Mit Claude Code in diesem Repo weiterbauen: z. B. `powerbi-design-framework` für ein Theme nach Firmen-CI oder
  `chartkitchen-report`, um die Karten und Varianzen mit ChartKitchen zu zeichnen (siehe [Claude-Skills](../../04-Material/Claude-Skills.md)).
