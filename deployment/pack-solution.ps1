# Performance Management Solution - Pack Script (Windows)
# Creates a Teams-ready solution ZIP directly from solution/ contents

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Performance Management Solution Pack" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
$solutionDir = Join-Path $projectRoot "solution"
$releaseDir = Join-Path $projectRoot "releases"

if (!(Test-Path $solutionDir)) {
    Write-Host "ERROR: 'solution' folder not found!" -ForegroundColor Red
    exit 1
}

Write-Host "Project root: $projectRoot" -ForegroundColor White
Write-Host ""

[xml]$solutionXml = Get-Content (Join-Path $solutionDir "Other/Solution.xml")
$version = $solutionXml.ImportExportXml.SolutionManifest.Version

if ([string]::IsNullOrWhiteSpace($version)) {
    Write-Host "ERROR: Could not read <Version> from Solution.xml" -ForegroundColor Red
    exit 1
}

$outputFile = "PerformanceManagement_v$version.zip"
$outputPath = Join-Path $releaseDir $outputFile

if (!(Test-Path $releaseDir)) {
    New-Item -ItemType Directory -Path $releaseDir | Out-Null
}

Write-Host "Packaging version $version → releases/$outputFile" -ForegroundColor Yellow
Write-Host ""

if (Test-Path $outputPath) {
    Remove-Item $outputPath -Force
}

$sourcePattern = Join-Path $solutionDir '*'
Compress-Archive -Path $sourcePattern -DestinationPath $outputPath -Force

if (!(Test-Path $outputPath)) {
    Write-Host "ERROR: Failed to create $outputFile" -ForegroundColor Red
    exit 1
}

$fileInfo = Get-Item $outputPath
$hash = (Get-FileHash $outputPath -Algorithm SHA256).Hash

Write-Host "======================================" -ForegroundColor Green
Write-Host "SUCCESS: Solution packed!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host ("Output file : releases/{0}" -f $outputFile) -ForegroundColor White
Write-Host ("File size   : {0:N2} KB" -f ($fileInfo.Length / 1KB)) -ForegroundColor White
Write-Host ("SHA256      : {0}" -f $hash) -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Upload the ZIP via Microsoft Teams → Power Apps → Import" -ForegroundColor White
Write-Host "  2. Or run import-solution.ps1 with your environment credentials" -ForegroundColor White
Write-Host ""
