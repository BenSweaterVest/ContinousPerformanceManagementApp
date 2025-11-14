# Releases

This folder contains pre-built solution packages for easy deployment.

## Latest Release

**Version:** 1.0.0
**File:** `PerformanceManagement_1_0_0_0.zip`

### Download

If you're viewing this on GitHub, download the ZIP file from the [Releases page](../../releases).

### Building from Source

If you want to build the solution yourself:

```bash
# Windows
cd deployment
.\pack-solution.ps1

# Mac/Linux
cd deployment
chmod +x pack-solution.sh
./pack-solution.sh
```

The ZIP file will be created in the project root folder.

### What's in the ZIP

- 9 Dataverse tables
- 4 Power Automate flows
- Solution metadata
- All required XML and JSON files

### Installation

1. Download `PerformanceManagement_1_0_0_0.zip`
2. Open Microsoft Teams → Power Apps app → Build
3. Select your team → "Import your solution"
4. Browse to the ZIP → Import
5. Wait 5-15 minutes

**Full instructions:** [DEPLOYMENT-GUIDE.md](../docs/DEPLOYMENT-GUIDE.md)

### Release Notes

See [RELEASE_NOTES.md](../RELEASE_NOTES.md) for detailed information about this release.
