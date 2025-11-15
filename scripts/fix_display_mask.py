#!/usr/bin/env python3
"""
Fix DisplayMask values for system fields to match Microsoft's pattern.

Microsoft uses more complete DisplayMask values:
- System fields (createdby, etc.): "ValidForAdvancedFind|ValidForForm|ValidForGrid"
- We're using: "ValidForAdvancedFind" (too simple)

This affects UI visibility in forms, grids, and advanced find.
"""

from pathlib import Path
import re

# System fields and their proper DisplayMask values (from Microsoft Boards)
SYSTEM_FIELD_DISPLAY_MASKS = {
    "createdby": "ValidForAdvancedFind|ValidForForm|ValidForGrid",
    "createdon": "ValidForAdvancedFind|ValidForForm|ValidForGrid",
    "createdonbehalfby": "ValidForAdvancedFind|ValidForForm|ValidForGrid",
    "modifiedby": "ValidForAdvancedFind|ValidForForm|ValidForGrid",
    "modifiedon": "ValidForAdvancedFind|ValidForForm|ValidForGrid",
    "modifiedonbehalfby": "ValidForAdvancedFind|ValidForForm|ValidForGrid",
    "ownerid": "ValidForAdvancedFind|ValidForForm|ValidForGrid",
    "owningbusinessunit": "ValidForAdvancedFind",
    "owningteam": "ValidForAdvancedFind",
    "owninguser": "ValidForAdvancedFind|ValidForForm|ValidForGrid",
    "statecode": "ValidForAdvancedFind|ValidForForm|ValidForGrid",
    "statuscode": "ValidForAdvancedFind|ValidForForm|ValidForGrid",
    "importsequencenumber": "ValidForAdvancedFind",
    "overriddencreatedon": "ValidForAdvancedFind",
    "versionnumber": "ValidForAdvancedFind",
    "timezoneruleversionnumber": "ValidForAdvancedFind",
    "utcconversiontimezonecode": "ValidForAdvancedFind",
}

def main():
    customizations_path = Path("solution/Other/Customizations.xml")

    if not customizations_path.exists():
        print(f"❌ Error: {customizations_path} not found")
        return 1

    print(f"📖 Reading {customizations_path}...")
    with open(customizations_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    total_replacements = 0

    print(f"\n🔧 Fixing DisplayMask for system fields...")

    for field_name, correct_display_mask in SYSTEM_FIELD_DISPLAY_MASKS.items():
        # Find attributes with this logical name
        # Pattern: <LogicalName>field_name</LogicalName> ... <DisplayMask>current_value</DisplayMask>
        pattern = f'(<LogicalName>{field_name}</LogicalName>.*?)(<DisplayMask>)([^<]+)(</DisplayMask>)'

        matches = list(re.finditer(pattern, content, re.DOTALL))
        if matches:
            for match in reversed(matches):  # Reverse to maintain positions
                current_mask = match.group(3)
                if current_mask != correct_display_mask:
                    start, end = match.span()
                    old_text = match.group(0)
                    new_text = match.group(1) + match.group(2) + correct_display_mask + match.group(4)
                    content = content[:start] + new_text + content[end:]
                    total_replacements += 1

            if matches:
                changed = sum(1 for m in matches if m.group(3) != correct_display_mask)
                if changed > 0:
                    print(f"   • {field_name:30} → Changed {changed:2} occurrences")

    if total_replacements == 0:
        print("\n⚠️  No changes made - DisplayMask values may already be correct")
        return 0

    # Write back
    print(f"\n💾 Writing updated Customizations.xml...")
    with open(customizations_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Success!")
    print(f"   • Total replacements: {total_replacements}")
    print(f"   • File size: {len(original_content):,} → {len(content):,} bytes ({len(content) - len(original_content):+,})")

    return 0


if __name__ == "__main__":
    exit(main())
