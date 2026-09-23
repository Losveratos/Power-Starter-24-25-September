# Prüft das Projekt mit den offiziellen CLIs – unter Windows (oder macOS mit pwsh).
# Voraussetzungen:
#   pbir-cli:            uv tool install pbir-cli     (oder: pip install pbir-cli)
#   Tabular Editor CLI:  te.exe von tabulareditor.com (Konto nötig), Ordner in PATH
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$Modell  = "Weiterbildungs-Monitoring.SemanticModel"
$Bericht = "Weiterbildungs-Monitoring.Report"

Write-Host "== Modell (te)" -ForegroundColor Cyan
te validate -m $Modell --errors-only
te list -m $Modell --paths-only
te list -m $Modell _Measures --paths-only

Write-Host "== Bericht (pbir)" -ForegroundColor Cyan
pbir validate $Bericht --fields
pbir ls $Bericht
