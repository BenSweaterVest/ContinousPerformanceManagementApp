#!/usr/bin/env python3
"""
Final alignment fixes to match Microsoft Boards structure exactly.

Fixes based on comprehensive deep analysis:
1. XML declaration quotes (single -> double)
2. AutoNumberFormat style (self-closing -> explicit tags)
3. Remove IsPrimaryId attributes (not in Microsoft's format)
4. Remove IsPrimaryName attributes (not in Microsoft's format)
5. Fix IntroducedVersion for primary key fields (1.0.0.0 -> 1.0)
6. Remove IsValidForCreate/Read/Update from system fields (use ValidFor*Api only)
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
    changes = {}

    # 1. Fix XML declaration quotes
    print(f"\n🔧 Fixing XML declaration...")
    old_decl = "<?xml version='1.0' encoding='utf-8'?>"
    new_decl = '<?xml version="1.0" encoding="utf-8"?>'
    if old_decl in content:
        content = content.replace(old_decl, new_decl)
        changes['XML declaration quotes'] = 1
        print(f"   • Changed single quotes to double quotes")

    # 2. Fix AutoNumberFormat style (self-closing -> explicit tags)
    print(f"\n🔧 Fixing AutoNumberFormat format...")
    pattern = r'<AutoNumberFormat />'
    replacement = r'<AutoNumberFormat></AutoNumberFormat>'
    content, count = re.subn(pattern, replacement, content)
    if count > 0:
        changes['AutoNumberFormat style'] = count
        print(f"   • Changed {count} self-closing tags to explicit open/close")

    # 3. Remove IsPrimaryId attributes
    print(f"\n🔧 Removing IsPrimaryId attributes...")
    pattern = r'\s*<IsPrimaryId>1</IsPrimaryId>\s*\n'
    content, count = re.subn(pattern, '\n', content)
    if count > 0:
        changes['IsPrimaryId removed'] = count
        print(f"   • Removed {count} IsPrimaryId attributes")

    # 4. Remove IsPrimaryName attributes
    print(f"\n🔧 Removing IsPrimaryName attributes...")
    pattern = r'\s*<IsPrimaryName>1</IsPrimaryName>\s*\n'
    content, count = re.subn(pattern, '\n', content)
    if count > 0:
        changes['IsPrimaryName removed'] = count
        print(f"   • Removed {count} IsPrimaryName attributes")

    # 5. Fix IntroducedVersion for primary key fields (Type=primarykey + IsCustomField=0)
    print(f"\n🔧 Fixing IntroducedVersion for primary key fields...")
    # Find primary key attributes with IsCustomField=0 and IntroducedVersion=1.0.0.0
    pattern = r'(<Type>primarykey</Type>.*?<IsCustomField>0</IsCustomField>.*?)<IntroducedVersion>1\.0\.0\.0</IntroducedVersion>'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    if matches:
        for match in reversed(matches):
            start, end = match.span()
            old_text = match.group(0)
            new_text = match.group(1) + '<IntroducedVersion>1.0</IntroducedVersion>'
            content = content[:start] + new_text + content[end:]
        changes['Primary key IntroducedVersion'] = len(matches)
        print(f"   • Fixed {len(matches)} primary key field versions (1.0.0.0 → 1.0)")

    # 6. Remove IsValidForCreate/Read/Update from system fields
    # (These should only use ValidFor*Api)
    print(f"\n🔧 Removing duplicate IsValidFor* attributes from system fields...")

    # Pattern: Find attributes with both IsValidFor* AND ValidFor*Api
    # System fields have LogicalName in lowercase and IsCustomField=0
    system_field_pattern = r'(<attribute PhysicalName="[A-Z][^"]*">.*?<LogicalName>(?:createdby|createdon|createdonbehalfby|modifiedby|modifiedon|modifiedonbehalfby|ownerid|owningbusinessunit|owningteam|owninguser|statecode|statuscode|importsequencenumber|overriddencreatedon|versionnumber|timezoneruleversionnumber|utcconversiontimezonecode)</LogicalName>.*?)</attribute>'

    system_fields = list(re.finditer(system_field_pattern, content, re.DOTALL))
    removed_count = 0

    for field_match in reversed(system_fields):
        field_content = field_match.group(0)

        # Check if this field has both IsValidFor* and ValidFor*Api
        if 'IsValidForCreate' in field_content and 'ValidForCreateApi' in field_content:
            # Remove the IsValidFor* versions
            field_content = re.sub(r'\s*<IsValidForCreate>[01]</IsValidForCreate>\s*\n', '\n', field_content)
            field_content = re.sub(r'\s*<IsValidForRead>[01]</IsValidForRead>\s*\n', '\n', field_content)
            field_content = re.sub(r'\s*<IsValidForUpdate>[01]</IsValidForUpdate>\s*\n', '\n', field_content)

            start, end = field_match.span()
            content = content[:start] + field_content + content[end:]
            removed_count += 1

    if removed_count > 0:
        changes['System field IsValidFor* removed'] = removed_count
        print(f"   • Removed duplicate IsValidFor* from {removed_count} system fields")

    if not changes:
        print("\n⚠️  No changes made - file may already be aligned")
        return 0

    # Write back
    print(f"\n💾 Writing updated Customizations.xml...")
    with open(customizations_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Success!")
    print(f"   • File size: {len(original_content):,} → {len(content):,} bytes ({len(content) - len(original_content):+,})")
    print(f"\n📊 Changes made:")
    for change_type, count in changes.items():
        print(f"   • {change_type}: {count}")

    return 0


if __name__ == "__main__":
    exit(main())
