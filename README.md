# Power BI Starter-Training · 24.–25. September

Alles für das zweitägige Einsteiger-Training an einem Ort: Ablauf, Übungen mit Kontrollzahlen,
Übungsdaten zum direkten Laden in Power BI, Code-Snippets und Videos zum Weiterlernen.
Nach dem Training kommen hier weitere Snippets und Dateien dazu – einfach wieder vorbeischauen.

## ⬇️ Herunterladen – ein Klick, kein GitHub-Wissen nötig

| | Paket | Was drin ist |
|---|---|---|
| 📘 | **[Tag 1 herunterladen (ZIP)](https://github.com/Losveratos/Power-Starter-24-25-September/raw/main/downloads/Starter-Training-Tag1.zip)** | Übungen als PDF, Übungsdaten, Lösung, Handout, Agenda |
| 📗 | **[Tag 2 herunterladen (ZIP)](https://github.com/Losveratos/Power-Starter-24-25-September/raw/main/downloads/Starter-Training-Tag2.zip)** | Übungen als PDF, Daten (CSV + Excel), Lösungen, Handout, Agenda |
| 📄 | [Handout (PDF)](https://github.com/Losveratos/Power-Starter-24-25-September/raw/main/downloads/Handout.pdf) · [Agenda (PDF)](https://github.com/Losveratos/Power-Starter-24-25-September/raw/main/downloads/Agenda.pdf) | zum direkten Öffnen oder Ausdrucken |
| 🧩 | [Fall Weiterbildungs-Monitoring (ZIP)](https://github.com/Losveratos/Power-Starter-24-25-September/raw/main/downloads/Fall-Weiterbildungs-Monitoring.zip) | Anleitung als PDF, Rohdaten, Ziele-Excel, Lösungsskripte, Mockup |
| 📊 | [Fertige Lösung als Power-BI-Datei (ZIP)](https://github.com/Losveratos/Power-Starter-24-25-September/raw/main/downloads/Loesung-Weiterbildungs-Monitoring-PowerBI.zip) | Power-BI-Projekt zum Doppelklicken |
| 📦 | [Alles auf einmal (ZIP)](https://github.com/Losveratos/Power-Starter-24-25-September/archive/refs/heads/main.zip) | das komplette Repo |

**So geht's:** Link anklicken → die Datei landet im Ordner *Downloads* → **Rechtsklick → „Alle extrahieren…" → „Extrahieren"** →
im entpackten Ordner zuerst `LIESMICH.txt` öffnen. Wichtig: nicht direkt aus der ZIP heraus arbeiten.

## 🧭 Wo finde ich was?

| | Inhalt |
|---|---|
| 📅 [**Agenda**](agenda.md) | Ablauf beider Tage mit Zeiten und Übungen |
| 🛠 [**Übungen Tag 1**](uebungen/tag1.md) | Vom Kassen-Export zum ersten Bericht – Power Query, Visuals, Filter |
| 🛠 [**Übungen Tag 2**](uebungen/tag2.md) | Sternschema, Kalender, DAX-Measures, Plan-Ist |
| 📄 [**Handout**](handout.md) | Das Wichtigste auf zwei Seiten: Regeln, DAX-Funktionen, Glossar |
| 📦 [**Daten**](daten/) | Übungsdaten der fiktiven Rad & Tat GmbH (CSV + Excel) |
| ✂️ [**Snippets**](snippets/) | Power-Query- und DAX-Code zum Kopieren |
| 🎬 [**Videos**](videos.md) | Daten-WG-Videos zum Vertiefen, sortiert nach Thema |
| 🧩 [**Fall: Weiterbildungs-Monitoring**](cases/weiterbildungs-monitoring/) | Zum Selbermachen: Rohdaten, Anreicherung, Ziele-Kreuztabelle, Skripte, Anleitung und Seiten-Mockup |
| 📊 [**Power-BI-Projekt**](pbip/Weiterbildungs-Monitoring/) | Fertige Lösung zum Weiterbildungs-Fall als PBIP (Modell + Berichtsseite) |
| 🤖 [**Claude-Skills**](skills.md) | Die ChartKitchen-Skills für Claude Code – Report, Design, Deneb, P&L, Mockup |

## ⚡ Schnellstart

1. **Power BI Desktop** installieren (Windows; Microsoft Store → „Power BI Desktop").
2. Power BI öffnen → **Daten abrufen → Web** → diese Adresse → **Anonym**:
   ```
   https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/daten/tag1/verkaeufe_2025_roh.csv
   ```
3. Weiter mit [Übung 1](uebungen/tag1.md#übung-1--daten-anbinden-15-min).

## 📁 Aufbau

```
agenda.md              Ablauf
handout.md             Teilnehmer-Handout
videos.md              Videoempfehlungen
uebungen/              Übungsblätter Tag 1 + Tag 2
daten/                 Übungsdaten + kontrollzahlen.json
  tag1/                  unordentlicher Kassen-Export
  tag2/                  Sternschema + Plan (Excel)
snippets/              Power Query (.pq) und DAX (.dax) zum Kopieren
pbip/                  fertige Power-BI-Projekte (PBIP) als Lösungen
cases/                 Fälle zum Selbermachen (je Fall: daten/, skripte/, mockup/, README)
tools/generate_data.py erzeugt die Übungsdaten neu
tools/sync_kitchen_skills.sh  holt die Skills aus der Kitchen
tools/pbip/            erzeugt und prüft die PBIP-Projekte (TOM + Microsoft-Schemas)
.claude/skills/        Claude-Skills aus der ChartKitchen (siehe skills.md)
CLAUDE.md              Hinweise für Claude Code in diesem Repo
```

## 🔗 Weiterlernen

- [Praxis-Pfad: Dein erstes Dashboard](https://datenwgknowledgekitchen.com/powerbi_praxis_pfad.html) – Tag 1 zum Wiederholen, allein, ≈ 2 h
- [Power BI von A bis Z – Einsteiger-Guide](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html)
- [Daten-WG Knowledge Kitchen](https://datenwgknowledgekitchen.com/) · [YouTube @Daten-WG](https://www.youtube.com/@Daten-WG)

---
Alle Daten sind simuliert. Inhalte unter [MIT-Lizenz](LICENSE).
