#!/usr/bin/env python3
"""
Fix CRITICAL malformed XML issue in CanModifyAdditionalSettings elements.

The add_missing_attribute_metadata.py script incorrectly inserted new elements
INSIDE the <CanModifyAdditionalSettings> tag instead of AFTER it.

This created:
    <CanModifyAdditionalSettings>1<SourceType>0</SourceType>...

Instead of:
    <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
    <SourceType>0</SourceType>...
"""

from pathlib import Path
import re

def main():
    customizations_path = Path("solution/Other/Customizations.xml")

    if not customizations_path.exists():
        print(f"❌ Error: {customizations_path} not found")
        return 1

    print(f"📖 Reading {customizations_path}...")
    with open(customizations_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    print(f"\n🔧 Fixing malformed XML in CanModifyAdditionalSettings...")

    # Pattern to find malformed elements
    # Looks for: <CanModifyAdditionalSettings>1      <SourceType>
    # Should be: <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>\n      <SourceType>

    pattern = r'(<CanModifyAdditionalSettings>)(1)(\s+<SourceType>)'
    replacement = r'\g<1>\g<2></CanModifyAdditionalSettings>\n      <SourceType>'

    content, count = re.subn(pattern, replacement, content)

    print(f"   • Fixed {count} malformed <CanModifyAdditionalSettings> elements")

    if count == 0:
        print("\n⚠️  No malformed XML found - file may already be correct")
        return 0

    # Write back
    print(f"\n💾 Writing corrected Customizations.xml...")
    with open(customizations_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Success!")
    print(f"   • Fixed {count} XML structure errors")
    print(f"   • File size: {len(original_content):,} → {len(content):,} bytes ({len(content) - len(original_content):+,})")

    # Verify the fix
    if '<CanModifyAdditionalSettings>1      <SourceType>' in content:
        print("\n❌ ERROR: Malformed XML still present!")
        return 1
    else:
        print("\n✅ Verification: No malformed XML detected")

    return 0


if __name__ == "__main__":
    exit(main())
