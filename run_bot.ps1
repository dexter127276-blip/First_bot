$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$mainScript = Join-Path $projectRoot "main.py"
$envFile = Join-Path $projectRoot ".env"

if (-not (Test-Path -LiteralPath $venvPython)) {
    throw "Virtual environment not found. Create it with: python -m venv .venv"
}

if (-not (Test-Path -LiteralPath $envFile)) {
    throw ".env file not found. Copy .env.example to .env and fill in the credentials."
}

& $venvPython $mainScript
exit $LASTEXITCODE
