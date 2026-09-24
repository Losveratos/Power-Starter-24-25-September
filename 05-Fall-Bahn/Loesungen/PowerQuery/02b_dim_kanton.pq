// Teil B – Kantone der Schweiz (für die SBB-Daten). Abfrage umbenennen in: dim_kanton   ✅ 26 Zeilen
let
    Quelle = Csv.Document(
        Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/05-Fall-Bahn/Daten/2-Anreicherung/dim_kanton.csv"),
        [Delimiter = ";", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Kopfzeile = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true]),
    Typen = Table.TransformColumnTypes(Kopfzeile,
        {{"Kanton", type text}, {"Kantonsname", type text}, {"Hauptsprache", type text}, {"Amtssprachen", type text}})
in
    Typen
