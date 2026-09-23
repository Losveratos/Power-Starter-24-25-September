# Workshop-Dokumentation · Weiterbildungs-Monitoring 2025

Stand: 2026-09-23 · Version 0.1 · Spec-Hash `cb7b3760` · erstellt mit MockupKitchen byDatenWG 0.4

| | |
|---|---|
| Teilnehmende | Personalentwicklung, Controlling, Betriebsrat (Datenschutz), Standortleitungen |
| Zielgruppe | Geschäftsführung, Personalentwicklung, Betriebsrat |
| Ziel des Berichts | Monatlicher Blick, ob die Weiterbildungsziele 2025 erreicht werden und das Budget hält. |
| Entscheidung | Wo steuern wir nach: Pflichtschulungen nachholen (Werk Ulm), Budget umschichten (Vertrieb), Kursangebot für Teilzeit öffnen? |
| Datenstand / Aktualisierung | monatlich, LMS-Export zum Monatsersten |
| Seiten | Überblick |
| Datenmodell | Weiterbildungs-Monitoring (Trainingsmodell, 03-Fall-Weiterbildung) (8 Tabellen) |

## Entscheidungen zur Gestaltung

- Format 1280 × 720 px (HD).
- Kopfband „Weiterbildungs-Monitoring 2025" · Muster Maschinenbau GmbH · Personalentwicklung, Stil dark, Logo links.
- Filter als Panel rechts: Standort, Bereich, Beschaeftigung, Kategorie.
- Fußleiste „Quelle: LMS-Export + HR-Stamm · Stand: Monatsende · fiktive Trainingsdaten".
- Kacheln gerundet (8 px), mit feinem Rahmen, Seitenhintergrund #F4F4F1, Akzent #C25A2D.

## Seite 1 · Überblick

**Fragestellung:** Erreichen wir unsere Weiterbildungsziele 2025 – und wo müssen wir nachsteuern?

**Notizen:** Eine Seite für die GF. Details (Person, Kurs) bewusst nicht hier – personenbezogene Daten nur mit RLS.

| # | Kachel | Darstellung | Felder | Analyse | Prio | Status | Notizen |
|---|---|---|---|---|---|---|---|
| 1.1 | Teilnahmequote (vs. Ziel) | KPI-Kachel (ChartKitchen), ChartKitchen | Kennzahl: Teilnahmequote; Ziel / Referenz: Ziel Teilnahmequote | % | Must | abgestimmt | Anteil der Belegschaft mit mindestens einer freiwilligen Weiterbildung. Pflichtkurse zählen nicht mit. |
| 1.2 | Ø Stunden je MA (vs. Ziel) | KPI-Kachel (ChartKitchen), ChartKitchen | Kennzahl: Ø Stunden je MA; Ziel / Referenz: Ziel Ø Stunden je MA | h | Must | abgestimmt | Nenner ist der Headcount – Personen ohne Weiterbildung ziehen den Schnitt bewusst nach unten. |
| 1.3 | Pflichtquote (alle 3 Pflichtkurse) | KPI-Kachel (ChartKitchen), ChartKitchen | Kennzahl: Pflichtquote; Ziel / Referenz: Ziel Pflichtquote | % | Must | abgestimmt | Compliance-relevant: Datenschutz, Arbeitsschutz, Verhaltenskodex. Ziel 95 %. |
| 1.4 | Kosten (vs. Budget) | KPI-Kachel (ChartKitchen), ChartKitchen | Kennzahl: Kosten; Ziel / Referenz: Budget | kleiner = besser, € | Must | abgestimmt | Weniger ist besser (Polarität gesetzt): Überschreitung = rot. |
| 1.5 | Ø Zufriedenheit (Skala 1–5) | KPI-Kachel (ChartKitchen), ChartKitchen | Kennzahl: Ø Zufriedenheit; Ziel / Referenz: Ziel Zufriedenheit | – | Must | abgestimmt | Mittelwert ist hier richtig: jede Bewertung zählt gleich. Nur abgeschlossene, bewertete Kurse. |
| 1.6 | Kosten vs. Budget je Quartal (in T€)<br>_Q2 sprengt das Budget – Vertriebsoffensive mit Premium-Seminaren_ | Säulen (AC vs Referenz), AC/PL, ChartKitchen | Zeit / Periode: Quartal; AC · Ist-Wert: Kosten; Referenz (PL / PY / BU): Budget | kleiner = besser, T€ | Must | abgestimmt | Budget liegt nur auf Quartalsebene vor – nie nach Monat zeigen. |
| 1.7 | Pflichtquote je Standort (in % vs. Ziel)<br>_Werk Ulm hängt beim Datenschutz-E-Learning zurück_ | Balken (Kategorien, sortiert), AC/PL, ChartKitchen | Kategorie / Achse: Standort; AC · Ist-Wert: Pflichtquote; Referenz (PL / PY / BU): Ziel Pflichtquote | sortiert nach value, % | Must | abgestimmt | Drill-Idee: Standort → Bereich → Pflichtkurs. Ulm/Produktion hat kaum PC-Arbeitsplätze. |
| 1.8 | Ø Stunden je MA nach Bereich (in h vs. Ziel) | Balken (Kategorien, sortiert), AC/PL, ChartKitchen | Kategorie / Achse: Bereich; AC · Ist-Wert: Ø Stunden je MA; Referenz (PL / PY / BU): Ziel Ø Stunden je MA | sortiert nach delta, h | Must | abgestimmt | Ziel je Bereich unterschiedlich (IT 28 h, Logistik 12 h) – deshalb Abweichung statt Rangfolge. |
| 1.9 | Weiterbildungsstunden je Monat (abgeschlossene Kurse) | Liniendiagramm (nativ) | Zeit / Periode: Monat; Werte: Stunden | – | Should | abgestimmt | Saisonmuster: Sommerloch und Dezember. Hilft bei der Kursplanung 2026. |
| 1.10 | Vollzeit vs. Teilzeit (Teilnahmequote · Ø Stunden)<br>_Teilzeitkräfte kommen nur halb so oft zum Zug_ | Balkendiagramm (nativ) | Kategorie / Achse: Beschaeftigung; Werte: Teilnahmequote, Ø Stunden je MA | – | Should | abgestimmt | Fairness-Frage für GF und Betriebsrat: Kurszeiten passen nicht zu Teilzeitmodellen? |
| 1.11 | Top-Kurse nach Kosten (Teilnahmen · Kosten · Zufriedenheit) | Matrix (nativ) | Zeilen: Kurstitel; Werte: Teilnahmen, Kosten, Ø Zufriedenheit | sortiert nach value, Top 8 | Could | abgestimmt | Kosten und Zufriedenheit nebeneinander: Welche teuren Kurse lohnen sich? |

