# Werkzeuge · nur für Trainer:innen

Teilnehmende brauchen diesen Ordner nicht. Hier liegt alles, womit Daten, Mockup, Power-BI-Projekt
und Download-Pakete erzeugt werden. **Erzeugte Dateien nie von Hand ändern** – Skript anpassen und neu laufen lassen.

| Werkzeug | Erzeugt | Aufruf (aus dem Repo-Root) |
|---|---|---|
| `tag-daten_erzeugen.py` | `01-Tag-1/Daten`, `02-Tag-2/Daten`, `kontrollzahlen-tag1-tag2.json` | `python3 _Werkzeuge/tag-daten_erzeugen.py` |
| `fall-weiterbildung/generate_data.py` | `03-Fall-Weiterbildung/Daten` inkl. Kontrollzahlen | `python3 _Werkzeuge/fall-weiterbildung/generate_data.py` |
| `fall-weiterbildung/build_mockup.py` | `03-Fall-Weiterbildung/Mockup` (mit der echten MockupKitchen) | `python3 _Werkzeuge/fall-weiterbildung/build_mockup.py ../PowerBI-Kitchen-` |
| `pbip/build_weiterbildung_pbip.py` | `03-Fall-Weiterbildung/PowerBI-Loesung` (Modell per TOM geprüft) | siehe [`pbip/README.md`](pbip/README.md) |
| `downloads_bauen.py` | `00-Downloads` (PDFs + ZIPs) | `python3 _Werkzeuge/downloads_bauen.py` |
| `sync_kitchen_skills.sh` | `.claude/skills` aus der Knowledge Kitchen | `_Werkzeuge/sync_kitchen_skills.sh` |

**Reihenfolge nach Änderungen:** Daten → Mockup → PBIP → Downloads. Danach Kontrollzahlen in den Anleitungen abgleichen.

Benötigt: Python 3 mit `openpyxl`, `playwright`, `markdown`, `jsonschema`; für das PBIP zusätzlich .NET 8 SDK.

Mehr zu den Übungsdaten (Geschichte in den Daten, Kontrollzahlen): [`daten-tag1-tag2.md`](daten-tag1-tag2.md).
