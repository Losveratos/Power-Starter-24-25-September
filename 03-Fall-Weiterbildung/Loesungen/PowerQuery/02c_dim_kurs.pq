// Schritt 3 · Anreicherung: Kurskatalog → Abfrage "dim_kurs"
// Kontrollzahl: 23 Zeilen, davon 3 Pflichtkurse. Beziehung: fakt_buchungen[Kursnr] → dim_kurs[Kursnr]
let
    Quelle = Csv.Document(
        Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/03-Fall-Weiterbildung/Daten/2-Anreicherung/dim_kurs.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Ueberschriften = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true]),
    Typen = Table.TransformColumnTypes(
        Ueberschriften,
        {
            {"Kursnr", type text}, {"Kurstitel", type text}, {"Kategorie", type text}, {"Format", type text},
            {"Anbieter", type text}, {"Pflicht", type text}, {"Dauer_h", type number}, {"Listenpreis", Currency.Type}
        },
        "en-US"
    )
in
    Typen
