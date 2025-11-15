#!/usr/bin/env python3
"""
Fix IntroducedVersion for system fields to use "1.0" instead of "1.0.0.0".

Microsoft's pattern:
- System fields (createdby, modifiedby, ownerid, etc.): "1.0"
- Custom fields: "1.0.0.0"

Currently we use "1.0.0.0" for almost everything except system relationships.
"""

from pathlib import Path
import re

# System fields that should have IntroducedVersion="1.0"
SYSTEM_FIELDS = [
    "createdby",
    "createdon",
    "createdonbehalfby",
    "modifiedby",
    "modifiedon",
    "modifiedonbehalfby",
    "ownerid",
    "owningbusinessunit",
    "owningteam",
    "owninguser",
    "statecode",
    "statuscode",
    "importsequencenumber",
    "overriddencreatedon",
    "versionnumber",
    "timezoneruleversionnumber",
    "utcconversiontimezonecode",
]

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

    print(f"\n🔧 Fixing IntroducedVersion for system fields...")

    # For each system field, find its IntroducedVersion and change it to "1.0"
    for field_name in SYSTEM_FIELDS:
        # Pattern: Find attributes with this logical name that have IntroducedVersion 1.0.0.0
        # We need to be careful to only match within attribute blocks

        # Find all occurrences of this field
        pattern = f'<LogicalName>{field_name}</LogicalName>.*?<IntroducedVersion>1\\.0\\.0\\.0</IntroducedVersion>'

        # Count matches first
        matches = list(re.finditer(pattern, content, re.DOTALL))
        if matches:
            # Replace within each match
            for match in reversed(matches):  # Reverse to maintain positions
                start, end = match.span()
                old_text = match.group(0)
                new_text = old_text.replace('<IntroducedVersion>1.0.0.0</IntroducedVersion>',
                                           '<IntroducedVersion>1.0</IntroducedVersion>')
                content = content[:start] + new_text + content[end:]
                total_replacements += 1

            print(f"   • {field_name:30} → Changed {len(matches)} occurrences to 1.0")

    if total_replacements == 0:
        print("\n⚠️  No changes made - IntroducedVersion may already be correct")
        return 0

    # Write back
    print(f"\n💾 Writing updated Customizations.xml...")
    with open(customizations_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Success!")
    print(f"   • Total replacements: {total_replacements}")
    print(f"   • File size: {len(original_content):,} → {len(content):,} bytes")

    # Verify counts
    count_1_0 = content.count('<IntroducedVersion>1.0</IntroducedVersion>')
    count_1_0_0_0 = content.count('<IntroducedVersion>1.0.0.0</IntroducedVersion>')

    print(f"\n📊 IntroducedVersion distribution:")
    print(f"   • 1.0:       {count_1_0:4} occurrences (system fields + system relationships)")
    print(f"   • 1.0.0.0:   {count_1_0_0_0:4} occurrences (custom fields + entities)")

    return 0


if __name__ == "__main__":
    exit(main())
