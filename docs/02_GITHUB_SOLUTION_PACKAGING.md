# GitHub Solution Packaging Guide
**Using GitHub for Power Platform Version Control**

## Overview

This guide explains how to structure, version control, and package Microsoft Power Platform solutions using GitHub. Unlike traditional Power Platform development (which typically uses Power Apps Studio + ALM Accelerator), this approach treats solutions as code, enabling full Git workflows, code review, and CI/CD pipelines.

## Why Version Control Power Platform Solutions?

**Traditional Approach Problems**:
- Solutions stored in binary .zip files - not diff-able
- Changes hidden until export/import
- No code review possible
- Difficult to track what changed and why
- Manual packaging prone to errors

**GitHub Approach Benefits**:
- ✅ **Transparent changes**: XML files show exactly what changed
- ✅ **Code review**: PR workflows for solution changes
- ✅ **Version history**: Full audit trail of modifications
- ✅ **Collaboration**: Multiple developers can work simultaneously
- ✅ **Automation**: Scripts can generate/modify solutions
- ✅ **Documentation**: Inline comments explain design decisions

## Power Platform Solution Structure

### What is a Power Platform Solution?

A Power Platform solution is a **ZIP file** containing:
- Entity/table definitions (XML)
- Canvas apps (.msapp files - also ZIPs!)
- Power Automate flows (JSON)
- Security roles, plugins, etc.
- Manifest files ([Content_Types].xml, solution.xml)

### Unzipped Solution Structure

```
PerformanceManagement.zip (when extracted)
├── [Content_Types].xml      # MIME type mappings
├── solution.xml              # Solution manifest (never edit directly!)
├── Other/
│   ├── Solution.xml          # Solution metadata (version, publisher, components)
│   ├── Customizations.xml    # Entity definitions, fields, relationships
│   └── Relationships.xml     # Entity relationships (sometimes separate)
├── Workflows/
│   ├── AdHocSelfEvalRequest-{guid}.json
│   ├── QuarterlySelfEvalReminder-{guid}.json
│   └── ...
├── CanvasApps/
│   └── pm_performancemanagement_{guid}_DocumentUri.msapp
└── WebResources/
    └── ...
```

### Key Files Explained

**[Content_Types].xml**:
- Maps file extensions to MIME types
- Required for ZIP package parsing
- Auto-generated based on contents

**solution.xml** (root):
- Temporary manifest file
- Generated during packaging
- **Never edit this file directly** - edit `Other/Solution.xml` instead

**Other/Solution.xml**:
- Solution metadata: name, version, publisher
- RootComponents list (which entities/apps are in the solution)
- **This is what you edit** to change solution info

**Other/Customizations.xml**:
- ALL entity definitions
- Field (attribute) definitions
- Relationships between entities
- Forms, views, charts (if applicable)
- **Largest and most important file**

## GitHub Repository Structure

### Recommended Layout

```
ContinousPerformanceManagementApp/
├── .github/
│   └── workflows/
│       └── package-solution.yml    # CI/CD automation
├── solution/                        # Unpacked solution files
│   ├── Other/
│   │   ├── Solution.xml
│   │   └── Customizations.xml
│   ├── Workflows/                   # Flow JSONs
│   │   └── *.json
│   └── [Content_Types].xml
├── releases/                        # Packaged ZIPs for deployment
│   ├── PerformanceManagement_v2.0.0.7.zip
│   └── README.md                    # Release notes
├── deployment/                      # Scripts for packaging/deploying
│   ├── pack-solution.sh
│   ├── pack-solution.ps1
│   └── import-solution.ps1
├── docs/                            # Documentation
│   └── ...
├── ref/                             # Reference materials (Microsoft templates)
│   └── ...
├── .gitignore                       # Exclude temp files, ZIPs, etc.
└── README.md                        # Project overview
```

### Why This Structure?

**`solution/` directory** - Unzipped solution:
- XML files can be diffed and reviewed
- Changes visible in pull requests
- Can be edited with any text editor
- Scripts can generate/modify programmatically

