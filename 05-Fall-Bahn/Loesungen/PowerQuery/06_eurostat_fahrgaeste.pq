// Teil C – Fahrgäste je Land und Jahr (Eurostat rail_pa_total), mit der Funktion fxEurostat
// Abfrage umbenennen in: fakt_fahrgaeste
// Datensatz: https://ec.europa.eu/eurostat/databrowser/view/rail_pa_total/default/table?lang=en
let
    Quelle = fxEurostat("rail_pa_total"),
    // Zwei Einheiten stecken in der Tabelle: THS_PAS = Tausend Fahrgäste, MIO_PKM = Mio. Personenkilometer
    Fahrgaeste = Table.SelectRows(Quelle, each [unit] = "THS_PAS"),
    // Summen wie EU27_2020 raus – nur echte Länder (Code mit zwei Buchstaben), sonst zählst du doppelt
    NurLaender = Table.SelectRows(Fahrgaeste, each Text.Length([geo]) = 2),
    InMio = Table.AddColumn(NurLaender, "Fahrgäste Mio", each [Wert] / 1000, type number),
    Fertig = Table.SelectColumns(InMio, {"geo", "Jahr", "Fahrgäste Mio", "Kennzeichen"})
in
    Fertig
