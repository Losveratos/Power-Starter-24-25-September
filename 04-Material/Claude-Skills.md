# Claude-Skills aus der ChartKitchen nutzen

In diesem Repo liegen die Claude-Skills der [Daten-WG Knowledge Kitchen](https://datenwgknowledgekitchen.com/).
Mit ihnen hilft dir **Claude Code**, aus einem Power-BI-Projekt einen fertigen Bericht zu planen:
Feld-Mapping vorschlagen, Visuals vorbereiten, Theme bauen, Deneb-Specs anpassen.

Alle Skills arbeiten im sicheren **„vorbereiten + Plan"-Modus**: Sie lesen dein Modell, zeigen dir
einen Plan und ändern erst nach deiner Freigabe etwas.

## Welcher Skill wofür?

| Du sagst zum Beispiel … | Skill |
|---|---|
| „Bau mir mit ChartKitchen einen Report aus meinen Daten" | `chartkitchen-report` |
| „Füg mir den Säulen-Varianz-Chart aus dem Chart-Builder in meinen Report ein" | `deploy-to-powerbi` |
| „Setz mein Mockup in Power BI um" | `mockup-to-powerbi` |
| „Mach mir eine GuV-Seite mit dem P&L-Visual" | `pnl-report` |
| „Bau mir ein Report-Layout / Theme aus unserer Webseite" · „Prüf mein Report-Design" | `powerbi-design-framework` |
| „Mein Deneb-Visual rendert nicht" · „Bau mir ein Vega-Lite-Spec" | `vega-charts` |

## So geht's

1. **Power-BI-Datei als Projekt speichern:** In Power BI Desktop **Datei → Speichern unter →
   Dateityp „Power BI-Projekt (*.pbip)"**. Dann liegen Bericht und Modell als lesbare Textdateien vor – damit können die Skills arbeiten.
   (Falls die Option fehlt: **Optionen → Vorschaufeatures → Power BI-Projektdateien speichern** einschalten.)
2. Den PBIP-Ordner **in dieses Repo legen** (oder dieses Repo neben deinen Projektordner klonen).
3. **Claude Code** im Repo-Ordner starten – im Terminal `claude` oder im Browser über [claude.ai/code](https://claude.ai/code) mit diesem Repo.
4. Einfach sagen, was du willst (siehe Tabelle). Claude erkennt den passenden Skill selbst.

## Zum Üben: das Trainingsmodell

Kein eigenes Modell zur Hand? Nimm das **Rad-&-Tat-Modell aus Tag 2** ([Übungen](../02-Tag-2/README.md)),
speichere es als PBIP und probier zum Beispiel:

- *„Bau mir mit ChartKitchen einen Monatsreport: Plan-Ist je Monat und Filialvergleich."*
  → nutzt `Umsatz`, `Plan`, `Δ Plan`, `Kalender[Monat]`, `dim_filiale[Filiale]`
- *„Mach mir eine GuV-Seite: Umsatz, Kosten, Deckungsbeitrag."* → `pnl-report`
- *„Gib dem Bericht ein ruhiges Theme mit einer Akzentfarbe und prüf den Kontrast."* → `powerbi-design-framework`

Die Zahlen kannst du gegen [`kontrollzahlen-tag1-tag2.json`](../_Werkzeuge/kontrollzahlen-tag1-tag2.json) prüfen.

## Die Custom Visuals

Einige Skills brauchen ein Custom Visual, das du einmal in Power BI Desktop importierst
(**Visualisierungen → … → Visual aus Datei importieren**):

| Visual | Download |
|---|---|
| ChartKitchen byDatenWG | [chartkitchen-byDatenWG-latest.pbiviz](https://github.com/Losveratos/PowerBI-Kitchen-/raw/main/downloads/chartkitchen-byDatenWG-latest.pbiviz) · [Schnellstart](https://datenwgknowledgekitchen.com/chartkitchen-schnellstart.html) |
| P&L Statement byDatenWG (Beta) | [pnlByDatenWG/dist](https://github.com/Losveratos/PowerBI-Kitchen-/tree/main/pnlByDatenWG/dist) |
| Gantt byDatenWG | [dataKitchenGantt/dist](https://github.com/Losveratos/PowerBI-Kitchen-/tree/main/dataKitchenGantt/dist) |

Web-Werkzeuge dazu: [Chart-Builder](https://datenwgknowledgekitchen.com/business-chart-builder.html) ·
[MockupKitchen](https://datenwgknowledgekitchen.com/mockup-kitchen.html) ·
[IBCS-Trainer](https://datenwgknowledgekitchen.com/ibcs-trainer.html)

## Aktualisieren (für Trainer:innen)

Die Skills werden in der Kitchen gepflegt. Neuen Stand holen:
```bash
tools/sync_kitchen_skills.sh
```
