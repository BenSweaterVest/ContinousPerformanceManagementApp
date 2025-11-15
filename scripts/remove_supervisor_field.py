#!/usr/bin/env python3
"""
Remove pm_supervisor lookup attributes from all entities.

The pm_supervisor field references systemuser entity which doesn't exist
in Dataverse for Teams and causes import errors.

This field appears in:
- pm_staffmember
- pm_meetingnote
- pm_recognition
"""

import re
from pathlib import Path

def remove_supervisor_attributes(content: str) -> tuple[str, int]:
    """Remove all pm_supervisor attribute definitions."""

    # Pattern to match the entire pm_supervisor attribute block
    # Looking for <attribute PhysicalName="pm_supervisor"> ... </attribute>
    pattern = r'<attribute PhysicalName="pm_supervisor">.*?</attribute>\s*\n'

    matches = re.findall(pattern, content, re.DOTALL)
    count = len(matches)

    if count > 0:
        new_content = re.sub(pattern, '', content, flags=re.DOTALL)
        return new_content, count

    return content, 0


def remove_supervisor_from_fetchxml(content: str) -> tuple[str, int]:
    """Remove pm_supervisor from saved query fetchxml."""

    # Pattern for fetchxml attribute reference
    pattern = r'\s*&lt;attribute name="pm_supervisor" /&gt;\s*\n'

    matches = re.findall(pattern, content)
    count = len(matches)

    if count > 0:
        new_content = re.sub(pattern, '', content)
        return new_content, count

    return content, 0


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("REMOVING PM_SUPERVISOR LOOKUP FIELDS")
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

    # Count current occurrences
    current_count = content.count('PhysicalName="pm_supervisor"')
    print(f"📋 Found {current_count} pm_supervisor attribute definitions")

    fetchxml_count = content.count('&lt;attribute name="pm_supervisor"')
    print(f"📋 Found {fetchxml_count} pm_supervisor references in fetchxml\n")

    # Remove attribute definitions
    print("🔧 Removing pm_supervisor attribute definitions...")
    content, attrs_removed = remove_supervisor_attributes(content)
    print(f"  ✓ Removed {attrs_removed} attribute definitions")

    # Remove fetchxml references
    print("\n🔧 Removing pm_supervisor from saved queries...")
    content, fetch_removed = remove_supervisor_from_fetchxml(content)
    print(f"  ✓ Removed {fetch_removed} fetchxml references")

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
    print(f"\n✅ Removed {attrs_removed} pm_supervisor attribute definitions")
    print(f"✅ Removed {fetch_removed} fetchxml references")
    print(f"📉 Size reduction: {-size_diff:,} bytes")

    print("\n💡 Rationale:")
    print("  pm_supervisor referenced systemuser entity via <Target>systemuser</Target>")
    print("  systemuser entity doesn't exist in Dataverse for Teams")
    print("  Removing this lookup eliminates the missing relationship error")

    print("\n📝 Entities affected:")
    print("  - pm_staffmember (supervisor field removed)")
    print("  - pm_meetingnote (supervisor field removed)")
    print("  - pm_recognition (supervisor field removed)")

    print("\n⚠️  NEXT STEPS:")
    print("  1. Run: python scripts/pack_solution.py")
    print("  2. Test import into Teams environment")
    print("  3. Supervisor functionality can be added back later with self-referential lookup")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
