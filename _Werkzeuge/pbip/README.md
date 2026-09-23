# PBIP-Werkzeuge

| Datei | Zweck |
|---|---|
| `build_weiterbildung_pbip.py` | erzeugt `03-Fall-Weiterbildung/PowerBI-Loesung/` (Modell + Bericht) |
| `TmdlCheck/` | .NET-8-Programm mit Microsoft TOM: liest TMDL ein, prüft Grundregeln, schreibt kanonisch, exportiert eine Feldliste |
| `validate_pbir.py` | prüft einen PBIR-Bericht gegen die Microsoft-Schemas und alle Feldbezüge gegen die Feldliste |
| `resources/CY24SU10.json` | Power-BI-Basisdesign, das Desktop in jedes PBIP legt |

```bash
# einmalig: .NET 8 SDK (z. B. apt install dotnet-sdk-8.0) und pip install jsonschema
python3 _Werkzeuge/pbip/build_weiterbildung_pbip.py /tmp/wb_raw
python3 _Werkzeuge/pbip/validate_pbir.py 03-Fall-Weiterbildung/PowerBI-Loesung/Weiterbildungs-Monitoring.Report /tmp/wb_felder.json
```

Mit den offiziellen CLIs (Windows): `03-Fall-Weiterbildung/PowerBI-Loesung/pruefen.ps1`.
