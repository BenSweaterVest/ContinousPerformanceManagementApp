# Performance Management Solution - Manual Pack Script (Windows)
# This script creates the solution ZIP manually without using pac CLI

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Manual Solution Pack (No PAC CLI)" -ForegroundColor Cyan
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

Write-Host "Verifying solution files..." -ForegroundColor Yellow
$requiredFiles = @(
    (Join-Path $solutionDir "[Content_Types].xml"),
    (Join-Path $solutionDir "Other/Solution.xml"),
    (Join-Path $solutionDir "Other/Customizations.xml")
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (MISSING)" -ForegroundColor Red
        $allFilesExist = $false
    }
}
Write-Host ""

if (-not $allFilesExist) {
    Write-Host "ERROR: Required solution files are missing!" -ForegroundColor Red
    exit 1
}

$customizationsPath = Join-Path $solutionDir "Other/Customizations.xml"
$customizationsInfo = Get-Item $customizationsPath
Write-Host ("Customizations.xml size: {0:N0} KB" -f ($customizationsInfo.Length / 1KB)) -ForegroundColor White
Write-Host ""

if (!(Test-Path $releaseDir)) {
    New-Item -ItemType Directory -Path $releaseDir | Out-Null
}

$outputFile = "PerformanceManagement_v$version.zip"
$outputPath = Join-Path $releaseDir $outputFile

if (Test-Path $outputPath) {
    Write-Host "Removing existing package..." -ForegroundColor Yellow
    Remove-Item $outputPath -Force
}

Write-Host "Creating ZIP package (manual method)..." -ForegroundColor Yellow
Add-Type -AssemblyName System.IO.Compression.FileSystem

try {
    [System.IO.Compression.ZipFile]::CreateFromDirectory(
        $solutionDir,
        $outputPath,
        [System.IO.Compression.CompressionLevel]::Optimal,
        $false
    )

    $fileInfo = Get-Item $outputPath
    $hash = (Get-FileHash $outputPath -Algorithm SHA256).Hash

    Write-Host ""
    Write-Host "======================================" -ForegroundColor Green
    Write-Host "SUCCESS: Solution packed!" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Green
    Write-Host ""
    Write-Host ("Output file : releases/{0}" -f $outputFile) -ForegroundColor White
    Write-Host ("File size   : {0:N0} KB" -f ($fileInfo.Length / 1KB)) -ForegroundColor White
    Write-Host ("SHA256      : {0}" -f $hash) -ForegroundColor White
    Write-Host ""
    Write-Host "Package contents preview:" -ForegroundColor Yellow

    $zip = [System.IO.Compression.ZipFile]::OpenRead($outputPath)
    $zip.Entries | Select-Object -First 10 | ForEach-Object {
        Write-Host ("  • {0}" -f $_.FullName) -ForegroundColor White
    }
    if ($zip.Entries.Count -gt 10) {
        Write-Host ("  • ... ({0} total entries)" -f $zip.Entries.Count) -ForegroundColor White
    }
    $zip.Dispose()

    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Import releases/$outputFile into Teams Dataverse (Teams → Power Apps → Build → Import)" -ForegroundColor White
    Write-Host "  2. Or run import-solution.ps1 with your environment credentials" -ForegroundColor White
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "======================================" -ForegroundColor Red
    Write-Host "ERROR: Failed to create ZIP!" -ForegroundColor Red
    Write-Host "======================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    exit 1
}
