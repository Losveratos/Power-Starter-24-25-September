# PBIP-Werkzeuge

| Datei | Zweck |
|---|---|
| `build_weiterbildung_pbip.py` | erzeugt `pbip/Weiterbildungs-Monitoring/` (Modell + Bericht) |
| `TmdlCheck/` | .NET-8-Programm mit Microsoft TOM: liest TMDL ein, prüft Grundregeln, schreibt kanonisch, exportiert eine Feldliste |
| `validate_pbir.py` | prüft einen PBIR-Bericht gegen die Microsoft-Schemas und alle Feldbezüge gegen die Feldliste |
| `resources/CY24SU10.json` | Power-BI-Basisdesign, das Desktop in jedes PBIP legt |

```bash
# einmalig: .NET 8 SDK (z. B. apt install dotnet-sdk-8.0) und pip install jsonschema
python3 tools/pbip/build_weiterbildung_pbip.py /tmp/wb_raw
python3 tools/pbip/validate_pbir.py pbip/Weiterbildungs-Monitoring/Weiterbildungs-Monitoring.Report /tmp/wb_felder.json
```

Mit den offiziellen CLIs (Windows): `pbip/Weiterbildungs-Monitoring/pruefen.ps1`.
