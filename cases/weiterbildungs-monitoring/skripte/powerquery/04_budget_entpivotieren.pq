// Schritt 4a · Budget-Kreuztabelle (Bereiche × Quartale) → lange Tabelle "Budget"
// Kontrollzahl: 28 Zeilen (7 Bereiche × 4 Quartale), Summe Budget 274.500 €.
// Beziehungen: Budget[Bereich] → dim_bereich[Bereich] · Budget[Quartalsanfang] → Kalender[Datum]
let
    Quelle = Excel.Workbook(Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/cases/weiterbildungs-monitoring/daten/ziele/ziele_2025.xlsx"), null, true),
    Blatt = Quelle{[Item = "Budget 2025", Kind = "Sheet"]}[Data],
    // Titel + Leerzeile weg, dann Überschriften
    OhneTitel = Table.Skip(Blatt, 2),
    Ueberschriften = Table.PromoteHeaders(OhneTitel, [PromoteAllScalars = true]),
    // Summenzeile und Summenspalte weg – Summen rechnet Power BI selbst
    OhneGesamtzeile = Table.SelectRows(Ueberschriften, each [Bereich] <> "Gesamt"),
    OhneSummenspalte = Table.RemoveColumns(OhneGesamtzeile, {"Summe"}),
    // der Kern: Quartalsspalten werden zu Zeilen
    Entpivotiert = Table.UnpivotOtherColumns(OhneSummenspalte, {"Bereich"}, "Quartal", "Budget"),
    // "Q2" → 01.04.2025, damit das Budget an den Kalender passt
    Quartalsanfang = Table.AddColumn(
        Entpivotiert, "Quartalsanfang",
        each #date(2025, (Number.From(Text.End([Quartal], 1)) - 1) * 3 + 1, 1), type date
    ),
    Typen = Table.TransformColumnTypes(Quartalsanfang, {{"Bereich", type text}, {"Quartal", type text}, {"Budget", Currency.Type}})
in
    Typen
