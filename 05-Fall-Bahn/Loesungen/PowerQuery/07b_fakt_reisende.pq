// Extra · Abfrage 2 von 3: Faktentabelle – nur Schlüssel + Zahl, eine Zeile je Bahnhof und Monat
// Neue leere Abfrage, Name: fakt_reisende
// Klickweg: roh_bahnhoefe → Rechtsklick → Verweis → Spalte „Bahnhof" markieren →
//           Rechtsklick → Andere Spalten entpivotieren … (Stadt, Bundesland, Größenklasse vorher entfernen)
// ✅ 1.152 Zeilen (96 × 12) · Summe Reisende 2.906.495.000 · Januar 226.644.366
let
    Quelle = roh_bahnhoefe,
    // Beschreibende Spalten gehören in die Dimension, nicht in die Fakten
    NurSchluesselUndMonate = Table.RemoveColumns(Quelle, {"Stadt", "Bundesland", "Größenklasse"}),
    Entpivotiert = Table.UnpivotOtherColumns(NurSchluesselUndMonate, {"Bahnhof"}, "Monat", "Reisende"),
    // „2025-01" → 01.01.2025 (Datum, damit eine Kalendertabelle andocken kann)
    Datum = Table.TransformColumns(Entpivotiert,
        {{"Monat", each #date(Number.From(Text.Start(_, 4)), Number.From(Text.End(_, 2)), 1), type date}}),
    Typen = Table.TransformColumnTypes(Datum, {{"Bahnhof", type text}, {"Reisende", Int64.Type}})
in
    Typen
