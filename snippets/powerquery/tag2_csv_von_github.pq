// Tag 2 · Vorlage: eine saubere CSV aus diesem Repo laden
// Für jede Datei eine Leere Abfrage anlegen, Dateinamen + Typen anpassen, Abfrage wie die Datei nennen.
// Beispiel hier: fakt_verkaeufe
let
    Quelle = Csv.Document(
        Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/daten/tag2/fakt_verkaeufe.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Ueberschriften = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true]),
    Typen = Table.TransformColumnTypes(
        Ueberschriften,
        {
            {"Belegnummer", type text},
            {"Belegdatum", type date},
            {"FilialeID", type text},
            {"ProduktID", type text},
            {"KundeID", type text},
            {"Menge", Int64.Type},
            {"Rabatt", type number}
        },
        "en-US"
    )
in
    Typen

// Typen für die anderen Dateien (immer mit "en-US" als letztem Argument):
//   dim_produkt:  ProduktID text · Produkt text · Kategorie text · Listenpreis Currency.Type · Einstandspreis Currency.Type
//   dim_kunde:    KundeID text · Kunde text · Segment text · PLZ text (!) · Ort text · StammFilialeID text
//   dim_filiale:  FilialeID text · Filiale text · Bundesland text · Eroeffnet date · Verkaufsflaeche_m2 Int64.Type
// PLZ unbedingt als Text: sonst wird aus 04109 (Leipzig) die Zahl 4109.
