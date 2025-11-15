# Scripts Directory

This directory contains utility scripts used during the development and debugging of the Dataverse solution.

## Script Categories

### Fix Scripts (`fix_*.py`)
Scripts that correct specific issues in the Customizations.xml file:

- `fix_entity_name_casing.py` - Converts entity names to PascalCase (Error 9 fix)
- `fix_introduced_version.py` - Corrects IntroducedVersion pattern (system vs custom fields)
- `fix_display_mask.py` - Enhances DisplayMask values for system fields
- `fix_malformed_xml.py` - Fixes malformed XML structure (critical blocker)
- `fix_orphaned_closing_tags.py` - Removes duplicate closing tags
- `fix_*.py` - Various other targeted fixes

### Add Scripts (`add_*.py`)
Scripts that add missing elements or metadata:

- `add_system_relationships.py` - Generates 54 system entity relationships (Error 8 fix)
- `add_missing_attribute_metadata.py` - Adds 10 critical metadata elements to attributes
- `add_*.py` - Other attribute and metadata additions

### Utility Scripts
General-purpose utilities:

- `validate_msft_alignment.py` - Compares solution with Microsoft's Boards template
- `generate_relationships.py` - Generates relationship XML
- `find_lookup_fields.py` - Identifies lookup field patterns
- `merge_entities_to_customizations.py` - Merges entity definitions

## Usage

Most scripts are designed to be run from the repository root:

```bash
# Example: Fix entity name casing
python scripts/fix_entity_name_casing.py

# Example: Add system relationships
python scripts/add_system_relationships.py
```

## Important Notes

- **Always backup before running scripts** - Most create `.backup` files automatically
- **Scripts are idempotent** - Safe to run multiple times
- **Check script headers** - Each script includes usage instructions
- **Verify results** - Use `xmllint` to validate XML after changes

## Frequently Used Scripts at Root

Two commonly-used scripts remain at the repository root for convenience:

- `quick_fix_customizations.py` - All-in-one fix for downloaded versions
- `increment_version.py` - Version management utility

## Historical Context

These scripts were created during the debugging process to resolve 16 critical issues that prevented solution import. They're retained for:

1. **Documentation** - Shows the evolution of fixes
2. **Reusability** - Can be adapted for similar solutions
3. **Reference** - Demonstrates proper Dataverse XML structure
4. **Debugging** - Useful if new issues arise

For detailed information about the issues these scripts solve, see:
- `/docs/PROJECT_SUMMARY.md`
- `/docs/DEEP_ANALYSIS_FIXES_SUMMARY.md`
- `/ref/IMPORT-TROUBLESHOOTING-GUIDE.md`
