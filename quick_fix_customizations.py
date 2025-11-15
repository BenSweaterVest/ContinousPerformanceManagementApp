#!/usr/bin/env python3
"""
Quick Fix Script for Customizations.xml
This script fixes the malformed XML issue without needing to download the repository again.

Run this in the root directory of your downloaded ContinousPerformanceManagementApp folder.
"""

import re
import sys
from pathlib import Path

def find_customizations_xml():
    """Find the Customizations.xml file"""
    possible_paths = [
        Path("solution/Other/Customizations.xml"),
        Path("./solution/Other/Customizations.xml"),
        Path("../solution/Other/Customizations.xml"),
    ]

    for path in possible_paths:
        if path.exists():
            return path

    # Try searching from current directory
    for xml_file in Path(".").rglob("Customizations.xml"):
        if "solution/Other" in str(xml_file):
            return xml_file

    return None

def fix_malformed_xml(content):
    """Fix the malformed CanModifyAdditionalSettings elements"""

    fixes_applied = 0

    # Fix 1: Malformed CanModifyAdditionalSettings (CRITICAL FIX)
    # Pattern: <CanModifyAdditionalSettings>1      <SourceType>
    # Should be: <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>\n      <SourceType>
    pattern = r'(<CanModifyAdditionalSettings>)(1)(\s+<SourceType>)'
    replacement = r'\g<1>\g<2></CanModifyAdditionalSettings>\n      <SourceType>'
    content, count = re.subn(pattern, replacement, content)
    fixes_applied += count
    print(f"   ✓ Fixed {count} malformed <CanModifyAdditionalSettings> elements")

    # Fix 1b: Remove orphaned closing tags created by Fix 1
    # The previous fix adds closing tags but original orphaned ones remain
    pattern = r'\n      </CanModifyAdditionalSettings>\n'
    content, count = re.subn(pattern, '\n', content)
    if count > 0:
        fixes_applied += count
        print(f"   ✓ Removed {count} orphaned </CanModifyAdditionalSettings> tags")

    # Fix 2: XML declaration (single quotes -> double quotes)
    if "<?xml version='1.0' encoding='utf-8'?>" in content:
        content = content.replace(
            "<?xml version='1.0' encoding='utf-8'?>",
            '<?xml version="1.0" encoding="utf-8"?>'
        )
        fixes_applied += 1
        print(f"   ✓ Fixed XML declaration quotes")

    # Fix 3: AutoNumberFormat self-closing tags -> explicit tags
    pattern = r'<AutoNumberFormat />'
    replacement = r'<AutoNumberFormat></AutoNumberFormat>'
    content, count = re.subn(pattern, replacement, content)
    if count > 0:
        fixes_applied += count
        print(f"   ✓ Fixed {count} AutoNumberFormat tags")

    # Fix 4: Remove IsPrimaryId attributes (pac CLI artifacts)
    pattern = r'\s+IsPrimaryId="(true|false)"'
    content, count = re.subn(pattern, '', content)
    if count > 0:
        fixes_applied += count
        print(f"   ✓ Removed {count} IsPrimaryId attributes")

    # Fix 5: Remove IsPrimaryName attributes (pac CLI artifacts)
    pattern = r'\s+IsPrimaryName="(true|false)"'
    content, count = re.subn(pattern, '', content)
    if count > 0:
        fixes_applied += count
        print(f"   ✓ Removed {count} IsPrimaryName attributes")

    return content, fixes_applied

def main():
    print("=" * 70)
    print("Quick Fix for Dataverse Customizations.xml")
    print("=" * 70)
    print()

    # Find the file
    print("Searching for Customizations.xml...")
    xml_path = find_customizations_xml()

    if not xml_path:
        print("❌ ERROR: Could not find solution/Other/Customizations.xml")
        print()
        print("Make sure you run this script from the root directory of the")
        print("ContinousPerformanceManagementApp folder.")
        sys.exit(1)

    print(f"✓ Found: {xml_path}")
    print()

    # Backup the file
    backup_path = xml_path.with_suffix('.xml.backup')
    print(f"Creating backup: {backup_path}")

    with open(xml_path, 'r', encoding='utf-8-sig') as f:
        original_content = f.read()

    with open(backup_path, 'w', encoding='utf-8-sig') as f:
        f.write(original_content)

    original_size = len(original_content)
    print(f"✓ Backup created ({original_size:,} bytes)")
    print()

    # Apply fixes
    print("Applying fixes...")
    fixed_content, fixes_applied = fix_malformed_xml(original_content)

    if fixes_applied == 0:
        print()
        print("✓ No fixes needed - file appears to be already fixed!")
        print("  This might mean you already have the latest version.")
        return

    # Write the fixed content
    print()
    print("Writing fixed content...")
    with open(xml_path, 'w', encoding='utf-8-sig') as f:
        f.write(fixed_content)

    new_size = len(fixed_content)
    print(f"✓ File updated ({new_size:,} bytes)")
    print()

    print("=" * 70)
    print(f"SUCCESS! Applied {fixes_applied} fixes")
    print("=" * 70)
    print()
    print("The critical malformed XML issue has been fixed.")
    print()
    print("Next steps:")
    print("  1. Run: deployment\\pack-solution.ps1")
    print("     (Should now complete without errors)")
    print()
    print("  2. Import the generated PerformanceManagement_1_0_0_0.zip")
    print("     into Teams Dataverse")
    print()
    print(f"Note: Original file backed up to: {backup_path}")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
