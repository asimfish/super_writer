param(
    [string]$OutputDir = "paper_rewriting_output",
    [switch]$InPlace
)

$ErrorActionPreference = "Stop"
$wizard = Join-Path $PSScriptRoot "intake_wizard.py"
if (-not (Test-Path -LiteralPath $wizard)) {
    throw "Super Writer intake wizard not found: $wizard"
}
if ([Console]::IsInputRedirected) {
    throw "Interactive stdin is required. Use intake_wizard.py --no-interactive with explicit options."
}
# InPlace remains accepted for callers of the legacy launcher.
& python $wizard --classic-input --output-dir $OutputDir
exit $LASTEXITCODE
