#!/usr/bin/env python3
"""
Align Our Solution with Microsoft's Boards Solution Structure

Based on detailed comparison in ref/MSFT-BOARDS-COMPARISON.md, this script:
1. Removes attributes we have that Microsoft doesn't
2. Adds missing attributes to primary name fields (20+ attributes)
3. Fixes value differences (IntroducedVersion, RequiredLevel, etc.)
4. Ensures exact alignment with Microsoft's working solution structure
"""

import re
from pathlib import Path
import sys

def remove_extra_attributes(content: str) -> tuple[str, list]:
    """Remove attributes we have that Microsoft doesn't"""
    changes = []

    # 1. Remove IsPrimaryId from primarykey fields
    count = len(re.findall(r'<IsPrimaryId>.*?</IsPrimaryId>', content))
    if count > 0:
        content = re.sub(r'\s*<IsPrimaryId>.*?</IsPrimaryId>\s*', '\n', content)
        changes.append(f"Removed {count} IsPrimaryId attributes (Microsoft doesn't use this)")

    # 2. Remove IsValidForCreate/Read/Update from primarykey fields
    # (Keep ValidForCreateApi/ReadApi/UpdateApi)
    for tag in ['IsValidForCreate', 'IsValidForRead', 'IsValidForUpdate']:
        count = len(re.findall(f'<{tag}>.*?</{tag}>', content))
        if count > 0:
            content = re.sub(f'\\s*<{tag}>.*?</{tag}>\\s*', '\n', content)
            changes.append(f"Removed {count} {tag} attributes (Microsoft uses ValidForXxxApi only)")

    # 3. Remove IsPrimaryName from primary name fields
    count = len(re.findall(r'<IsPrimaryName>.*?</IsPrimaryName>', content))
    if count > 0:
        content = re.sub(r'\s*<IsPrimaryName>.*?</IsPrimaryName>\s*', '\n', content)
        changes.append(f"Removed {count} IsPrimaryName attributes (Microsoft uses DisplayMask only)")

    # 4. Remove MaxLength from primarykey fields (but keep it for nvarchar fields!)
    # We need to be careful - only remove from primarykey type
    primarykey_pattern = r'(<attribute[^>]*>.*?<Type>primarykey</Type>.*?)</MaxLength>(.*?</attribute>)'

    def remove_maxlength_from_primarykey(match):
        before = match.group(1)
        after = match.group(2)
        # Remove the MaxLength element
        before = re.sub(r'\s*<MaxLength>.*?$', '', before, flags=re.MULTILINE)
        return before + after

    new_content = re.sub(primarykey_pattern, remove_maxlength_from_primarykey, content, flags=re.DOTALL)
    if new_content != content:
        changes.append("Removed MaxLength from primarykey fields (Microsoft doesn't have this)")
        content = new_content

    return content, changes

