# Performance Management Solution - Manual Pack Script (Windows)
# This script creates the solution ZIP manually without using pac CLI
# Use this if pac solution pack is giving errors

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Manual Solution Pack (No PAC CLI)" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
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

# Verify required files exist
$requiredFiles = @(
    "solution/[Content_Types].xml",
    "solution/Other/Solution.xml",
    "solution/Other/Customizations.xml"
)

Write-Host "Verifying solution files..." -ForegroundColor Yellow
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

if (!$allFilesExist) {
    Write-Host "ERROR: Required solution files are missing!" -ForegroundColor Red
    exit 1
}

# Check Customizations.xml size (should be ~500KB if fixed)
$customizationsPath = "solution/Other/Customizations.xml"
$customizationsInfo = Get-Item $customizationsPath
$sizeKB = [math]::Round($customizationsInfo.Length / 1KB, 0)

Write-Host "Customizations.xml size: $sizeKB KB" -ForegroundColor White

if ($sizeKB -lt 450) {
    Write-Host "WARNING: File seems too small (expected ~500KB)" -ForegroundColor Yellow
    Write-Host "This might indicate the fixes haven't been applied yet." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You may need to:" -ForegroundColor Yellow
    Write-Host "  1. Run: python quick_fix_customizations.py" -ForegroundColor White
    Write-Host "  2. Or download the latest version from GitHub" -ForegroundColor White
    Write-Host ""

    $response = Read-Host "Continue anyway? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "Aborted by user" -ForegroundColor Yellow
        exit 1
    }
}
Write-Host ""

# Create the ZIP file
$outputFile = "PerformanceManagement_1_0_0_1.zip"
$outputPath = Join-Path $projectRoot $outputFile

# Remove existing zip if present
if (Test-Path $outputPath) {
    Write-Host "Removing existing package..." -ForegroundColor Yellow
    Remove-Item $outputPath -Force
}

Write-Host "Creating ZIP package (manual method)..." -ForegroundColor Yellow

# Create ZIP using .NET compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

try {
    # Create the ZIP archive
    [System.IO.Compression.ZipFile]::CreateFromDirectory(
        (Join-Path $projectRoot "solution"),
        $outputPath,
        [System.IO.Compression.CompressionLevel]::Optimal,
        $false  # Don't include base directory
    )

    Write-Host ""
    Write-Host "======================================" -ForegroundColor Green
    Write-Host "SUCCESS: Solution packed!" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Output file: $outputFile" -ForegroundColor White
    Write-Host "Location: $projectRoot" -ForegroundColor White
    Write-Host ""

    $fileInfo = Get-Item $outputPath
    Write-Host "File size: $([math]::Round($fileInfo.Length / 1KB, 0)) KB" -ForegroundColor White
    Write-Host ""

    Write-Host "Package Contents:" -ForegroundColor Yellow

    # List contents of ZIP
    $zip = [System.IO.Compression.ZipFile]::OpenRead($outputPath)
    $zip.Entries | ForEach-Object {
        Write-Host "  • $($_.FullName)" -ForegroundColor White
    }
    $zip.Dispose()

    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Import this ZIP into Teams Dataverse:" -ForegroundColor White
    Write-Host "     • Teams → Power Apps → Build tab" -ForegroundColor Gray
    Write-Host "     • Select your team → Import → Upload ZIP" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. Or use import-solution.ps1 to deploy via PAC CLI" -ForegroundColor White
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
