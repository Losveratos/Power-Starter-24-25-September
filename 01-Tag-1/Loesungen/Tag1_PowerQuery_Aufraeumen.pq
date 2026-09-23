// Tag 1 · Lösung zu Übung 2: der komplette Aufräum-Weg als M-Code
// Einfügen: Power Query → Neue Quelle → Leere Abfrage → Erweiterter Editor → alles ersetzen.
// Abfrage danach "verkaeufe_2025" nennen.
let
    Quelle = Csv.Document(
        Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/01-Tag-1/Daten/verkaeufe_2025_roh.csv"),
        [Delimiter = ",", Columns = 8, Encoding = 65001, QuoteStyle = QuoteStyle.None]
    ),
    // 1 · Müllzeile (Export-Kopf) weg
    OhneMuellzeile = Table.Skip(Quelle, 1),
    // 2 · erste Zeile als Überschrift
    Ueberschriften = Table.PromoteHeaders(OhneMuellzeile, [PromoteAllScalars = true]),
    // 3 · komplett leere Zeilen weg
    OhneLeereZeilen = Table.SelectRows(
        Ueberschriften,
        each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))
    ),
    // 4 · Leerzeichen am Ende ("Köln " → "Köln")
    Gekuerzt = Table.TransformColumns(OhneLeereZeilen, {{"Filiale", Text.Trim, type text}}),
    // 5 · Schreibweise vereinheitlichen ("zubehör" → "Zubehör")
    Grossschreibung = Table.TransformColumns(Gekuerzt, {{"Kategorie", Text.Proper, type text}}),
    // 6–8 · Datentypen – mit Gebietsschema en-US, weil die Datei den Punkt als Dezimalzeichen nutzt
    Typen = Table.TransformColumnTypes(
        Grossschreibung,
        {
            {"Belegnummer", type text},
            {"Belegdatum", type date},
            {"Produkt", type text},
            {"Menge", Int64.Type},
            {"Umsatz", Currency.Type},
            {"Kosten", Currency.Type}
        },
        "en-US"
    )
in
    Typen