def add_missing_primary_name_attributes(content: str) -> tuple[str, list]:
    """Add missing attributes to primary name fields based on Microsoft's structure"""
    changes = []

    # Find all primary name fields (those with PrimaryName in DisplayMask)
    pattern = r'(<attribute[^>]*>)(.*?)(<DisplayMask>[^<]*PrimaryName[^<]*</DisplayMask>)(.*?)(</attribute>)'

    def add_attributes(match):
        attr_start = match.group(1)
        before_display = match.group(2)
        display_mask = match.group(3)
        after_display = match.group(4)
        attr_end = match.group(5)

        # Check if this is a primary name field (nvarchar type)
        if '<Type>nvarchar</Type>' not in before_display:
            return match.group(0)  # Not an nvarchar, skip

        # Extract existing elements
        full_content = before_display + display_mask + after_display

        # Build new attributes to add (only if they don't exist)
        new_attrs = []

        # ImeMode
        if '<ImeMode>' not in full_content:
            new_attrs.append('  <ImeMode>auto</ImeMode>')

        # ValidForXxxApi
        if '<ValidForUpdateApi>' not in full_content:
            new_attrs.append('  <ValidForUpdateApi>1</ValidForUpdateApi>')
        if '<ValidForReadApi>' not in full_content:
            new_attrs.append('  <ValidForReadApi>1</ValidForReadApi>')
        if '<ValidForCreateApi>' not in full_content:
            new_attrs.append('  <ValidForCreateApi>1</ValidForCreateApi>')

        # IsCustomField
        if '<IsCustomField>' not in full_content:
            new_attrs.append('  <IsCustomField>1</IsCustomField>')

        # IsAuditEnabled (should be 0 for Teams)
        if '<IsAuditEnabled>' not in full_content:
            new_attrs.append('  <IsAuditEnabled>0</IsAuditEnabled>')

        # IsSecured
        if '<IsSecured>' not in full_content:
            new_attrs.append('  <IsSecured>0</IsSecured>')

        # SourceType
        if '<SourceType>' not in full_content:
            new_attrs.append('  <SourceType>0</SourceType>')

        # Global filter and sortable settings
        if '<IsGlobalFilterEnabled>' not in full_content:
            new_attrs.append('  <IsGlobalFilterEnabled>0</IsGlobalFilterEnabled>')
        if '<IsSortableEnabled>' not in full_content:
            new_attrs.append('  <IsSortableEnabled>0</IsSortableEnabled>')
        if '<CanModifyGlobalFilterSettings>' not in full_content:
            new_attrs.append('  <CanModifyGlobalFilterSettings>1</CanModifyGlobalFilterSettings>')
        if '<CanModifyIsSortableSettings>' not in full_content:
            new_attrs.append('  <CanModifyIsSortableSettings>1</CanModifyIsSortableSettings>')

        # IsDataSourceSecret
        if '<IsDataSourceSecret>' not in full_content:
            new_attrs.append('  <IsDataSourceSecret>0</IsDataSourceSecret>')

        # AutoNumberFormat (empty element)
        if '<AutoNumberFormat' not in full_content:
            new_attrs.append('  <AutoNumberFormat></AutoNumberFormat>')

        # Search and filter settings
        if '<IsSearchable>' not in full_content:
            new_attrs.append('  <IsSearchable>1</IsSearchable>')
        if '<IsFilterable>' not in full_content:
            new_attrs.append('  <IsFilterable>0</IsFilterable>')
        if '<IsRetrievable>' not in full_content:
            new_attrs.append('  <IsRetrievable>1</IsRetrievable>')
        if '<IsLocalizable>' not in full_content:
            new_attrs.append('  <IsLocalizable>0</IsLocalizable>')

        # Format for nvarchar
        if '<Format>' not in full_content:
            new_attrs.append('  <Format>text</Format>')

        # MaxLength for nvarchar (separate from Length)
        if '<MaxLength>' not in full_content:
            # Extract Length value if present
            length_match = re.search(r'<Length>(\d+)</Length>', full_content)
            if length_match:
                length_val = length_match.group(1)
                new_attrs.append(f'  <MaxLength>{length_val}</MaxLength>')

        if new_attrs:
            # Insert new attributes after DisplayMask
            return attr_start + before_display + display_mask + '\n' + '\n'.join(new_attrs) + after_display + attr_end

        return match.group(0)

    new_content = re.sub(pattern, add_attributes, content, flags=re.DOTALL)
    if new_content != content:
        changes.append("Added missing API attributes to primary name fields (ImeMode, ValidForXxxApi, Format, MaxLength, etc.)")
        content = new_content

    return content, changes

