#!/usr/bin/env python3
"""
Remove ALL lookup attributes that target systemuser entity.

systemuser entity doesn't exist in Dataverse for Teams.
Any lookup targeting it will cause AsyncOperation relationship errors.
"""

import re
from pathlib import Path

def find_systemuser_lookups(content: str) -> list:
    """Find all attributes that target systemuser."""

    # Pattern to find attribute blocks with systemuser targets
    pattern = r'<attribute PhysicalName="([^"]+)">.*?<Target>systemuser</Target>.*?</attribute>'

    matches = re.findall(pattern, content, re.DOTALL)
    return matches


def remove_systemuser_lookup_attributes(content: str) -> tuple[str, int, list]:
    """Remove all lookup attributes targeting systemuser."""

    # Find them first for reporting
    found_attrs = find_systemuser_lookups(content)

    # Pattern to match entire attribute block that contains systemuser target
    pattern = r'<attribute PhysicalName="[^"]+">.*?<Target>systemuser</Target>.*?</attribute>\s*\n'

    matches = re.findall(pattern, content, re.DOTALL)
    count = len(matches)

    if count > 0:
        new_content = re.sub(pattern, '', content, flags=re.DOTALL)
        return new_content, count, found_attrs

    return content, 0, found_attrs


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("REMOVING ALL SYSTEMUSER LOOKUP FIELDS")
    print("="*80 + "\n")

    # Paths
    solution_dir = Path(__file__).parent.parent / "solution"
    customizations_path = solution_dir / "Other" / "Customizations.xml"

    if not customizations_path.exists():
        print(f"❌ ERROR: File not found: {customizations_path}")
        return

    print(f"📂 Reading: {customizations_path}")
    with open(customizations_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_size = len(content)
    print(f"📊 Original size: {original_size:,} bytes\n")

    # Find systemuser lookups
    systemuser_attrs = find_systemuser_lookups(content)

    if systemuser_attrs:
        print(f"📋 Found {len(systemuser_attrs)} lookup attributes targeting systemuser:")
        for attr in systemuser_attrs:
            print(f"  • {attr}")
        print()
    else:
        print("✅ No systemuser lookup attributes found!\n")
        return

    # Remove them
    print("🔧 Removing systemuser lookup attributes...")
    content, attrs_removed, _ = remove_systemuser_lookup_attributes(content)
    print(f"  ✓ Removed {attrs_removed} attribute definitions")

    # Write back
    print(f"\n💾 Writing updated Customizations.xml...")
    with open(customizations_path, 'w', encoding='utf-8') as f:
        f.write(content)

    new_size = len(content)
    size_diff = new_size - original_size
    print(f"  ✓ Updated size: {new_size:,} bytes ({size_diff:+,} bytes)")

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\n✅ Removed {attrs_removed} systemuser lookup attributes:")
    for attr in systemuser_attrs:
        print(f"  • {attr}")

    print(f"\n📉 Size reduction: {-size_diff:,} bytes")

    print("\n💡 Rationale:")
    print("  systemuser entity doesn't exist in Dataverse for Teams")
    print("  All lookups to systemuser cause CreateAsyncOperationRelationship errors")
    print("  These fields can be re-added later as lookups to pm_staffmember")

    print("\n⚠️  NEXT STEPS:")
    print("  1. Run: python scripts/pack_solution.py")
    print("  2. Test import into Teams environment")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
