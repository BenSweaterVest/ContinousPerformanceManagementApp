# GitHub Actions Setup Guide

This document explains how the GitHub Actions CI/CD workflows are configured for this Dataverse for Teams solution, including the challenges faced and solutions implemented.

## Overview

Two GitHub Actions workflows automate solution packaging:

1. **build-solution.yml** - Runs on every push to `main` and `claude/**` branches
2. **release.yml** - Runs when you create a version tag (e.g., `v1.0.1.0`)

Both workflows:
- Validate XML structure (Customizations.xml and Solution.xml)
- Package the solution using `pac solution pack`
- Create a proper ZIP file for Dataverse import
- Upload artifacts for download

## The pac CLI Installation Challenge

Installing the Power Platform CLI (`pac`) in GitHub Actions proved challenging. Here's what we tried and why they failed:

### ❌ Failed Approaches

| Approach | Why It Failed |
|----------|---------------|
| **Manual tarball from GitHub releases** | URL `https://github.com/microsoft/PowerApps-Cli/releases/download/v1.50.1/pac-x64.tar.gz` doesn't exist (404) |
| **dotnet tool install** | NuGet package has invalid metadata: `DotnetToolSettings.xml was not found in the package` |
| **microsoft/powerplatform-actions/actions-install@v1** | Installs pac but doesn't configure PATH correctly; pac not found in subsequent steps |
| **npm install @microsoft/powerplatform-cli** | Package doesn't exist in npm registry (404) |
| **microsoft/powerplatform-actions/setup-pac@v1** | Action doesn't exist in the repository |

### ✅ Working Solution

**Direct download from NuGet with full dependency extraction**

```yaml
- name: Install Power Platform CLI (Linux)
  run: |
    # Download NuGet package for Linux
    PAC_VERSION="1.49.4"
    PACKAGE_URL="https://www.nuget.org/api/v2/package/Microsoft.PowerApps.CLI.Core.linux-x64/${PAC_VERSION}"

    curl -L -o pac.nupkg "${PACKAGE_URL}"
    unzip -q pac.nupkg -d pac-temp

    # Find directory with pac.dll and all dependencies
    PAC_DIR=$(find pac-temp -type d -name "linux-x64" | head -1)
    if [ -z "$PAC_DIR" ]; then
      PAC_DIR=$(find pac-temp -type f -name "pac.dll" -exec dirname {} \; | head -1)
    fi

    # Copy ALL files to /usr/local/share/pac
    sudo mkdir -p /usr/local/share/pac
    sudo cp -r "$PAC_DIR"/* /usr/local/share/pac/
    sudo chmod +x /usr/local/share/pac/pac

    # Create symlink in /usr/local/bin
    sudo ln -sf /usr/local/share/pac/pac /usr/local/bin/pac

    # Verify
    pac --version
```

**Why This Works:**
- Downloads official Microsoft Linux binary from NuGet
- Extracts **all dependencies** (pac.dll, runtimes, libraries)
- Installs to `/usr/local/share/pac` with all files together
- Creates symlink so `pac` is in PATH
- The `pac` executable can find `pac.dll` and dependencies

**Critical Lesson:** The `pac` executable is a .NET application wrapper. It needs `pac.dll` and all .NET runtime files in the same directory. Only copying the `pac` executable fails with "The application to execute does not exist: '/usr/local/bin/pac.dll'".

## Workflow Files

### build-solution.yml

Triggers on:
- Push to `main` branch
- Push to any `claude/**` branch
- Pull requests to `main`
- Manual workflow dispatch

Steps:
1. Checkout repository
2. Get solution version from `solution/Other/Solution.xml`
3. Install dependencies (libxml2-utils, unzip)
4. Install pac CLI from NuGet
5. Validate Customizations.xml and Solution.xml
6. Create solution package with `pac solution pack`
7. Verify package contents
8. Upload artifact (90-day retention)

### release.yml

Triggers on:
- Git tags matching `v*.*.*.*` (e.g., `v1.0.1.0`)

Additional steps:
- Validates tag version matches `Solution.xml` version
- Creates GitHub Release with release notes
- Uploads solution package to release
- 365-day artifact retention (vs 90 days for builds)

## Using the Workflows

### Automatic Builds

Every push to `main` or `claude/**` branches automatically builds the solution:

```bash
git push origin main
```

Wait 5-10 minutes, then download artifact:
1. Go to GitHub Actions tab
2. Click the workflow run
3. Download `PerformanceManagement-v1.0.1.0` artifact

### Creating a Release

```bash
# Ensure Solution.xml has correct version
# <Version>1.0.1.0</Version>

# Create and push tag
git tag v1.0.1.0
git push origin v1.0.1.0
```

The release workflow will:
1. Validate tag matches Solution.xml version
2. Build the solution package
3. Create GitHub Release with release notes
4. Attach ZIP file to release

