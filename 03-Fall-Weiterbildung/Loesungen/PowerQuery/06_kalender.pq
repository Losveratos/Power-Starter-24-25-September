// Schritt 5 · Kalendertabelle 2025 → Abfrage "Kalender"
// Danach: als Datumstabelle markieren (Spalte Datum), Monat nach MonatNr sortieren.
// Beziehung: fakt_buchungen[Kursbeginn] → Kalender[Datum]
let
    Start = #date(2025, 1, 1),
    Ende = #date(2025, 12, 31),
    Liste = List.Dates(Start, Duration.Days(Ende - Start) + 1, #duration(1, 0, 0, 0)),
    Tabelle = Table.FromList(Liste, Splitter.SplitByNothing(), {"Datum"}),
    Datum = Table.TransformColumnTypes(Tabelle, {{"Datum", type date}}),
    Jahr = Table.AddColumn(Datum, "Jahr", each Date.Year([Datum]), Int64.Type),
    Quartal = Table.AddColumn(Jahr, "Quartal", each "Q" & Text.From(Date.QuarterOfYear([Datum])), type text),
    MonatNr = Table.AddColumn(Quartal, "MonatNr", each Date.Month([Datum]), Int64.Type),
    Monat = Table.AddColumn(MonatNr, "Monat", each Date.ToText([Datum], [Format = "MMM", Culture = "de-DE"]), type text),
    Monatsanfang = Table.AddColumn(Monat, "Monatsanfang", each Date.StartOfMonth([Datum]), type date)
in
    Monatsanfang
