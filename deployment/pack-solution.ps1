# Performance Management Solution - Pack Script (Windows)
# This script packs the Power Platform solution into a distributable ZIP file

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Performance Management Solution Pack" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if PAC CLI is installed
Write-Host "Checking for Power Platform CLI..." -ForegroundColor Yellow
if (!(Get-Command "pac" -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Power Platform CLI not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install PAC CLI:" -ForegroundColor Yellow
    Write-Host "  1. Install .NET SDK: https://dotnet.microsoft.com/download" -ForegroundColor White
    Write-Host "  2. Run: dotnet tool install --global Microsoft.PowerApps.CLI.Tool" -ForegroundColor White
    Write-Host ""
    exit 1
}

$pacVersion = pac --version 2>&1
Write-Host "Found PAC CLI: $pacVersion" -ForegroundColor Green
Write-Host ""

# Navigate to project root
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

Write-Host "Project root: $projectRoot" -ForegroundColor White
Write-Host ""

# Verify solution folder exists
if (!(Test-Path "solution")) {
    Write-Host "ERROR: 'solution' folder not found!" -ForegroundColor Red
    exit 1
}

# Pack the solution
Write-Host "Packing solution..." -ForegroundColor Yellow
Write-Host ""

$outputFile = "PerformanceManagement_1_0_0_1.zip"
$outputPath = Join-Path $projectRoot $outputFile

# Remove existing zip if present
if (Test-Path $outputPath) {
    Write-Host "Removing existing package..." -ForegroundColor Yellow
    Remove-Item $outputPath -Force
}

# Execute pack command
pac solution pack `
    --zipfile $outputFile `
    --folder "./solution" `
    --packagetype Unmanaged `
    --errorlevel Verbose

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "======================================" -ForegroundColor Green
    Write-Host "SUCCESS: Solution packed!" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Output file: $outputFile" -ForegroundColor White
    Write-Host "Location: $projectRoot" -ForegroundColor White
    Write-Host ""

    $fileInfo = Get-Item $outputPath
    Write-Host "File size: $([math]::Round($fileInfo.Length / 1MB, 2)) MB" -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Review the package" -ForegroundColor White
    Write-Host "  2. Run import-solution.ps1 to deploy" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "======================================" -ForegroundColor Red
    Write-Host "ERROR: Solution pack failed!" -ForegroundColor Red
    Write-Host "======================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please review the error messages above and:" -ForegroundColor Yellow
    Write-Host "  - Check all XML files are well-formed" -ForegroundColor White
    Write-Host "  - Verify solution structure" -ForegroundColor White
    Write-Host "  - Ensure all required files exist" -ForegroundColor White
    Write-Host ""
    exit 1
}
