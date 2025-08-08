param(
  [switch]$Clean
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# always run from repo root if script is called from anywhere
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $scriptDir "..")

if ($Clean) {
  if (Test-Path .\build) { Remove-Item -Recurse -Force .\build }
  if (Test-Path .\dist)  { Remove-Item -Recurse -Force .\dist }
}

pyinstaller .\moddock.spec
Write-Host "`nBuild finished -> dist\ModDock\ModDock.exe" -ForegroundColor Green
