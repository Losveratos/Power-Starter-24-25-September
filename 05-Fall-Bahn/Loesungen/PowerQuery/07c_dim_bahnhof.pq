// Extra · Abfrage 3 von 3: Dimension – eine Zeile je Bahnhof mit allen beschreibenden Spalten
// Neue leere Abfrage, Name: dim_bahnhof
// Klickweg: roh_bahnhoefe → Rechtsklick → Verweis → Spalten Bahnhof, Stadt, Bundesland, Größenklasse markieren →
//           Rechtsklick → Andere Spalten entfernen → Start → Zeilen entfernen → Duplikate entfernen
// ✅ 96 Zeilen · 77 Städte · 16 Bundesländer · Größenklasse A 12 · B 27 · C 57
// Danach in der Modellansicht: fakt_reisende[Bahnhof] → dim_bahnhof[Bahnhof] (n:1)
let
    Quelle = roh_bahnhoefe,
    Spalten = Table.SelectColumns(Quelle, {"Bahnhof", "Stadt", "Bundesland", "Größenklasse"}),
    Eindeutig = Table.Distinct(Spalten, {"Bahnhof"})
in
    Eindeutig
