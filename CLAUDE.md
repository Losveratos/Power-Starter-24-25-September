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
dort machen, dann `_Werkzeuge/sync_kitchen_skills.sh` laufen lassen. Nach dem Sync die Selbsttests prüfen:
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
**Rad & Tat GmbH** aus Tag 2 vorschlagen (`02-Tag-2/README.md`, Daten in `02-Tag-2/Daten/`). Wer das
Modell in Power BI Desktop als **PBIP** speichert (*Datei → Speichern unter → Power BI-Projekt*),
hat die Grundlage, die `chartkitchen-report`, `deploy-to-powerbi`, `pnl-report`,
`powerbi-design-framework` und `mockup-to-powerbi` erwarten.

Passende Abbildungen:
- **Plan-Ist je Monat** (Measures `Umsatz`, `Plan`, `Δ Plan`, `Δ Plan %`; Achse `Kalender[Monat]`) → ChartKitchen Säulen mit Varianz · Chart-Builder-Template `columns_variance`
- **Filialvergleich** (`dim_filiale[Filiale]` × `Umsatz`/`Plan`) → Balken-Struktur · `bars_structure`
- **Marge je Filiale/Kategorie** (`Marge %`, `Deckungsbeitrag`) → Monatsreport- oder Sales-Analyse-Blaupause
- **GuV-Light** (Umsatz → Kosten → Deckungsbeitrag) → `pnl-report`, reine Hierarchie
- Kontrollzahlen zum Gegenprüfen: `_Werkzeuge/kontrollzahlen-tag1-tag2.json`

## Ordnerstruktur (nicht ohne Rückfrage ändern – alle Raw-Links hängen daran)

```
00-Downloads/          ZIPs + PDFs für Teilnehmende (erzeugt)
01-Tag-1/              README = Übungen · Daten/ · Loesungen/
02-Tag-2/              README = Übungen · Daten/ · Loesungen/
03-Fall-Weiterbildung/ README = Anleitung · Daten/{1-Rohdaten,2-Anreicherung,3-Ziele} · Loesungen/{PowerQuery,DAX} · Mockup/ · PowerBI-Loesung/
04-Material/           Agenda · Handout · Videos · Claude-Skills · Snippets/
_Werkzeuge/            Generatoren, PBIP-Bau und -Prüfung, Download-Bau, Skill-Sync (nur Trainer)
```

Jeder Ordner hat eine `README.md` – GitHub zeigt sie beim Öffnen an. Neue Inhalte in dieses Schema einsortieren;
ein neuer Fall wird `05-Fall-<Name>/` mit derselben Innenstruktur wie der Weiterbildungs-Fall.

## Erzeugte Dateien

- **Daten:** nur über `_Werkzeuge/tag-daten_erzeugen.py` bzw. `_Werkzeuge/fall-weiterbildung/generate_data.py` ändern, danach Kontrollzahlen in den Anleitungen abgleichen.
- **Mockup:** `_Werkzeuge/fall-weiterbildung/build_mockup.py` (braucht einen Klon der Kitchen daneben). `03-Fall-Weiterbildung/Mockup/mockup-spec.json` ist eine gültige Eingabe für `mockup-to-powerbi`.
- **PBIP:** `03-Fall-Weiterbildung/PowerBI-Loesung/` erzeugt `_Werkzeuge/pbip/build_weiterbildung_pbip.py` – Modell per TOM geprüft (`_Werkzeuge/pbip/TmdlCheck`, .NET 8), Bericht per `_Werkzeuge/pbip/validate_pbir.py` (Microsoft-Schemas + Feldbezüge). Wenn `te`/`pbir` verfügbar sind, zusätzlich `PowerBI-Loesung/pruefen.ps1` – die CLIs haben Vorrang.
- **Downloads:** `_Werkzeuge/downloads_bauen.py` – **nach jeder Änderung an Übungen, Material, Daten, Fall oder PBIP neu bauen**, sonst laden Teilnehmende einen alten Stand.

## Konventionen im Repo

- Sprache Deutsch, Anrede „du".
- Änderungen direkt auf `main` pushen (Wunsch des Repo-Owners).
- Neue Snippets nach `04-Material/Snippets/` (Regeln in der README dort).
- Keine echten Firmen- oder Personendaten einchecken – das Repo ist öffentlich.
