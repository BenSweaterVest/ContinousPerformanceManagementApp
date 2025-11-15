#!/usr/bin/env python3
"""
Fix Remaining Teams-Specific Issues

1. Add IsAuditEnabled="0" to all attributes that don't have it (Teams doesn't support AsyncOperation)
2. Fix entity-level IntroducedVersion from "1.0.0.0" to "1.0"
"""

import re
from pathlib import Path
import sys

def add_missing_audit_to_attributes(content: str) -> tuple[str, int]:
    """Add IsAuditEnabled=0 to any attribute missing it"""

    # Find all attributes and check if they have IsAuditEnabled
    pattern = r'(<attribute[^>]*>)(.*?)(</attribute>)'

    count = 0

    def check_and_add_audit(match):
        nonlocal count
        attr_start = match.group(1)
        attr_content = match.group(2)
        attr_end = match.group(3)

        # Check if IsAuditEnabled already exists
        if '<IsAuditEnabled>' in attr_content:
            return match.group(0)  # Already has it

        # Find a good place to insert it - after IsCustomizable or IsRenameable
        # Try to insert after IsCustomizable
        if '<IsCustomizable>' in attr_content:
            attr_content = re.sub(
                r'(<IsCustomizable>.*?</IsCustomizable>)',
                r'\1\n      <IsAuditEnabled>0</IsAuditEnabled>',
                attr_content,
                count=1
            )
            count += 1
        # Try to insert after IsRenameable
        elif '<IsRenameable>' in attr_content:
            attr_content = re.sub(
                r'(<IsRenameable>.*?</IsRenameable>)',
                r'\1\n      <IsAuditEnabled>0</IsAuditEnabled>',
                attr_content,
                count=1
            )
            count += 1
        # Try to insert after IntroducedVersion
        elif '<IntroducedVersion>' in attr_content:
            attr_content = re.sub(
                r'(<IntroducedVersion>.*?</IntroducedVersion>)',
                r'\1\n      <IsAuditEnabled>0</IsAuditEnabled>',
                attr_content,
                count=1
            )
            count += 1
        # Last resort: insert before displaynames
        elif '<displaynames>' in attr_content:
            attr_content = re.sub(
                r'(<displaynames>)',
                r'<IsAuditEnabled>0</IsAuditEnabled>\n      \1',
                attr_content,
                count=1
            )
            count += 1
        else:
            # Can't find a good spot, skip
            pass

        return attr_start + attr_content + attr_end

    new_content = re.sub(pattern, check_and_add_audit, content, flags=re.DOTALL)

    return new_content, count

def fix_entity_introduced_version(content: str) -> tuple[str, int]:
    """Fix entity-level IntroducedVersion from 1.0.0.0 to 1.0"""

    pattern = r'(<entity[^>]*IntroducedVersion=")1\.0\.0\.0(")'
    count = len(re.findall(pattern, content))

    if count > 0:
        content = re.sub(pattern, r'\g<1>1.0\2', content)

    return content, count

def main():
    print("🔧 Fixing remaining Teams-specific issues...\n")

    project_root = Path(__file__).parent.parent
    customizations_file = project_root / "solution" / "Other" / "Customizations.xml"

    if not customizations_file.exists():
        print(f"❌ ERROR: {customizations_file} not found")
        return 1

    print(f"📖 Reading: {customizations_file}")
    with open(customizations_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_size = len(content)

    # Step 1: Add missing IsAuditEnabled to attributes
    print("\n🔍 Step 1: Adding IsAuditEnabled=0 to attributes missing it...")
    content, audit_count = add_missing_audit_to_attributes(content)
    if audit_count > 0:
        print(f"   ✓ Added IsAuditEnabled=0 to {audit_count} attributes")
    else:
        print("   ℹ️  All attributes already have IsAuditEnabled")

    # Step 2: Fix entity-level IntroducedVersion
    print("\n🔍 Step 2: Fixing entity-level IntroducedVersion...")
    content, version_count = fix_entity_introduced_version(content)
    if version_count > 0:
        print(f"   ✓ Fixed IntroducedVersion on {version_count} entities: '1.0.0.0' → '1.0'")
    else:
        print("   ℹ️  All entities already have correct IntroducedVersion")

    # Write updated file
    with open(customizations_file, 'w', encoding='utf-8') as f:
        f.write(content)

    new_size = len(content)
    size_diff = new_size - original_size
    size_change = f"+{size_diff}" if size_diff > 0 else str(size_diff)

    print(f"\n✅ Teams-specific issues fixed!")
    print(f"   • File: {customizations_file}")
    print(f"   • Original size: {original_size:,} bytes")
    print(f"   • New size: {new_size:,} bytes ({size_change} bytes)")
    print(f"   • Attributes with IsAuditEnabled added: {audit_count}")
    print(f"   • Entities with IntroducedVersion fixed: {version_count}")

    # Verify counts
    print("\n📊 Verification:")
    total_attrs = len(re.findall(r'<attribute ', content))
    total_audit = len(re.findall(r'<IsAuditEnabled>', content))
    print(f"   • Total attributes: {total_attrs}")
    print(f"   • Attributes with IsAuditEnabled: {total_audit}")

    if total_attrs == total_audit:
        print("   ✅ All attributes now have IsAuditEnabled!")
    else:
        print(f"   ⚠️  Still missing {total_attrs - total_audit} IsAuditEnabled settings")

    # Check entity IntroducedVersion
    entity_version_10 = len(re.findall(r'<entity[^>]*IntroducedVersion="1\.0"', content))
    entity_version_1000 = len(re.findall(r'<entity[^>]*IntroducedVersion="1\.0\.0\.0"', content))
    print(f"   • Entities with IntroducedVersion='1.0': {entity_version_10}")
    print(f"   • Entities with IntroducedVersion='1.0.0.0': {entity_version_1000}")

    if entity_version_1000 == 0:
        print("   ✅ All entities now have correct IntroducedVersion!")

    print("\n📌 Next steps:")
    print("   1. Rebuild the solution package")
    print("   2. Test import into Dataverse for Teams")
    print("   3. Verify no AsyncOperation errors")

    return 0

if __name__ == "__main__":
    sys.exit(main())
