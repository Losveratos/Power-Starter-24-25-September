// Teil A · Schritt 5 – Zielwerte (fiktiv) von der Kreuztabelle in eine lange Tabelle
// Abfrage umbenennen in: ziele
// ✅ vorher 31 Zeilen × 6 Spalten, nachher 155 Zeilen × 3 Spalten (Land, Jahr, Ziel)
let
    Quelle = Csv.Document(
        Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/05-Fall-Bahn/Daten/3-Ziele/ziele_fahrten_pro_kopf_fiktiv.csv"),
        [Delimiter = ";", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Kopfzeile = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true]),
    // Klickweg: Spalte „Land" markieren → Rechtsklick → Andere Spalten entpivotieren
    Entpivotiert = Table.UnpivotOtherColumns(Kopfzeile, {"Land"}, "Jahr", "Ziel"),
    Typen = Table.TransformColumnTypes(Entpivotiert,
        {{"Land", type text}, {"Jahr", Int64.Type}, {"Ziel", type number}}, "de-DE")
in
    Typen
