// Schritt 3 · Anreicherung: Bereiche → Abfrage "dim_bereich"
// Kontrollzahl: 7 Zeilen. Beziehung: dim_mitarbeitende[BereichID] → dim_bereich[BereichID]
let
    Quelle = Csv.Document(
        Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/cases/weiterbildungs-monitoring/daten/anreicherung/dim_bereich.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Ueberschriften = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true]),
    Typen = Table.TransformColumnTypes(
        Ueberschriften,
        {{"BereichID", type text}, {"Bereich", type text}, {"Ressort", type text}, {"Kostenstelle", type text}}
    )
in
    Typen
