#!/usr/bin/env python3
"""
Fix Orphaned Closing Tags in Customizations.xml

The fix_malformed_xml.py script added closing tags but didn't remove
the original orphaned closing tags, creating duplicate closing tags.

This script removes the orphaned standalone closing tags.
"""

import re
from pathlib import Path

def main():
    print("=" * 70)
    print("Fix Orphaned </CanModifyAdditionalSettings> Closing Tags")
    print("=" * 70)
    print()

    customizations_xml = Path("solution/Other/Customizations.xml")

    if not customizations_xml.exists():
        print(f"❌ ERROR: {customizations_xml} not found!")
        return 1

    # Read the file
    print(f"Reading {customizations_xml}...")
    with open(customizations_xml, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    original_size = len(content)
    print(f"Original size: {original_size:,} bytes")
    print()

    # Backup
    backup_path = customizations_xml.with_suffix('.xml.backup2')
    print(f"Creating backup: {backup_path}")
    with open(backup_path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("✓ Backup created")
    print()

    # Fix: Remove orphaned closing tags
    # These are standalone </CanModifyAdditionalSettings> tags that appear
    # AFTER we've already added the proper closing tag
    print("Removing orphaned closing tags...")

    # Pattern: Find lines that are JUST the closing tag with leading whitespace
    # But NOT part of the self-closing pattern we want to keep
    pattern = r'\n      </CanModifyAdditionalSettings>\n'
    content, count = re.subn(pattern, '\n', content)

    print(f"   ✓ Removed {count} orphaned </CanModifyAdditionalSettings> tags")
    print()

    # Write the fixed content
    print("Writing fixed content...")
    with open(customizations_xml, 'w', encoding='utf-8-sig') as f:
        f.write(content)

    new_size = len(content)
    print(f"✓ File updated ({new_size:,} bytes)")
    print()

    print("=" * 70)
    print(f"✅ SUCCESS! Removed {count} orphaned closing tags")
    print("=" * 70)
    print()
    print("The XML should now be well-formed.")
    print("Verify with: xmllint --noout solution/Other/Customizations.xml")
    print()

if __name__ == "__main__":
    import sys
    try:
        sys.exit(main() or 0)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
