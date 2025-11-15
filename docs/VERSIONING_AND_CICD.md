# Versioning and CI/CD Guide

This document explains the automated versioning and continuous integration/deployment (CI/CD) system for the Performance Management Dataverse solution.

---

## 📌 Version Numbering

The solution uses **semantic versioning** with four components:

```
MAJOR.MINOR.BUILD.REVISION
  1  .  0  .  0  .  1
```

| Component | When to Increment | Example |
|-----------|-------------------|---------|
| **MAJOR** | Breaking changes, major rewrites | 1.0.0.0 → 2.0.0.0 |
| **MINOR** | New features, entities, or significant additions | 1.0.0.0 → 1.1.0.0 |
| **BUILD** | Bug fixes, improvements, refactoring | 1.0.0.0 → 1.0.1.0 |
| **REVISION** | Small fixes, documentation, minor tweaks | 1.0.0.0 → 1.0.0.1 |

---

## 🔄 Incrementing the Version

### Automatic Version Increment

Use the provided Python script to automatically update the version across all files:

```bash
# Increment revision (smallest change)
python increment_version.py revision    # 1.0.0.0 → 1.0.0.1

# Increment build (bug fixes)
python increment_version.py build       # 1.0.0.1 → 1.0.1.0

# Increment minor (new features)
python increment_version.py minor       # 1.0.1.0 → 1.1.0.0

# Increment major (breaking changes)
python increment_version.py major       # 1.1.0.0 → 2.0.0.0
```

### What Gets Updated

The script automatically updates:
- ✅ `solution/Other/Solution.xml` - The `<Version>` tag
- ✅ `deployment/pack-solution.ps1` - The output ZIP filename
- ✅ `deployment/pack-solution-manual.ps1` - The output ZIP filename
- ✅ `deployment/import-solution.ps1` - The expected input ZIP filename

### Example Session

```bash
$ python increment_version.py build

======================================================================
Performance Management Solution - Version Increment
======================================================================

Current version: 1.0.0.1
New version:     1.0.1.0 (incrementing build)

Proceed with version update? (y/N): y

Updating files...
   ✓ Updated Solution.xml
   ✓ Updated 3 pack/import scripts
     • deployment/pack-solution.ps1
     • deployment/pack-solution-manual.ps1
     • deployment/import-solution.ps1

======================================================================
✅ SUCCESS: Version updated to 1.0.1.0
======================================================================

Files updated:
  • solution/Other/Solution.xml
  • deployment/pack-solution.ps1
  • deployment/pack-solution-manual.ps1
  • deployment/import-solution.ps1

Next steps:
  1. Review the changes
  2. Run deployment scripts to create new package
  3. Commit: git add . && git commit -m 'Bump version to 1.0.1.0'
```

---

## 🤖 GitHub Actions CI/CD

The repository includes two GitHub Actions workflows for automated building and releasing.

### Workflow 1: Build Solution (Continuous Integration)

**File:** `.github/workflows/build-solution.yml`

**Triggers:**
- Push to `main` branch
- Push to any `claude/**` branch
- Pull requests to `main`
- Manual trigger via GitHub UI

**What It Does:**
1. ✅ Validates XML structure (Customizations.xml, Solution.xml)
2. ✅ Checks file sizes (ensures fixes are applied)
3. ✅ Creates solution ZIP package
4. ✅ Verifies package contents
5. ✅ Uploads package as artifact
6. ✅ Generates build summary

**How to Use:**
- Automatically runs on every push
- Download artifacts from Actions tab: `PerformanceManagement-v1.0.0.1`
- Artifacts retained for 90 days

**Manual Trigger:**
1. Go to GitHub → Actions tab
2. Select "Build Dataverse Solution"
3. Click "Run workflow"
4. Select branch
5. Click "Run workflow" button

### Workflow 2: Create Release

**File:** `.github/workflows/release.yml`

**Triggers:**
- Push of version tags (e.g., `v1.0.0.1`, `v1.1.0.0`)

**What It Does:**
1. ✅ Validates tag matches Solution.xml version
2. ✅ Creates solution package
3. ✅ Generates comprehensive release notes
4. ✅ Creates GitHub Release
5. ✅ Attaches solution ZIP to release
6. ✅ Uploads long-term artifacts (365 days)

**How to Create a Release:**

```bash
# 1. Increment version
python increment_version.py minor

# 2. Commit changes
git add .
git commit -m "Bump version to 1.1.0.0"

# 3. Create and push tag
git tag v1.1.0.0
git push origin v1.1.0.0

# 4. GitHub Actions automatically creates the release
```

**Release Includes:**
- 📦 Solution ZIP package
- 📝 Auto-generated release notes
- 📋 Installation instructions
- 📊 Technical details
- 🆘 Troubleshooting guide
- 🔗 Resource links

---

## 📋 Recommended Workflow

### For Small Changes (Documentation, Minor Fixes)

```bash
# 1. Make your changes
# 2. Increment revision
python increment_version.py revision

# 3. Test locally
.\deployment\pack-solution.ps1

# 4. Commit
git add .
git commit -m "Fix: Update documentation [v1.0.0.2]"
git push

# 5. GitHub Actions builds automatically
# 6. Download from Actions artifacts if needed
```

