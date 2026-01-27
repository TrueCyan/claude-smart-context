# Smart Context Plugin Initialization (Windows)
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PluginRoot = Split-Path -Parent $ScriptDir
$InitFlag = Join-Path $PluginRoot ".initialized"
$VenvPath = Join-Path $PluginRoot ".venv"
$ContextDir = Join-Path $env:USERPROFILE ".claude\context_history"

# Already initialized → exit immediately
if (Test-Path $InitFlag) {
    exit 0
}

Write-Host "[smart-context] Initializing plugin..."

# Check Python availability
$PythonCmd = $null
if (Get-Command python3 -ErrorAction SilentlyContinue) {
    $PythonCmd = "python3"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonCmd = "python"
} else {
    Write-Host "[smart-context] ERROR: Python not found. Please install Python 3.8+"
    exit 1
}

# Create virtual environment
if (-not (Test-Path $VenvPath)) {
    Write-Host "[smart-context] Creating Python virtual environment..."
    & $PythonCmd -m venv $VenvPath
}

# Create context directories
New-Item -ItemType Directory -Force -Path (Join-Path $ContextDir "archives") | Out-Null

# Mark as initialized
New-Item -ItemType File -Force -Path $InitFlag | Out-Null
Write-Host "[smart-context] Plugin initialized successfully"
