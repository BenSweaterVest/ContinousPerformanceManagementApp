#!/usr/bin/env python3
"""
Disable Audit for Dataverse for Teams

Dataverse for Teams doesn't support audit functionality which requires
the AsyncOperation entity. This script disables IsAuditEnabled on all
entities and attributes to allow import into Teams environments.

Based on error:
"Failed to create entity... at CreateAsyncOperationRelationship"
"""

import re
from pathlib import Path

def main():
    print("=" * 70)
    print("Disable Audit for Dataverse for Teams")
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
    backup_path = customizations_xml.with_suffix('.xml.backup_audit')
    print(f"Creating backup: {backup_path}")
    with open(backup_path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("✓ Backup created")
    print()

    # Fix entity-level audit settings
    print("Disabling audit on entities...")
    pattern = r'(<entity Name="[^"]+".+?IsAuditEnabled=")1(")'
    content, count = re.subn(pattern, r'\g<1>0\g<2>', content)
    print(f"   ✓ Disabled audit on {count} entities")

    # Fix attribute-level audit settings
    print("Disabling audit on attributes...")
    pattern = r'(<IsAuditEnabled>)1(</IsAuditEnabled>)'
    content, count = re.subn(pattern, r'\g<1>0\g<2>', content)
    print(f"   ✓ Disabled audit on {count} attributes")

    print()

    # Write the fixed content
    print("Writing updated content...")
    with open(customizations_xml, 'w', encoding='utf-8-sig') as f:
        f.write(content)

    new_size = len(content)
    print(f"✓ File updated ({new_size:,} bytes)")
    print()

    print("=" * 70)
    print("✅ SUCCESS! Audit disabled for Teams compatibility")
    print("=" * 70)
    print()
    print("Audit functionality requires AsyncOperation entity which is not")
    print("available in Dataverse for Teams. The solution should now import")
    print("successfully into Teams environments.")
    print()
    print("Note: This change only affects audit logging. All other functionality")
    print("remains intact.")
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
