using System;
using System.Linq;
using Microsoft.AnalysisServices.Tabular;

// TmdlCheck <tmdl-ordner> [ausgabe-ordner]
// Liest ein TMDL-Modell mit TOM ein (Syntax + Objektbezüge), prüft Grundregeln und schreibt es
// optional kanonisch neu (so, wie Power BI Desktop / Tabular Editor TMDL serialisieren).
class Program
{
    static int Main(string[] args)
    {
        var db = TmdlSerializer.DeserializeDatabaseFromFolder(args[0]);
        var m = db.Model;
        int errors = 0;
        void Err(string s) { Console.WriteLine("FEHLER  " + s); errors++; }

        Console.WriteLine($"Modell: {m.Tables.Count} Tabellen · {m.Tables.Sum(t => t.Columns.Count(c => c.Type != ColumnType.RowNumber))} Spalten · " +
                          $"{m.Tables.Sum(t => t.Measures.Count)} Measures · {m.Relationships.Count} Beziehungen · {m.Expressions.Count} Ausdrücke");
        foreach (var t in m.Tables)
        {
            if (t.Partitions.Count == 0 && t.CalculationGroup == null) Err($"Tabelle {t.Name} hat keine Partition");
            foreach (var p in t.Partitions)
                if (p.Source is MPartitionSource ms && string.IsNullOrWhiteSpace(ms.Expression)) Err($"{t.Name}: leere M-Abfrage");
            foreach (var c in t.Columns.OfType<DataColumn>())
                if (string.IsNullOrEmpty(c.SourceColumn)) Err($"{t.Name}[{c.Name}] ohne sourceColumn");
            foreach (var c in t.Columns.Where(c => c.SortByColumn != null))
                Console.WriteLine($"  sortiert: {t.Name}[{c.Name}] nach [{c.SortByColumn.Name}]");
            foreach (var ms in t.Measures)
                if (string.IsNullOrWhiteSpace(ms.Expression)) Err($"Measure {ms.Name} leer");
            if (t.DataCategory == "Time")
            {
                var key = t.Columns.FirstOrDefault(c => c.IsKey);
                if (key == null || key.DataType != DataType.DateTime) Err($"Datumstabelle {t.Name} ohne Datums-Schlüsselspalte");
                else Console.WriteLine($"  Datumstabelle: {t.Name}[{key.Name}]");
            }
        }
        foreach (var r in m.Relationships.OfType<SingleColumnRelationship>())
        {
            Console.WriteLine($"  Beziehung: {r.FromTable.Name}[{r.FromColumn.Name}] ({r.FromCardinality}) → {r.ToTable.Name}[{r.ToColumn.Name}] ({r.ToCardinality}) · {r.CrossFilteringBehavior}{(r.IsActive ? "" : " · INAKTIV")}");
            if (r.FromColumn.DataType != r.ToColumn.DataType) Err($"Beziehung {r.FromTable.Name}[{r.FromColumn.Name}] ↔ {r.ToTable.Name}[{r.ToColumn.Name}]: Datentypen verschieden");
        }
        // Mehrdeutige Pfade grob prüfen: jede Tabelle höchstens eine aktive Beziehung je Zieltabelle
        foreach (var g in m.Relationships.Where(r => r.IsActive).GroupBy(r => (r.FromTable.Name, r.ToTable.Name)))
            if (g.Count() > 1) Err($"mehrere aktive Beziehungen {g.Key.Item1} → {g.Key.Item2}");

        var inv = args.SkipWhile(a => a != "--inventory").Skip(1).FirstOrDefault();
        if (inv != null)
        {
            var o = m.Tables.ToDictionary(t => t.Name, t => new {
                columns = t.Columns.Where(c => c.Type != ColumnType.RowNumber).Select(c => c.Name).ToArray(),
                measures = t.Measures.Select(x => x.Name).ToArray() });
            System.IO.File.WriteAllText(inv, System.Text.Json.JsonSerializer.Serialize(o, new System.Text.Json.JsonSerializerOptions { WriteIndented = true, Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping }));
            Console.WriteLine($"Feldliste geschrieben nach {inv}");
        }
        if (args.Length > 1 && !args[1].StartsWith("--"))
        {
            TmdlSerializer.SerializeDatabaseToFolder(db, args[1]);
            Console.WriteLine($"Kanonisch geschrieben nach {args[1]}");
        }
        Console.WriteLine(errors == 0 ? "OK – keine Fehler" : $"{errors} Fehler");
        return errors == 0 ? 0 : 1;
    }
}