**`releases/` directory** - Packaged solutions:
- Final ZIP files ready for import
- Named with version numbers for clarity
- Typically .gitignore'd or only include major releases
- Built from `solution/` directory

**`deployment/` scripts** - Automation:
- Package solution (ZIP creation)
- Deploy to environments
- Validate solution structure
- Version incrementing

## Packaging Process

### Manual Packaging (ZIP Creation)

The packaged solution is created by:

1. **Navigate to solution directory**:
   ```bash
   cd solution/
   ```

2. **Create ZIP with correct structure**:
   ```bash
   zip -r ../releases/PerformanceManagement_v2.0.0.7.zip . \
     -x "*.DS_Store" \
     -x "__MACOSX/*"
   ```

   **Important**: ZIP must contain files at root level, not wrapped in a folder!

3. **Verify structure**:
   ```bash
   unzip -l ../releases/PerformanceManagement_v2.0.0.7.zip | head -20
   ```

   Should show:
   ```
   [Content_Types].xml
   solution.xml
   Other/Solution.xml
   Other/Customizations.xml
   ...
   ```

   NOT:
   ```
   solution/[Content_Types].xml   ← WRONG!
   ```

### Automated Packaging Script

**deployment/pack-solution.sh**:
```bash
#!/bin/bash
# Package Power Platform solution from source files

VERSION=$(grep '<Version>' solution/Other/Solution.xml | sed 's/.*<Version>\(.*\)<\/Version>/\1/')
OUTPUT="releases/PerformanceManagement_v${VERSION}.zip"

echo "Packaging solution version ${VERSION}..."

cd solution/
zip -r "../${OUTPUT}" . \
  -x "*.DS_Store" \
  -x "__MACOSX/*" \
  -x "*.swp" \
  -x "*~"

cd ..

if [ -f "${OUTPUT}" ]; then
  SIZE=$(ls -lh "${OUTPUT}" | awk '{print $5}')
  SHA=$(shasum -a 256 "${OUTPUT}" | awk '{print $1}')

  echo "✓ Package created: ${OUTPUT}"
  echo "  Size: ${SIZE}"
  echo "  SHA256: ${SHA}"
else
  echo "✗ Failed to create package"
  exit 1
fi
```

**PowerShell version (pack-solution.ps1)**:
```powershell
$version = (Select-Xml -Path "solution/Other/Solution.xml" -XPath "//Version").Node.InnerText
$output = "releases/PerformanceManagement_v$version.zip"

Write-Host "Packaging solution version $version..."

Compress-Archive -Path "solution/*" -DestinationPath $output -Force

if (Test-Path $output) {
    $size = (Get-Item $output).Length / 1KB
    $hash = (Get-FileHash $output -Algorithm SHA256).Hash

    Write-Host "✓ Package created: $output"
    Write-Host "  Size: $([math]::Round($size, 2)) KB"
    Write-Host "  SHA256: $hash"
} else {
    Write-Host "✗ Failed to create package"
    exit 1
}
```

## Version Management

### Semantic Versioning for Solutions

Follow semantic versioning: `MAJOR.MINOR.PATCH.BUILD`

**Example**: `2.0.0.7`
- **MAJOR** (2): Breaking changes to data model
- **MINOR** (0): New features, backward-compatible
- **PATCH** (0): Bug fixes
- **BUILD** (7): Incremental builds/fixes

### Where Version is Stored

**In `Other/Solution.xml`**:
```xml
<Version>2.0.0.7</Version>
```

### Incrementing Version

**Manual**:
```bash
# Edit solution/Other/Solution.xml
<Version>2.0.0.7</Version>  →  <Version>2.0.0.8</Version>
```