### For Bug Fixes

```bash
# 1. Make your fixes
# 2. Increment build
python increment_version.py build

# 3. Test
.\deployment\pack-solution.ps1

# 4. Commit
git add .
git commit -m "Fix: Resolve relationship issue [v1.0.1.0]"
git push

# 5. Create release tag
git tag v1.0.1.0
git push origin v1.0.1.0

# 6. Check GitHub Releases for published release
```

### For New Features

```bash
# 1. Implement feature
# 2. Increment minor version
python increment_version.py minor

# 3. Test thoroughly
.\deployment\pack-solution.ps1

# 4. Commit
git add .
git commit -m "Feature: Add new evaluation workflow [v1.1.0.0]"
git push

# 5. Create release
git tag v1.1.0.0
git push origin v1.1.0.0

# 6. Publish release notes on GitHub
```

### For Major Changes

```bash
# 1. Complete major refactoring/rewrite
# 2. Increment major version
python increment_version.py major

# 3. Extensive testing
.\deployment\pack-solution.ps1

# 4. Commit
git add .
git commit -m "BREAKING: Redesign entity structure [v2.0.0.0]"
git push

# 5. Create release with detailed notes
git tag v2.0.0.0
git push origin v2.0.0.0

# 6. Update documentation for breaking changes
```

---

## 🎯 Build Artifacts

### Where to Find Builds

1. **GitHub Actions Tab**
   - Go to repository → Actions
   - Select workflow run
   - Scroll to "Artifacts" section
   - Download `PerformanceManagement-v1.0.0.1`

2. **GitHub Releases**
   - Go to repository → Releases
   - Find your version (e.g., v1.0.0.1)
   - Download attached ZIP file

### Artifact Retention

| Source | Retention Period | Use Case |
|--------|------------------|----------|
| **Actions Artifacts** | 90 days | Development, testing |
| **Release Artifacts** | 365 days | Production deployments |
| **Tagged Releases** | Permanent | Long-term reference |

---

## ✅ Validation Checks

GitHub Actions performs these validations on every build:

### XML Structure Validation
- ✅ Customizations.xml is well-formed
- ✅ Solution.xml is well-formed
- ✅ No malformed tags or attributes

### File Size Checks
- ✅ Customizations.xml ≥ 450 KB (ensures fixes applied)
- ✅ Package ZIP created successfully
- ✅ Package size reasonable (60-130 KB)

### Content Verification
- ✅ Solution.xml present in package
- ✅ Customizations.xml present in package
- ✅ All required directories included

### Version Validation (Releases Only)
- ✅ Git tag matches Solution.xml version
- ✅ No version mismatch errors

---

## 🔧 Manual Build Options

If GitHub Actions is unavailable or you need local builds:

### Option 1: PowerShell with pac CLI
```powershell
.\deployment\pack-solution.ps1
```

### Option 2: PowerShell Manual (No pac CLI)
```powershell
.\deployment\pack-solution-manual.ps1
```

### Option 3: Python + Bash/Linux
```bash
python quick_fix_customizations.py  # If needed
cd solution
zip -r ../PerformanceManagement_1_0_0_1.zip .
```

---

## 📊 Version History

Current versioning approach:

| Version | Date | Type | Description |
|---------|------|------|-------------|
| 1.0.0.0 | Initial | - | Initial hand-written solution |
| 1.0.0.1 | 2025-11-15 | Revision | Added versioning system and CI/CD |

Future versions will be documented automatically in GitHub Releases.

---

## 🆘 Troubleshooting

### "Version mismatch" error in release workflow

**Problem:** Tag doesn't match Solution.xml version

**Solution:**
```bash
# Check current version
grep '<Version>' solution/Other/Solution.xml

# Make sure tag matches
git tag v1.0.0.1  # Must match exactly
```

### Build artifact not appearing

**Problem:** Workflow completed but no artifact

**Causes:**
- Workflow failed validation
- XML errors in solution files
- Package creation failed

**Solution:**
- Check workflow logs for errors
- Run `xmllint` on XML files locally
- Verify file permissions

### Manual builds work but Actions fail

**Problem:** Local builds succeed, CI/CD fails

**Common Issues:**
- Line ending differences (CRLF vs LF)
- File permissions
- Missing files in repository

**Solution:**
```bash
# Check what's committed
git status
git ls-files solution/

# Verify all files are tracked
git add solution/
git commit -m "Ensure all solution files tracked"
```

---

## 📚 Additional Resources

- **increment_version.py** - Version increment script
- **ALTERNATIVE_SOLUTIONS.md** - Manual build methods
- **DATAVERSE_SOLUTION_CHECKLIST.md** - Technical reference
- **.github/workflows/** - CI/CD configurations

---

## 🎯 Quick Reference

```bash
# Increment version
python increment_version.py revision

# Test build locally
.\deployment\pack-solution.ps1

# Commit changes
git add .
git commit -m "Update: Brief description [v1.0.0.2]"

# Push (triggers CI build)
git push

# Create release (optional)
git tag v1.0.0.2
git push origin v1.0.0.2
```

---

**Last Updated:** 2025-11-15
**Current Version:** 1.0.0.1
**CI/CD Status:** ✅ Fully Automated
