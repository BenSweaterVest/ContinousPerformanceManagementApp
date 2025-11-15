#!/usr/bin/env python3
"""
Fix entity name casing to use PascalCase like Microsoft's solutions.

Microsoft uses PascalCase for entity names in Customizations.xml:
- <Name>msft_Board</Name> (not msft_board)
- <entity Name="msft_Board"> (not msft_board)
- <ReferencingEntityName>msft_Board</ReferencingEntityName> (not msft_board)

But Solution.xml uses lowercase:
- schemaName="msft_board" (lowercase - this is correct in our file)

This script updates Customizations.xml to use PascalCase everywhere.
"""

from pathlib import Path
import re

# Mapping of lowercase to PascalCase
ENTITY_NAME_MAPPING = {
    "pm_staffmember": "pm_StaffMember",
    "pm_evaluationquestion": "pm_EvaluationQuestion",
    "pm_weeklyevaluation": "pm_WeeklyEvaluation",
    "pm_selfevaluation": "pm_SelfEvaluation",
    "pm_idpentry": "pm_IDPEntry",
    "pm_meetingnote": "pm_MeetingNote",
    "pm_goal": "pm_Goal",
    "pm_recognition": "pm_Recognition",
    "pm_actionitem": "pm_ActionItem",
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

    print(f"\n🔧 Fixing entity name casing...")

    for lowercase_name, pascalcase_name in ENTITY_NAME_MAPPING.items():
        # Count how many times this entity appears
        count = 0

        # 1. Fix <Name> element content
        pattern1 = f'<Name LocalizedName="[^"]*" OriginalName="[^"]*">{lowercase_name}</Name>'
        replacement1 = lambda m: m.group(0).replace(f'>{lowercase_name}<', f'>{pascalcase_name}<')
        content, n1 = re.subn(pattern1, replacement1, content)
        count += n1

        # 2. Fix <entity Name="..."> attribute
        pattern2 = f'<entity Name="{lowercase_name}"'
        replacement2 = f'<entity Name="{pascalcase_name}"'
        content = content.replace(pattern2, replacement2)
        n2 = original_content.count(pattern2)
        count += n2

        # 3. Fix <ReferencingEntityName> in relationships
        pattern3 = f'<ReferencingEntityName>{lowercase_name}</ReferencingEntityName>'
        replacement3 = f'<ReferencingEntityName>{pascalcase_name}</ReferencingEntityName>'
        content = content.replace(pattern3, replacement3)
        n3 = original_content.count(pattern3)
        count += n3

        # 4. Fix <ReferencedEntityName> (for our custom-to-custom relationships)
        pattern4 = f'<ReferencedEntityName>{lowercase_name}</ReferencedEntityName>'
        replacement4 = f'<ReferencedEntityName>{pascalcase_name}</ReferencedEntityName>'
        content = content.replace(pattern4, replacement4)
        n4 = original_content.count(pattern4)
        count += n4

        if count > 0:
            print(f"   • {lowercase_name:30} → {pascalcase_name:30} ({count:3} replacements)")
            total_replacements += count

    if content == original_content:
        print("\n⚠️  No changes made - entity names may already be correct")
        return 0

    # Write back
    print(f"\n💾 Writing updated Customizations.xml...")
    with open(customizations_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Success!")
    print(f"   • Total replacements: {total_replacements}")
    print(f"   • File size: {len(original_content):,} → {len(content):,} bytes")

    # Verify the changes
    print(f"\n🔍 Verification:")
    for lowercase_name in ENTITY_NAME_MAPPING.keys():
        if f'>{lowercase_name}<' in content or f'"{lowercase_name}"' in content or f'>{lowercase_name}</' in content:
            print(f"   ⚠️  WARNING: '{lowercase_name}' still appears in the file!")

    print(f"\n✅ All entity names updated to PascalCase!")

    return 0


if __name__ == "__main__":
    exit(main())