**Automated Script**:
```python
#!/usr/bin/env python3
import re

with open('solution/Other/Solution.xml', 'r') as f:
    content = f.read()

# Find current version
match = re.search(r'<Version>(\d+)\.(\d+)\.(\d+)\.(\d+)</Version>', content)
if match:
    major, minor, patch, build = map(int, match.groups())
    new_version = f"{major}.{minor}.{patch}.{build + 1}"

    # Update version
    content = re.sub(
        r'<Version>\d+\.\d+\.\d+\.\d+</Version>',
        f'<Version>{new_version}</Version>',
        content
    )

    with open('solution/Other/Solution.xml', 'w') as f:
        f.write(content)

    print(f"Version incremented to {new_version}")
```

### Release Naming Convention

**releases/ folder**:
```
PerformanceManagement_v2.0.0.7.zip   ← Version in filename
PerformanceManagement_v2.0.0.8.zip
```

Benefits:
- Easy to identify which version you're deploying
- No confusion about "latest"
- Can keep multiple versions for rollback

## Git Workflows

### Initial Setup

```bash
# Initialize repository
git init
git add solution/ deployment/ docs/ README.md .gitignore
git commit -m "Initial commit: Performance Management solution v2.0.0.0"

# Create .gitignore
cat > .gitignore <<EOF
# Packaged solutions (keep only releases/)
*.zip
!releases/*.zip

# Temporary files
*.tmp
*.swp
*~
.DS_Store
__MACOSX/

# Python cache
__pycache__/
*.pyc

# Build artifacts
build/
dist/
EOF
```

### Making Changes Workflow

1. **Create feature branch**:
   ```bash
   git checkout -b feature/add-recognition-entity
   ```

2. **Edit solution files** (e.g., `solution/Other/Customizations.xml`):
   - Add new entity definition
   - Add relationships
   - Update entity schemas

3. **Increment version**:
   ```bash
   ./increment_version.py  # or manual edit
   ```

4. **Package solution**:
   ```bash
   ./deployment/pack-solution.sh
   ```

5. **Test import** in dev environment

6. **Commit changes**:
   ```bash
   git add solution/Other/
   git commit -m "Add Recognition entity with fields and relationships

   - Added pm_recognition entity
   - Added lookup to pm_staffmember
   - Added date, description, and recognizedby fields
   - Version 2.0.1.0"
   ```

7. **Create pull request** for review

8. **Merge to main** after approval

### Commit Message Best Practices

**Good commit messages**:
```
Remove <Format> elements from datetime fields

Teams Dataverse doesn't accept <Format>DateAndTime</Format> on
datetime type columns. Removed from all 9 datetime fields.

Fixes import error: "The format DateAndTime is not valid for the
datetime type column pm_startdate"

Version: 2.0.0.1
```

**Bad commit messages**:
```
Fixed stuff
Updated XML
Version 2.0.0.1
```

### Pull Request Template

```markdown
## Description
Add Recognition entity for logging employee kudos and achievements

## Changes
- New entity: pm_recognition
- Fields: date, description, recognizedby (lookup to Staff Member)
- Relationship: pm_staffmember → pm_recognition (1:N)

## Testing
- [x] Solution imports successfully to Teams Dataverse
- [x] Entity visible in Power Apps
- [x] Lookup relationship works
- [x] No validation errors

## Version
2.0.1.0

## Deployment Notes
No breaking changes. Safe to import over existing 2.0.0.x versions.
```

## CI/CD Automation

### GitHub Actions Workflow

**.github/workflows/package-solution.yml**:
```yaml
name: Package Solution

on:
  push:
    branches: [ main ]
    paths:
      - 'solution/**'
  workflow_dispatch:

jobs:
  package:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Read version
      id: version
      run: |
        VERSION=$(grep '<Version>' solution/Other/Solution.xml | sed 's/.*<Version>\(.*\)<\/Version>/\1/')
        echo "version=$VERSION" >> $GITHUB_OUTPUT

    - name: Package solution
      run: |
        cd solution/
        zip -r "../PerformanceManagement_v${{ steps.version.outputs.version }}.zip" . \
          -x "*.DS_Store" -x "__MACOSX/*"

    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: solution-package
        path: "*.zip"

    - name: Create Release
      if: startsWith(github.ref, 'refs/tags/v')
      uses: softprops/action-gh-release@v1
      with:
        files: "*.zip"
```

