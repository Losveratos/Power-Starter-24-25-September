// Teil A · Schritt 2 – Länder-Stammdaten (Name, Region, EU ja/nein)
// Abfrage umbenennen in: dim_land   ✅ 31 Zeilen
// Achtung: Eurostat schreibt Griechenland als EL (nicht GR) – die Codes hier passen dazu.
let
    Quelle = Csv.Document(
        Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/05-Fall-Bahn/Daten/2-Anreicherung/dim_land.csv"),
        [Delimiter = ";", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Kopfzeile = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true]),
    Typen = Table.TransformColumnTypes(Kopfzeile,
        {{"Code", type text}, {"Land", type text}, {"Land_EN", type text}, {"Region", type text}, {"EU", type text}})
in
    Typen
