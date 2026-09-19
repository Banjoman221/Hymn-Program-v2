$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvDir = Join-Path $RepoRoot ".venv-build"
$DistDir = Join-Path $RepoRoot "dist"

Set-Location $RepoRoot

function Get-Python {
    $py = $null
    $candidate = Get-Command "py" -ErrorAction SilentlyContinue
    if ($candidate) {
        $py = "py -3"
    } else {
        $candidate = Get-Command "python" -ErrorAction SilentlyContinue
        if ($candidate) {
            $py = "python"
        }
    }
    if (-not $py) {
        throw "Python was not found. Install Python 3.12+ from https://www.python.org/downloads/"
    }
    return $py
}

function Invoke-Venv {
    param([string]$Expr)
    if (-not (Test-Path (Join-Path $VenvDir "Scripts"))) {
        Invoke-Expression "$Py -m venv $VenvDir"
    }
    $Activate = Join-Path $VenvDir "Scripts\Activate.ps1"
    & $Activate
    Invoke-Expression $Expr
    if ($LASTEXITCODE -ne 0) { throw "Command failed: $Expr" }
}

$Py = Get-Python

Invoke-Venv "python -m pip install --upgrade pip"
Invoke-Venv "python -m pip install --upgrade cx_Freeze PyQt6 screeninfo"

Write-Host "Building executable with cx_Freeze..." -ForegroundColor Cyan
Invoke-Venv "python setup.py build"
if ($LASTEXITCODE -ne 0) { throw "cx_Freeze build failed" }

$Exe = Get-ChildItem -Path (Join-Path $RepoRoot "build") -Recurse -Filter "HymnOS.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $Exe) {
    throw "Built executable HymnOS.exe was not found under build/"
}

New-Item -ItemType Directory -Force -Path $DistDir | Out-Null
Copy-Item -Path $Exe.FullName -Destination (Join-Path $DistDir "HymnOS.exe") -Force

Write-Host "Build complete: $DistDir\HymnOS.exe" -ForegroundColor Green