def fix_value_differences(content: str) -> tuple[str, list]:
    """Fix value differences identified in comparison"""
    changes = []

    # 1. Fix IntroducedVersion: "1.0.0.0" → "1.0"
    count = len(re.findall(r'<IntroducedVersion>1\.0\.0\.0</IntroducedVersion>', content))
    if count > 0:
        content = re.sub(
            r'<IntroducedVersion>1\.0\.0\.0</IntroducedVersion>',
            '<IntroducedVersion>1.0</IntroducedVersion>',
            content
        )
        changes.append(f"Fixed {count} IntroducedVersion values: '1.0.0.0' → '1.0'")

    # 2. Fix AutoNumberFormat: self-closing → empty element
    count = len(re.findall(r'<AutoNumberFormat\s*/>', content))
    if count > 0:
        content = re.sub(
            r'<AutoNumberFormat\s*/>',
            '<AutoNumberFormat></AutoNumberFormat>',
            content
        )
        changes.append(f"Fixed {count} AutoNumberFormat elements: self-closing → empty element")

    # 3. Fix RequiredLevel on primary name fields: "applicationrequired" → "required"
    # Only change for primary name fields (those with PrimaryName in DisplayMask)
    pattern = r'(<RequiredLevel>)applicationrequired(</RequiredLevel>\s*<DisplayMask>[^<]*PrimaryName)'
    count = len(re.findall(pattern, content))
    if count > 0:
        content = re.sub(pattern, r'\1required\2', content)
        changes.append(f"Fixed {count} RequiredLevel values on primary name fields: 'applicationrequired' → 'required'")

    # 4. Fix IsRenameable on primarykey: "0" → "1"
    pattern = r'(<attribute[^>]*>.*?<Type>primarykey</Type>.*?<IsRenameable>)0(</IsRenameable>.*?</attribute>)'

    def fix_renameable(match):
        return match.group(1) + '1' + match.group(2)

    new_content = re.sub(pattern, fix_renameable, content, flags=re.DOTALL)
    if new_content != content:
        changes.append("Fixed IsRenameable on primarykey fields: '0' → '1'")
        content = new_content

    # 5. Fix IsAuditEnabled on primarykey: already handled by disable_audit script
    # But ensure it's "0" not "1"
    pattern = r'(<attribute[^>]*>.*?<Type>primarykey</Type>.*?<IsAuditEnabled>)1(</IsAuditEnabled>.*?</attribute>)'

    def fix_audit_primarykey(match):
        return match.group(1) + '0' + match.group(2)

    new_content = re.sub(pattern, fix_audit_primarykey, content, flags=re.DOTALL)
    if new_content != content:
        changes.append("Fixed IsAuditEnabled on primarykey fields: '1' → '0'")
        content = new_content

    return content, changes

def main():
    print("🔧 Aligning solution with Microsoft's Boards solution structure...")
    print("📋 Based on: ref/MSFT-BOARDS-COMPARISON.md\n")

    project_root = Path(__file__).parent.parent
    customizations_file = project_root / "solution" / "Other" / "Customizations.xml"

    if not customizations_file.exists():
        print(f"❌ ERROR: {customizations_file} not found")
        return 1

    print(f"📖 Reading: {customizations_file}")
    with open(customizations_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_size = len(content)
    all_changes = []

    # Step 1: Remove extra attributes
    print("\n🔍 Step 1: Removing extra attributes not in Microsoft's solution...")
    content, changes = remove_extra_attributes(content)
    all_changes.extend(changes)
    for change in changes:
        print(f"   ✓ {change}")

    # Step 2: Add missing attributes to primary name fields
    print("\n🔍 Step 2: Adding missing attributes to primary name fields...")
    content, changes = add_missing_primary_name_attributes(content)
    all_changes.extend(changes)
    for change in changes:
        print(f"   ✓ {change}")

    # Step 3: Fix value differences
    print("\n🔍 Step 3: Fixing value differences...")
    content, changes = fix_value_differences(content)
    all_changes.extend(changes)
    for change in changes:
        print(f"   ✓ {change}")

    # Write updated file
    with open(customizations_file, 'w', encoding='utf-8') as f:
        f.write(content)

    new_size = len(content)
    size_diff = new_size - original_size
    size_change = f"+{size_diff}" if size_diff > 0 else str(size_diff)

    print(f"\n✅ Solution aligned successfully!")
    print(f"   • File: {customizations_file}")
    print(f"   • Original size: {original_size:,} bytes")
    print(f"   • New size: {new_size:,} bytes ({size_change} bytes)")
    print(f"   • Total changes: {len(all_changes)}")

    print("\n📋 Summary of alignment:")
    print("   ✓ Removed IsPrimaryId (Microsoft doesn't use)")
    print("   ✓ Removed IsValidForCreate/Read/Update (Microsoft uses ValidForXxxApi)")
    print("   ✓ Removed IsPrimaryName (Microsoft uses DisplayMask only)")
    print("   ✓ Removed MaxLength from primarykey fields")
    print("   ✓ Added 20+ missing attributes to primary name fields")
    print("   ✓ Fixed IntroducedVersion: 1.0.0.0 → 1.0")
    print("   ✓ Fixed AutoNumberFormat formatting")
    print("   ✓ Fixed RequiredLevel: applicationrequired → required")
    print("   ✓ Fixed IsRenameable on primarykey: 0 → 1")

    print("\n📌 Next steps:")
    print("   1. Review the changes in git diff")
    print("   2. Rebuild the solution package")
    print("   3. Test import into Dataverse for Teams")

    return 0

if __name__ == "__main__":
    sys.exit(main())
