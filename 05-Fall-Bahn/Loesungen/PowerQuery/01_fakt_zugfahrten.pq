// Teil A · Schritt 1 – Zugfahrten pro Kopf 2024 laden (Eurostat, 31 Länder)
// Einfügen: Start → Daten transformieren → Neue Quelle → Leere Abfrage → Erweiterter Editor → alles ersetzen.
// Abfrage umbenennen in: fakt_zugfahrten
// ✅ 31 Zeilen, Schweiz 57,9 · Kategorie: hoch 9 · mittel 7 · niedrig 15
let
    Quelle = Csv.Document(
        Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/05-Fall-Bahn/Daten/1-Rohdaten/zugfahrten_pro_kopf_2024.csv"),
        [Delimiter = ";", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Kopfzeile = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true]),
    // Der Ländername in GROSSBUCHSTABEN wird nicht gebraucht – den schönen Namen liefert dim_land
    OhneLand = Table.RemoveColumns(Kopfzeile, {"Land"}),
    // Komma als Dezimalzeichen → Gebietsschema Deutsch (sonst wird aus 57,9 die Zahl 579)
    Typen = Table.TransformColumnTypes(OhneLand,
        {{"geo", type text}, {"Jahr", Int64.Type}, {"Fahrten pro Kopf", type number}}, "de-DE"),
    // Spalte hinzufügen → Bedingte Spalte: ≥ 20 hoch · ≥ 12 mittel · sonst niedrig
    Kategorie = Table.AddColumn(Typen, "Kategorie",
        each if [Fahrten pro Kopf] >= 20 then "hoch" else if [Fahrten pro Kopf] >= 12 then "mittel" else "niedrig",
        type text)
in
    Kategorie
