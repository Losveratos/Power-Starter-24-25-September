// Teil B – SBB: Ein- und Aussteigende an Bahnhöfen, live vom SBB-Datenportal (Lizenz: offen, Quelle nennen)
// Abfrage umbenennen in: sbb_bahnhoefe
// Datensatz: https://data.sbb.ch/explore/dataset/passagierfrequenz/
// Anmeldung beim ersten Laden: Anonym.
//
// DTV = durchschnittlicher täglicher Verkehr (alle Tage), DWV = durchschnittlicher Werktagsverkehr (Mo–Fr).
// Umsteigende zählen doppelt (einmal aus-, einmal einsteigen).
//
// Die Spaltennamen im Export können sich leicht ändern (z. B. „dtv_tjm_tgm"). Deshalb sucht das Skript
// die Spalten über ihren Anfang und benennt sie einheitlich um. Fehlt eine Spalte, wird sie einfach weggelassen.
let
    Quelle = Csv.Document(
        Web.Contents("https://data.sbb.ch/api/explore/v2.1/catalog/datasets/passagierfrequenz/exports/csv",
            [Query = [delimiter = ";"]]),
        [Delimiter = ";", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Kopfzeile = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true]),
    Finde = (anfang as text) as nullable text =>
        List.First(List.Select(Table.ColumnNames(Kopfzeile), each Text.StartsWith(Text.Lower(_), anfang))),
    Wunsch = {{"bahnhof", "Bahnhof"}, {"kt", "Kanton"}, {"jahr", "Jahr"}, {"dtv", "DTV"}, {"dwv", "DWV"}, {"geopos", "Geopos"}},
    Paare = List.Select(List.Transform(Wunsch, each {Finde(_{0}), _{1}}), each _{0} <> null),
    Auswahl = Table.SelectColumns(Kopfzeile, List.Transform(Paare, each _{0})),
    Umbenannt = Table.RenameColumns(Auswahl, Paare),
    // Jahr kann als 2024 oder 2024-01-01 kommen → die ersten vier Zeichen nehmen
    Jahr = Table.TransformColumns(Umbenannt, {{"Jahr", each Int64.From(Text.Start(Text.From(_), 4)), Int64.Type}}),
    // Zahlen kommen mit Punkt als Dezimalzeichen → Gebietsschema Englisch (USA)
    Zahlen = Table.TransformColumnTypes(Jahr, {{"DTV", type number}, {"DWV", type number}}, "en-US"),
    // Koordinaten „47.378, 8.540" in Breite und Länge zerlegen (für die Kartenvisualisierung)
    MitKoordinaten =
        if List.Contains(Table.ColumnNames(Zahlen), "Geopos") then
            Table.TransformColumns(
                Table.SplitColumn(Zahlen, "Geopos", Splitter.SplitTextByDelimiter(",", QuoteStyle.None), {"Breitengrad", "Längengrad"}),
                {{"Breitengrad", each Number.From(Text.Trim(_), "en-US"), type nullable number},
                 {"Längengrad", each Number.From(Text.Trim(_), "en-US"), type nullable number}})
        else Zahlen,
    OhneLeer = Table.SelectRows(MitKoordinaten, each [DTV] <> null)
in
    OhneLeer