### Benefits of CI/CD

- ✅ **Automatic packaging** on every push to main
- ✅ **Validation** that solution structure is correct
- ✅ **Release artifacts** attached to GitHub releases
- ✅ **Version consistency** enforced
- ✅ **No manual ZIP creation** required

## Common Pitfalls

### 1. ZIP Structure Wrong

**Problem**: ZIP contains a parent folder
```
solution/[Content_Types].xml   ← WRONG!
solution/Other/Solution.xml
```

**Solution**: CD into solution/ directory before zipping
```bash
cd solution/
zip -r ../output.zip .    # Note the period (.)
```

### 2. Line Ending Issues

**Problem**: Windows CRLF vs. Unix LF line endings cause diffs

**Solution**: Configure Git
```bash
git config core.autocrlf true   # Windows
git config core.autocrlf input  # macOS/Linux
```

Add `.gitattributes`:
```
*.xml text eol=lf
*.json text eol=lf
*.md text eol=lf
```

### 3. Version Not Updated

**Problem**: Forgot to increment version before packaging

**Solution**: Add pre-commit hook or CI check
```bash
#!/bin/bash
# .git/hooks/pre-commit
VERSION=$(grep '<Version>' solution/Other/Solution.xml | sed 's/.*<Version>\(.*\)<\/Version>/\1/')
echo "Current version: $VERSION"
echo "Did you increment the version? (y/n)"
read answer
if [ "$answer" != "y" ]; then
  echo "Commit aborted. Please increment version first."
  exit 1
fi
```

### 4. Forgetting to Package

**Problem**: Edited solution files but didn't create new ZIP

**Solution**: Automate with GitHub Actions or always run pack script before commit

## Best Practices

### 1. Keep releases/ Clean

Only commit final release ZIPs, not intermediate builds:
```gitignore
# .gitignore
releases/*.zip
!releases/PerformanceManagement_v2.0.0.7.zip  # Only keep final releases
```

### 2. Document Breaking Changes

In commit message and RELEASE_NOTES.md:
```markdown
## Version 2.0.0.0 → 3.0.0.0 (BREAKING)

### Breaking Changes
- Renamed pm_supervisor field to pm_manager
- Changed pm_rating from OptionSet to Integer
- Removed pm_oldfield (no longer used)

### Migration Steps
1. Export data from pm_supervisor field
2. Import solution v3.0.0.0
3. Re-import data to pm_manager field
```

### 3. Tag Releases in Git

```bash
git tag -a v2.0.0.7 -m "Release 2.0.0.7: Working Dataverse import"
git push origin v2.0.0.7
```

Creates a permanent reference point for this version.

### 4. Code Review Even Solo

Even working alone, create PRs for:
- Review your own changes before merging
- Document why changes were made
- Create audit trail
- Practice good habits

## Advanced: Multi-Environment Strategy

### Development Workflow

```
feature/xyz → dev → staging → main → production
     ↓         ↓       ↓        ↓          ↓
   (local)  (dev env) (test) (release) (prod import)
```

**Branches**:
- `feature/*` - Individual features
- `dev` - Integration testing
- `staging` - Pre-production validation
- `main` - Production-ready code

**Environments**:
- Local editing (no Dataverse)
- Dev Dataverse environment (testing)
- Staging Dataverse (validation)
- Production Dataverse (live)

## Conclusion

Using GitHub for Power Platform solutions enables:
- **Transparent version control** of all solution changes
- **Code review workflows** for quality assurance
- **Automated packaging** and deployment
- **Full audit trail** of who changed what and why
- **Collaboration** between multiple developers

This approach treats Power Platform solutions as code, bringing modern software development practices to low-code/no-code platforms.

The key is maintaining the unzipped `solution/` directory in Git while using scripts to package into ZIP files for deployment.
