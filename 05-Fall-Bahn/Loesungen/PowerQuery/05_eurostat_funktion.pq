// Teil C – Funktion: lädt eine beliebige Eurostat-Tabelle im TSV-Format und entpivotiert sie
// Abfrage umbenennen in: fxEurostat   (danach mit 06_eurostat_fahrgaeste.pq aufrufen)
//
// Das TSV-Format ist eine echte Kreuztabelle: erste Spalte z. B. „freq,unit,geo\TIME_PERIOD",
// danach eine Spalte je Jahr. Werte wie „123456 p" (p = vorläufig) oder „:" (fehlt).
// Doku: https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-faq
(datensatz as text) as table =>
let
    Quelle = Csv.Document(
        Web.Contents("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/" & datensatz,
            [Query = [format = "TSV", compressed = "false"]]),
        [Delimiter = "#(tab)", Encoding = 65001, QuoteStyle = QuoteStyle.None]),
    Kopfzeile = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true]),
    ErsteSpalte = Table.ColumnNames(Kopfzeile){0},
    // „freq,unit,geo\TIME_PERIOD" → {"freq", "unit", "geo"}
    Dimensionen = Text.Split(Text.BeforeDelimiter(ErsteSpalte, "\"), ","),
    Aufgeteilt = Table.SplitColumn(Kopfzeile, ErsteSpalte, Splitter.SplitTextByDelimiter(",", QuoteStyle.None), Dimensionen),
    // Kernschritt: die Jahresspalten untereinander schreiben
    Entpivotiert = Table.UnpivotOtherColumns(Aufgeteilt, Dimensionen, "Jahr", "Wert_roh"),
    Jahr = Table.TransformColumns(Entpivotiert, {{"Jahr", each Int64.From(Text.Trim(_)), Int64.Type}}),
    Wert = Table.AddColumn(Jahr, "Wert",
        each try Number.From(Text.Trim(Text.Remove(_[Wert_roh], {"a".."z", ":"})), "en-US") otherwise null,
        type nullable number),
    Kennzeichen = Table.AddColumn(Wert, "Kennzeichen", each Text.Trim(Text.Select(_[Wert_roh], {"a".."z"})), type text),
    OhneLeer = Table.SelectRows(Kennzeichen, each [Wert] <> null),
    Fertig = Table.RemoveColumns(OhneLeer, {"Wert_roh"})
in
    Fertig