## Troubleshooting

### pac CLI Installation Fails

**Symptom:** `pac: command not found` or `pac.dll does not exist`

**Solution:** Check that the installation step:
1. Successfully downloads the NuGet package
2. Finds the `linux-x64` directory or `pac.dll` location
3. Copies ALL files to `/usr/local/share/pac`
4. Creates the symlink

**Debug:**
```yaml
# Add after unzip step to see package structure
- run: |
    echo "NuGet package contents:"
    ls -R pac-temp
```

### Version Mismatch (Release Workflow)

**Symptom:** Release workflow fails with "Version mismatch"

**Cause:** Git tag version doesn't match `<Version>` in `solution/Other/Solution.xml`

**Solution:**
```bash
# Check current version
grep '<Version>' solution/Other/Solution.xml

# Use increment_version.py to update
python increment_version.py --patch

# Or edit manually, then create matching tag
git tag v1.0.1.0
```

### XML Validation Fails

**Symptom:** `xmllint` reports XML errors

**Solution:** Validate XML locally before pushing:
```bash
# Install xmllint
sudo apt-get install libxml2-utils  # Ubuntu/Debian
brew install libxml2                # macOS

# Validate
xmllint --noout solution/Other/Customizations.xml
xmllint --noout solution/Other/Solution.xml
```

### Package is Empty or Missing Files

**Symptom:** ZIP file doesn't contain `solution.xml`, `customizations.xml`, or `[Content_Types].xml`

**Cause:** `pac solution pack` failed but didn't error

**Solution:** Check the "Create solution package" step logs for warnings

## Local Build Alternative

If GitHub Actions fails, build locally:

### Windows (PowerShell)

```powershell
# Install pac CLI
dotnet tool install --global Microsoft.PowerApps.CLI.Tool

# Build
cd /path/to/ContinousPerformanceManagementApp
.\deployment\pack-solution.ps1
```

### Linux/macOS

```bash
# Install pac CLI
dotnet tool install --global Microsoft.PowerApps.CLI.Tool

# Build
pac solution pack \
  --zipfile "PerformanceManagement_1_0_1_0.zip" \
  --folder "./solution" \
  --packagetype Unmanaged \
  --errorlevel Verbose
```

## pac CLI Version Pinning

The workflows use `PAC_VERSION="1.49.4"` (pinned).

**To update pac CLI version:**

1. Check available versions: https://www.nuget.org/packages/Microsoft.PowerApps.CLI.Core.linux-x64
2. Update `PAC_VERSION` in both workflow files:
   - `.github/workflows/build-solution.yml`
   - `.github/workflows/release.yml`
3. Test locally first:
   ```bash
   dotnet tool install --global Microsoft.PowerApps.CLI.Tool --version 1.50.1
   pac --version
   ```

## Artifact Downloads

### From Workflow Runs

1. Go to GitHub Actions: https://github.com/YOUR_ORG/ContinousPerformanceManagementApp/actions
2. Click the workflow run
3. Scroll to "Artifacts" section
4. Download `PerformanceManagement-v1.0.1.0.zip`

### From Releases

1. Go to Releases: https://github.com/YOUR_ORG/ContinousPerformanceManagementApp/releases
2. Find your version (e.g., `v1.0.1.0`)
3. Download the ZIP from "Assets" section

## Security Notes

- ✅ No secrets required (public NuGet package)
- ✅ No authentication needed for `pac solution pack`
- ✅ All tools installed from official sources
- ⚠️ Workflows use `sudo` for system-wide installation

## Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `pac: command not found` | pac not in PATH | Verify symlink creation step succeeded |
| `pac.dll does not exist` | Only pac executable copied, not dependencies | Ensure all files from NuGet package are copied |
| `File size: X KB (expected ~500KB)` | Customizations.xml fixes not applied | Run `python scripts/disable_audit_for_teams.py` |
| `ZIP file is invalid` | pac pack failed silently | Check for XML validation errors |
| `AsyncOperation entity not found` | Imported old ZIP before audit fix | Use ZIP from latest build (after commit 0ddd3a1) |

## References

- [Power Platform CLI Documentation](https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction)
- [NuGet Package: Microsoft.PowerApps.CLI.Core.linux-x64](https://www.nuget.org/packages/Microsoft.PowerApps.CLI.Core.linux-x64)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pac solution pack Documentation](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/solution#pac-solution-pack)

## Related Documentation

- [VERSIONING_AND_CICD.md](VERSIONING_AND_CICD.md) - Version management and release process
- [ALTERNATIVE_SOLUTIONS.md](ALTERNATIVE_SOLUTIONS.md) - Local build methods
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Overall project documentation

---

**Last Updated:** 2025-11-15
**pac CLI Version:** 1.49.4
**Solution Version:** 1.0.1.0
