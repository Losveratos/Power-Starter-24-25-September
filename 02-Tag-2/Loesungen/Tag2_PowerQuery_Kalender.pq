// Kalendertabelle in M (Power Query) – Abfrage "Kalender" nennen
// Danach im Modell: Tabellentools → Als Datumstabelle markieren → Spalte "Datum".
// Und: Datei → Optionen → Aktuelle Datei → Datenladevorgang → "Automatisches Datum/Uhrzeit" aus.
let
    Start = #date(2025, 1, 1),
    Ende = #date(2025, 12, 31),
    Liste = List.Dates(Start, Duration.Days(Ende - Start) + 1, #duration(1, 0, 0, 0)),
    Tabelle = Table.FromList(Liste, Splitter.SplitByNothing(), {"Datum"}),
    Datum = Table.TransformColumnTypes(Tabelle, {{"Datum", type date}}),
    Jahr = Table.AddColumn(Datum, "Jahr", each Date.Year([Datum]), Int64.Type),
    Quartal = Table.AddColumn(Jahr, "Quartal", each "Q" & Text.From(Date.QuarterOfYear([Datum])), type text),
    MonatNr = Table.AddColumn(Quartal, "MonatNr", each Date.Month([Datum]), Int64.Type),
    // "Monat" im Modell nach "MonatNr" sortieren (Spaltentools → Nach Spalte sortieren), sonst steht Apr vor Jan
    Monat = Table.AddColumn(MonatNr, "Monat", each Date.ToText([Datum], [Format = "MMM", Culture = "de-DE"]), type text),
    Monatsanfang = Table.AddColumn(Monat, "Monatsanfang", each Date.StartOfMonth([Datum]), type date),
    WochentagNr = Table.AddColumn(Monatsanfang, "WochentagNr", each Date.DayOfWeek([Datum], Day.Monday) + 1, Int64.Type),
    // "Wochentag" nach "WochentagNr" sortieren
    Wochentag = Table.AddColumn(WochentagNr, "Wochentag", each Date.ToText([Datum], [Format = "ddd", Culture = "de-DE"]), type text),
    IstWochenende = Table.AddColumn(Wochentag, "IstWochenende", each [WochentagNr] >= 6, type logical)
in
    IstWochenende
