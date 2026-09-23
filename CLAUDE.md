# Power BI Starter-Training · Hinweise für Claude

Dieses Repo ist der Austausch-Ort für das Power-BI-Starter-Training (24.–25.09.): Agenda, Übungen,
Übungsdaten, Snippets. Zusätzlich liegen hier die **Claude-Skills aus der Daten-WG Knowledge
Kitchen** (`.claude/skills/`), damit Teilnehmende und Trainer:innen sie direkt in diesem Repo nutzen können.

## Skills

| Skill | Wofür |
|---|---|
| `chartkitchen-report` | IBCS-Report mit dem Custom Visual *ChartKitchen byDatenWG* planen und vorbereiten |
| `deploy-to-powerbi` | Chart-Builder-Templates (Deneb) in eine PBIP-Datei einsetzen |
| `mockup-to-powerbi` | Eine MockupKitchen-Skizze in ein PBIP-Projekt übertragen |
| `pnl-report` | GuV-/P&L-Seite mit *P&L Statement byDatenWG* |
| `powerbi-design-framework` | Theme, Seitenraster, Navigation, Design-Linter |
| `vega-charts` | Vega/Vega-Lite/Deneb-Specs bauen und debuggen |

**Nicht hier ändern.** Quelle der Wahrheit ist das Repo `Losveratos/PowerBI-Kitchen-`. Änderungen
dort machen, dann `tools/sync_kitchen_skills.sh` laufen lassen. Nach dem Sync die Selbsttests prüfen:
`python3 .claude/skills/mockup-to-powerbi/tests/run_tests.py`.

## Dateien, die die Skills in der Kitchen erwarten

Die Skills nennen manche Pfade aus dem Kitchen-Repo. Hier im Starter-Repo gibt es sie nicht. Dann
nicht suchen, sondern auf diese Quellen verweisen:

| Pfad im Skill | Hier stattdessen |
|---|---|
| `ibcsInspiredChartDeck/…` (ChartKitchen-Visual, `capabilities.json`, `src/settings.ts`) | https://github.com/Losveratos/PowerBI-Kitchen-/tree/main/ibcsInspiredChartDeck · aktueller Build: https://github.com/Losveratos/PowerBI-Kitchen-/blob/main/downloads/chartkitchen-byDatenWG-latest.pbiviz |
| `pnlByDatenWG/…` inkl. `dist/*.pbiviz` | https://github.com/Losveratos/PowerBI-Kitchen-/tree/main/pnlByDatenWG |
| `dataKitchenGantt/…` inkl. `dist/*.pbiviz` | https://github.com/Losveratos/PowerBI-Kitchen-/tree/main/dataKitchenGantt |
| Chart-Builder (`business-chart-builder.html`) | https://datenwgknowledgekitchen.com/business-chart-builder.html |
| MockupKitchen (`mockup-kitchen.html`, `assets/mockup/…`) | https://datenwgknowledgekitchen.com/mockup-kitchen.html |
| `assets/vega/` | nur für Kitchen-Webseiten relevant; für Deneb in Power BI nicht nötig |

Zum Lesen von `capabilities.json` o. ä. reicht die Raw-Adresse
`https://raw.githubusercontent.com/Losveratos/PowerBI-Kitchen-/main/<pfad>`.

## Trainingsdaten als Beispiel für die Skills

Wenn jemand einen Skill ausprobieren will und kein eigenes Modell hat, das Trainingsmodell der
**Rad & Tat GmbH** aus Tag 2 vorschlagen (`uebungen/tag2.md`, Daten in `daten/tag2/`). Wer das
Modell in Power BI Desktop als **PBIP** speichert (*Datei → Speichern unter → Power BI-Projekt*),
hat die Grundlage, die `chartkitchen-report`, `deploy-to-powerbi`, `pnl-report`,
`powerbi-design-framework` und `mockup-to-powerbi` erwarten.

Passende Abbildungen:
- **Plan-Ist je Monat** (Measures `Umsatz`, `Plan`, `Δ Plan`, `Δ Plan %`; Achse `Kalender[Monat]`) → ChartKitchen Säulen mit Varianz · Chart-Builder-Template `columns_variance`
- **Filialvergleich** (`dim_filiale[Filiale]` × `Umsatz`/`Plan`) → Balken-Struktur · `bars_structure`
- **Marge je Filiale/Kategorie** (`Marge %`, `Deckungsbeitrag`) → Monatsreport- oder Sales-Analyse-Blaupause
- **GuV-Light** (Umsatz → Kosten → Deckungsbeitrag) → `pnl-report`, reine Hierarchie
- Kontrollzahlen zum Gegenprüfen: `daten/kontrollzahlen.json`

## Fälle (`cases/`)

Jeder Fall ist in sich geschlossen: `README.md` (Anleitung mit Kontrollzahlen), `daten/` (roh · anreicherung ·
ziele + `kontrollzahlen.json`), `skripte/` (Power Query + DAX zum Überspringen), `mockup/` (MockupKitchen-Export),
`tools/` (Generatoren). Kontrollzahlen nie von Hand ändern – Generator laufen lassen und Anleitung abgleichen.
Das Mockup `cases/weiterbildungs-monitoring/mockup/mockup-spec.json` ist eine gültige Eingabe für `mockup-to-powerbi`.

## Power-BI-Projekte (`pbip/`)

`pbip/Weiterbildungs-Monitoring/` wird von `tools/pbip/build_weiterbildung_pbip.py` erzeugt – nicht von Hand ändern,
sondern das Skript anpassen und neu laufen lassen. Das Skript prüft das Modell mit TOM (`tools/pbip/TmdlCheck`, .NET 8);
danach `tools/pbip/validate_pbir.py` (Microsoft-Schemas + Feldbezüge). Wenn `te`/`pbir` verfügbar sind,
zusätzlich `pbip/Weiterbildungs-Monitoring/pruefen.ps1` – die CLIs haben Vorrang vor den eigenen Prüfungen.

## Download-Pakete (`downloads/`)

ZIPs und PDFs für Teilnehmende ohne GitHub-Kenntnisse, erzeugt von `tools/build_downloads.py`
(PDFs aus den Markdown-Dateien). **Nach jeder Änderung an Übungen, Handout, Agenda, Daten, Fall oder PBIP
neu bauen**, sonst laden Teilnehmende einen alten Stand. Die Links auf der Startseite zeigen auf `raw/main/downloads/…`.

## Konventionen im Repo

- Sprache Deutsch, Anrede „du".
- Neue Snippets nach `snippets/` (Regeln in `snippets/README.md`), Daten nach `daten/`.
- Übungsdaten nur über `tools/generate_data.py` ändern und danach Kontrollzahlen in den Übungsblättern abgleichen.
- Keine echten Firmen- oder Personendaten einchecken – das Repo ist öffentlich.
