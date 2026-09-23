// Schritt 2 · Rohdaten aus dem LMS aufräumen → Abfrage "fakt_buchungen"
// Einfügen: Start → Neue Quelle → Leere Abfrage → Erweiterter Editor → alles ersetzen.
// Kontrollzahl danach: 1.712 Zeilen, 10 Spalten.
let
    // Windows-1252 (ANSI), Semikolon, deutsche Zahlen – typisch für Exporte aus deutschen Systemen
    Quelle = Csv.Document(
        Web.Contents("https://raw.githubusercontent.com/Losveratos/Power-Starter-24-25-September/main/cases/weiterbildungs-monitoring/daten/roh/weiterbildung_buchungen_2025.csv"),
        [Delimiter = ";", Columns = 11, Encoding = 1252, QuoteStyle = QuoteStyle.None]
    ),
    Ueberschriften = Table.PromoteHeaders(Quelle, [PromoteAllScalars = true]),
    // Summenzeile "Summe;1736 Datensätze" am Ende weg
    OhneSummenzeile = Table.RemoveLastN(Ueberschriften, 1),
    // 24 Buchungen stehen doppelt im Export
    OhneDuplikate = Table.Distinct(OhneSummenzeile),
    // Kurstitel steht schon in dim_kurs – im Fakt nur der Schlüssel
    OhneKurstitel = Table.RemoveColumns(OhneDuplikate, {"Kurstitel"}),
    // Personalnr: im LMS ohne führende Nullen ("238"), im HR-System fünfstellig ("00238")
    Personalnr = Table.TransformColumns(OhneKurstitel, {{"Personalnr", each Text.PadStart(Text.Trim(_), 5, "0"), type text}}),
    // Status: Leerzeichen, Groß-/Kleinschreibung und Synonyme vereinheitlichen
    StatusBereinigt = Table.TransformColumns(Personalnr, {{"Status", each Text.Lower(Text.Trim(_)), type text}}),
    StatusSynonyme = Table.TransformColumns(StatusBereinigt, {{"Status", each
        if _ = "teilgenommen" then "abgeschlossen"
        else if List.Contains({"no-show", "no show", "nicht erschienen"}, _) then "No-Show"
        else _, type text}}),
    // "1.234,50 €" → "1.234,50"
    OhneEuro = Table.ReplaceValue(StatusSynonyme, " €", "", Replacer.ReplaceText, {"Kosten"}),
    // leeres Feedback (nicht bewertet) ist null, nicht 0
    FeedbackLeer = Table.ReplaceValue(OhneEuro, "", null, Replacer.ReplaceValue, {"Feedback"}),
    // Typen mit Gebietsschema de-DE: Komma als Dezimalzeichen, Datum TT.MM.JJJJ
    Typen = Table.TransformColumnTypes(
        FeedbackLeer,
        {
            {"BuchungsID", Int64.Type},
            {"Kursnr", type text},
            {"Buchungsdatum", type date},
            {"Kursbeginn", type date},
            {"Kursende", type date},
            {"Stunden", type number},
            {"Kosten", Currency.Type},
            {"Feedback", Int64.Type}
        },
        "de-DE"
    )
in
    Typen
