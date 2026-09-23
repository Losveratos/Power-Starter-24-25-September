// Tag 2 · Lösung zu Übung 8: Excel-Kreuztabelle (Monate als Spalten) → lange Tabelle
// Abfrage "Plan" nennen. Beziehungen danach:
//   Plan[Filiale]      → dim_filiale[Filiale]  (n:1)
//   Plan[Monatsanfang] → Kalender[Datum]       (n:1)
let
    Quelle = Excel.Workbook(Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/daten/tag2/plan_2025.xlsx"), null, true),
    Blatt = Quelle{[Item = "Plan 2025", Kind = "Sheet"]}[Data],
    // Titelzeile + Leerzeile weg, dann Überschriften
    OhneTitel = Table.Skip(Blatt, 2),
    Ueberschriften = Table.PromoteHeaders(OhneTitel, [PromoteAllScalars = true]),
    // Summenspalte gehört nicht in eine lange Tabelle – die rechnet Power BI selbst
    OhneGesamt = Table.RemoveColumns(Ueberschriften, {"Gesamt"}),
    // der Kern: alles außer "Filiale" wird zu Zeilen
    Entpivotiert = Table.UnpivotOtherColumns(OhneGesamt, {"Filiale"}, "Monat", "Plan"),
    Monate = {"Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"},
    MitDatum = Table.AddColumn(
        Entpivotiert, "Monatsanfang",
        each #date(2025, List.PositionOf(Monate, [Monat]) + 1, 1), type date
    ),
    Typen = Table.TransformColumnTypes(MitDatum, {{"Filiale", type text}, {"Plan", Currency.Type}}),
    Ergebnis = Table.RemoveColumns(Typen, {"Monat"})
in
    Ergebnis