## Kennzahlen-Steckbrief

| Feld | Heißt beim Fachbereich | Definition laut Modell | Einheit | Ziel | Owner | Quelle | bestätigt |
|---|---|---|---|---|---|---|---|
| _Measures.Teilnahmequote | Teilnahmequote | Personen mit ≥ 1 abgeschlossener freiwilliger Weiterbildung ÷ Headcount | % | 75 % | Personalentwicklung | LMS + HR-Stamm | ☑ |
| _Measures.Ziel Teilnahmequote | – | [ausfüllen] | 0.0% | – | – | – | ☐ |
| _Measures.Ø Stunden je MA | Weiterbildungsstunden pro Kopf | Stunden ÷ Headcount (alle Personen, auch ohne Weiterbildung) | h | je Bereich (12–28 h) | Personalentwicklung | LMS | ☑ |
| _Measures.Ziel Ø Stunden je MA | – | nach Headcount gewichtet | #,##0.0 | – | – | – | ☐ |
| _Measures.Pflichtquote | Pflichtschulungsquote | Personen, die alle Pflichtkurse abgeschlossen haben ÷ Headcount | % | 95 % | Compliance / Arbeitssicherheit | LMS + HR-Stamm | ☑ |
| _Measures.Ziel Pflichtquote | – | [ausfüllen] | 0.0% | – | – | – | ☐ |
| _Measures.Kosten | Weiterbildungskosten | Summe Kosten inkl. No-Show und Stornogebühren | € | ≤ Budget | Controlling | LMS (Kosten je Buchung) | ☐ |
| _Measures.Budget | – | [ausfüllen] | #,##0 | – | – | – | ☐ |
| _Measures.Ø Zufriedenheit | Kurszufriedenheit | Mittelwert der Bewertungen 1–5 | 1–5 | 4,0 | Personalentwicklung | LMS-Feedback | ☑ |
| _Measures.Ziel Zufriedenheit | – | [ausfüllen] | 0.0 | – | – | – | ☐ |
| Kalender.Quartal | – | [ausfüllen] | – | – | – | – | ☐ |
| dim_mitarbeitende.Standort | – | [ausfüllen] | – | – | – | – | ☐ |
| dim_bereich.Bereich | – | [ausfüllen] | – | – | – | – | ☐ |
| Kalender.Monat | – | [ausfüllen] | – | – | – | – | ☐ |
| _Measures.Stunden | – | Weiterbildungsstunden aus abgeschlossenen Buchungen | #,##0 | – | – | – | ☐ |
| dim_mitarbeitende.Beschaeftigung | – | Vollzeit / Teilzeit | – | – | – | – | ☐ |
| dim_kurs.Kurstitel | – | [ausfüllen] | – | – | – | – | ☐ |
| _Measures.Teilnahmen | – | Buchungen mit Status abgeschlossen | #,##0 | – | – | – | ☐ |
| dim_kurs.Kategorie | – | [ausfüllen] | – | – | – | – | ☐ |

## Offene Punkte

- [ ] _Measures.Teilnahmequote: nur freiwillige Kurse; Nenner = Headcount
- [ ] _Measures.Ø Stunden je MA: Nenner Headcount, nicht Teilnehmende
- [ ] _Measures.Pflichtquote: alle drei Pflichtkurse abgeschlossen
- [ ] _Measures.Kosten: offen: Reisekosten gehören (noch) nicht dazu
- [ ] _Measures.Ø Zufriedenheit: freiwillige Angabe, ca. 70 % Rücklauf

## Nächste Schritte

- [ ] Kennzahlen-Definitionen bestätigen (Steckbrief), fehlende Kennzahlen im Semantikmodell anlegen
- [ ] Seiten mit dem Skill `mockup-to-powerbi` ins PBIP übertragen
- [ ] Review der gebauten Seiten mit den Teilnehmenden, Status auf „abgenommen" setzen
