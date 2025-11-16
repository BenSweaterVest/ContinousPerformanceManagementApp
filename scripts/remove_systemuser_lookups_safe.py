#!/usr/bin/env python3
"""
Safely remove lookup attributes targeting systemuser by changing targets.

Instead of removing entire attributes, change systemuser targets to pm_staffmember.
"""

import re
from pathlib import Path

def replace_systemuser_with_staffmember(content: str) -> tuple[str, int]:
    """Replace <Target>systemuser</Target> with <Target>pm_staffmember</Target>."""

    pattern = r'<Target>systemuser</Target>'
    replacement = '<Target>pm_staffmember</Target>'

    count = len(re.findall(pattern, content))

    if count > 0:
        new_content = content.replace(pattern, replacement)
        return new_content, count

    return content, 0


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("REPLACING SYSTEMUSER TARGETS WITH PM_STAFFMEMBER")
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

    # Count current systemuser targets
    current_count = content.count('<Target>systemuser</Target>')
    print(f"📋 Found {current_count} <Target>systemuser</Target> references\n")

    if current_count == 0:
        print("✅ No systemuser targets found!\n")
        return

    # Show context of what we're changing
    print("🔍 Finding systemuser lookup attributes...")
    # Find attribute names that have systemuser targets
    pattern = r'<attribute PhysicalName="([^"]+)">(?:(?!<attribute).)*?<Target>systemuser</Target>'
    attrs_with_systemuser = re.findall(pattern, content, re.DOTALL)

    print(f"  Found in {len(attrs_with_systemuser)} attributes:")
    for attr in attrs_with_systemuser:
        print(f"    • {attr}")
    print()

    # Replace
    print("🔧 Replacing systemuser targets with pm_staffmember...")
    content, count = replace_systemuser_with_staffmember(content)
    print(f"  ✓ Replaced {count} targets")

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
    print(f"\n✅ Changed {count} lookup targets from systemuser to pm_staffmember")

    print("\n📝 Attributes affected:")
    for attr in attrs_with_systemuser:
        print(f"  • {attr}: Now references pm_staffmember instead of systemuser")

    print("\n💡 Rationale:")
    print("  systemuser entity doesn't exist in Dataverse for Teams")
    print("  Changing lookups to pm_staffmember keeps functionality while avoiding")
    print("  non-existent entity references")

    print("\n📋 Meaning:")
    print("  pm_evaluator: Points to staff member who performs evaluation")
    print("  pm_owner: Points to staff member who owns action item")

    print("\n⚠️  NEXT STEPS:")
    print("  1. Run: python scripts/pack_solution.py")
    print("  2. Test import into Teams environment")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
