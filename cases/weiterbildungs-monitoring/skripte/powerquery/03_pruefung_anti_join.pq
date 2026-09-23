// Schritt 3b · Prüfabfrage: Buchungen ohne passende Person im HR-Stamm
// Nach Schritt 2 und 3 anlegen. Ergebnis sollte 0 Zeilen haben.
// Nimmst du den Schritt "Personalnr" aus fakt_buchungen heraus, sind es plötzlich alle 1.712 Zeilen –
// genau so findet man kaputte Schlüssel. Abfrage danach mit Rechtsklick → "Laden aktivieren" abschalten.
let
    Ohne_Treffer = Table.NestedJoin(
        fakt_buchungen, {"Personalnr"},
        dim_mitarbeitende, {"Personalnr"},
        "HR", JoinKind.LeftAnti
    ),
    Ergebnis = Table.RemoveColumns(Ohne_Treffer, {"HR"})
in
    Ergebnis
