// Extra · Kreuztabelle → Sternschema, Abfrage 1 von 3: die Rohdatei laden (Staging, nicht laden)
// Abfrage umbenennen in: roh_bahnhoefe · Rechtsklick → „Laden aktivieren" ausschalten
// ✅ 96 Zeilen × 16 Spalten (Bahnhof, Stadt, Bundesland, Größenklasse, 2025-01 … 2025-12)
// Hinweis: Die Monatswerte sind simuliert (Demo), die Tageswerte je Bahnhof gerundete Größenordnungen.
let
    Quelle = Csv.Document(
        Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/05-Fall-Bahn/Daten/1-Rohdaten/bahnhoefe_reisende_2025_kreuztabelle.csv"),
        [Delimiter = ";", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Kopfzeile = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true])
in
    Kopfzeile
