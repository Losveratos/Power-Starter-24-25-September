// Schritt 4b · Zielwerte-Kreuztabelle (Bereiche × Kennzahlen) → lange Tabelle "Zielwerte"
// Kontrollzahl: 28 Zeilen (7 Bereiche × 4 Kennzahlen).
// Beziehung: Zielwerte[Bereich] → dim_bereich[Bereich]
let
    Quelle = Excel.Workbook(Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/03-Fall-Weiterbildung/Daten/3-Ziele/ziele_2025.xlsx"), null, true),
    Blatt = Quelle{[Item = "Zielwerte 2025", Kind = "Sheet"]}[Data],
    OhneTitel = Table.Skip(Blatt, 2),
    Ueberschriften = Table.PromoteHeaders(OhneTitel, [PromoteAllScalars = true]),
    Entpivotiert = Table.UnpivotOtherColumns(Ueberschriften, {"Bereich"}, "Kennzahl", "Zielwert"),
    // Prozentwerte stehen in Excel als 0,75 – die Formatierung "75 %" war nur Anzeige
    Typen = Table.TransformColumnTypes(Entpivotiert, {{"Bereich", type text}, {"Kennzahl", type text}, {"Zielwert", type number}})
in
    Typen
