# Performance Management Solution - Import Script (Windows)
# This script imports the Power Platform solution into a Dataverse environment

param(
    [Parameter(Mandatory=$false)]
    [string]$EnvironmentId,

    [Parameter(Mandatory=$false)]
    [string]$EnvironmentUrl,

    [Parameter(Mandatory=$false)]
    [string]$PackagePath
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Performance Management Solution Import" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if PAC CLI is installed
Write-Host "Checking for Power Platform CLI..." -ForegroundColor Yellow
if (!(Get-Command "pac" -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Power Platform CLI not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install PAC CLI:" -ForegroundColor Yellow
    Write-Host "  dotnet tool install --global Microsoft.PowerApps.CLI.Tool" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "Found PAC CLI" -ForegroundColor Green
Write-Host ""

# Navigate to project root
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

[xml]$solutionXml = Get-Content "solution/Other/Solution.xml"
$version = $solutionXml.ImportExportXml.SolutionManifest.Version

if ([string]::IsNullOrWhiteSpace($version)) {
    Write-Host "ERROR: Could not read <Version> from Solution.xml" -ForegroundColor Red
    exit 1
}

$defaultPackage = Join-Path $projectRoot ("releases/PerformanceManagement_v{0}.zip" -f $version)

if ([string]::IsNullOrWhiteSpace($PackagePath)) {
    $packageFile = $defaultPackage
} elseif ([System.IO.Path]::IsPathRooted($PackagePath)) {
    $packageFile = $PackagePath
} else {
    $packageFile = Join-Path $projectRoot $PackagePath
}

if (!(Test-Path $packageFile)) {
    Write-Host "ERROR: Solution package not found: $packageFile" -ForegroundColor Red
    Write-Host ""
    Write-Host ("Expected path: {0}" -f $defaultPackage) -ForegroundColor Yellow
    Write-Host "Run pack-solution.ps1 to create it or pass -PackagePath with a custom ZIP." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host ("Found solution package: {0}" -f $packageFile) -ForegroundColor Green
Write-Host ""

# Check authentication
Write-Host "Checking authentication status..." -ForegroundColor Yellow
$authList = pac auth list 2>&1
if ($authList -match "No profiles") {
    Write-Host "Not authenticated to any environment" -ForegroundColor Yellow
    Write-Host ""

    if ([string]::IsNullOrWhiteSpace($EnvironmentId) -and [string]::IsNullOrWhiteSpace($EnvironmentUrl)) {
        Write-Host "Please provide environment credentials:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Option 1 - By Environment ID:" -ForegroundColor White
        Write-Host "  .\import-solution.ps1 -EnvironmentId 'your-env-id-here'" -ForegroundColor White
        Write-Host ""
        Write-Host "Option 2 - By Environment URL:" -ForegroundColor White
        Write-Host "  .\import-solution.ps1 -EnvironmentUrl 'https://yourorg.crm.dynamics.com'" -ForegroundColor White
        Write-Host ""
        Write-Host "To find your environment:" -ForegroundColor Yellow
        Write-Host "  1. Go to admin.powerplatform.microsoft.com" -ForegroundColor White
        Write-Host "  2. Select Environments" -ForegroundColor White
        Write-Host "  3. Copy the Environment ID or URL" -ForegroundColor White
        Write-Host ""
        exit 1
    }

    Write-Host "Authenticating..." -ForegroundColor Yellow
    if (![string]::IsNullOrWhiteSpace($EnvironmentId)) {
        pac auth create --environment $EnvironmentId
    } else {
        pac auth create --url $EnvironmentUrl
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Authentication failed!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Authenticated successfully" -ForegroundColor Green
Write-Host ""

# Import solution
Write-Host "Starting solution import..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Yellow
Write-Host ""

pac solution import `
    --path $packageFile `
    --async `
    --force-overwrite `
    --publish-changes

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "SUCCESS: Import initiated!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "The solution is being imported asynchronously." -ForegroundColor White
    Write-Host ""
    Write-Host "To monitor progress:" -ForegroundColor Yellow
    Write-Host "  1. Go to admin.powerplatform.microsoft.com" -ForegroundColor White
    Write-Host "  2. Select your environment" -ForegroundColor White
    Write-Host "  3. Go to Solutions" -ForegroundColor White
    Write-Host "  4. Look for 'Performance Management System'" -ForegroundColor White
    Write-Host ""
    Write-Host "After import completes:" -ForegroundColor Yellow
    Write-Host "  1. Configure connection references (Office 365, Dataverse)" -ForegroundColor White
    Write-Host "  2. Enable Power Automate flows" -ForegroundColor White
    Write-Host "  3. Share the Canvas app with users" -ForegroundColor White
    Write-Host "  4. Load seed data (12 evaluation questions)" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "ERROR: Import failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please review the error messages above" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
