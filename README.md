# Power BI Starter-Training · 24.–25. September

Alles für das zweitägige Einsteiger-Training an einem Ort: Ablauf, Übungen mit Kontrollzahlen,
Übungsdaten zum direkten Laden in Power BI, Code-Snippets und Videos zum Weiterlernen.
Nach dem Training kommen hier weitere Snippets und Dateien dazu – einfach wieder vorbeischauen.

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
cases/                 Fälle zum Selbermachen (je Fall: daten/, skripte/, mockup/, README)
tools/generate_data.py erzeugt die Übungsdaten neu
tools/sync_kitchen_skills.sh  holt die Skills aus der Kitchen
.claude/skills/        Claude-Skills aus der ChartKitchen (siehe skills.md)
CLAUDE.md              Hinweise für Claude Code in diesem Repo
```

## 🔗 Weiterlernen

- [Praxis-Pfad: Dein erstes Dashboard](https://datenwgknowledgekitchen.com/powerbi_praxis_pfad.html) – Tag 1 zum Wiederholen, allein, ≈ 2 h
- [Power BI von A bis Z – Einsteiger-Guide](https://datenwgknowledgekitchen.com/power_bi_einsteiger_guide_v4.html)
- [Daten-WG Knowledge Kitchen](https://datenwgknowledgekitchen.com/) · [YouTube @Daten-WG](https://www.youtube.com/@Daten-WG)

---
Alle Daten sind simuliert. Inhalte unter [MIT-Lizenz](LICENSE).
