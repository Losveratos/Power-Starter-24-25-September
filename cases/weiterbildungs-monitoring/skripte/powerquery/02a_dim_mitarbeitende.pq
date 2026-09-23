// Schritt 3 · Anreicherung: HR-Stamm → Abfrage "dim_mitarbeitende"
// Kontrollzahl: 420 Zeilen. Beziehung: fakt_buchungen[Personalnr] → dim_mitarbeitende[Personalnr]
let
    Quelle = Csv.Document(
        Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/cases/weiterbildungs-monitoring/daten/anreicherung/dim_mitarbeitende.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Ueberschriften = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true]),
    Typen = Table.TransformColumnTypes(
        Ueberschriften,
        {
            {"Personalnr", type text},          // Text! Sonst gehen die führenden Nullen verloren
            {"BereichID", type text},
            {"Standort", type text},
            {"Rolle", type text},
            {"Beschaeftigung", type text},
            {"FTE", type number},
            {"Altersgruppe", type text},
            {"Eintritt", type date}
        },
        "en-US"                                 // diese Datei nutzt den Punkt als Dezimalzeichen
    )
in
    Typen
