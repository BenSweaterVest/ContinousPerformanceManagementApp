# Releases

This folder contains pre-built solution packages for easy deployment.

## Latest Release

**Version:** 2.0.0.7
**File:** `PerformanceManagement_v2.0.0.7.zip`
**Status:** ✅ Successfully imports to Microsoft Teams Dataverse

### What's Included

- 9 Dataverse entities with complete schema
- All field definitions and relationships
- Power Automate flow templates (JSON files for reference)
- Solution metadata

**Note:** This version contains the data layer only. Canvas app and flows must be built separately in Power Apps Studio.

### Download

Download the ZIP file directly from this folder or from the [GitHub Releases page](../../releases).

### Installation

1. Download `PerformanceManagement_v2.0.0.7.zip`
2. Open Microsoft Teams → Power Apps app → Build tab
3. Select your team → "Import your solution"
4. Browse and select the ZIP file
5. Click "Next" → "Import"
6. Wait 5-15 minutes for import to complete

**Full instructions:** [DEPLOYMENT-GUIDE.md](../docs/DEPLOYMENT-GUIDE.md)

### What Happens After Import

After successful import, you'll have:
- ✅ 9 custom tables visible in your Dataverse for Teams environment
- ✅ All fields and relationships configured
- ✅ Ready for canvas app development

### Next Steps

1. **Add Evaluation Questions** - Populate the pm_evaluationquestion table with your 12 evaluation criteria
2. **Build Canvas App** - Use Power Apps Studio to create the user interface (see [03_AI_CANVAS_APP_GUIDE.md](../docs/03_AI_CANVAS_APP_GUIDE.md))
3. **Create Flows** - Build Power Automate flows using the templates in `solution/Workflows/`

### Building from Source

If you want to rebuild the solution package yourself:

```bash
# Windows
cd deployment
.\pack-solution.ps1

# Mac/Linux
cd deployment
chmod +x pack-solution.sh
./pack-solution.sh
```

The ZIP file will be created in the `releases/` folder.

### Version History

See [RELEASE_NOTES.md](../docs/RELEASE_NOTES.md) for detailed version history and changelog.

### Support

- **Documentation:** See the `docs/` folder for comprehensive guides
- **Issues:** The solution has been tested and successfully imports to Teams Dataverse
- **Learning:** See [04_SOLUTION_FIXES_JOURNEY.md](../docs/04_SOLUTION_FIXES_JOURNEY.md) for the complete troubleshooting journey
