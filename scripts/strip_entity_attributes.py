#!/usr/bin/env python3
"""
Remove entity-level attributes to match Microsoft Teams solution format.

Microsoft's managed solutions only have Name attribute on the entity tag.
All other metadata is stored as child elements.

This is critical for Teams import success!
"""

import re
from pathlib import Path

def strip_entity_attributes(content: str) -> tuple[str, int]:
    """
    Strip all attributes from entity tags except Name.

    Before:
    <entity Name="pm_StaffMember" OwnershipType="UserOwned" ... IntroducedVersion="1.0">

    After:
    <entity Name="pm_StaffMember">
    """
    # Pattern to match entity opening tags with all their attributes
    pattern = r'<entity\s+Name="([^"]+)"[^>]*>'

    entities_found = re.findall(pattern, content)

    # Replace with minimal entity tag
    new_content = re.sub(pattern, r'<entity Name="\1">', content)

    return new_content, len(entities_found)


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("STRIPPING ENTITY-LEVEL ATTRIBUTES (Teams Format)")
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

    # Show current entity tags
    print("📋 Current entity tags (first 3):")
    current_tags = re.findall(r'<entity\s+Name="[^"]+"\s+[^>]{50,150}', content)
    for i, tag in enumerate(current_tags[:3], 1):
        print(f"  {i}. {tag}...")

    # Strip attributes
    print("\n🔧 Stripping entity-level attributes...")
    new_content, entities_fixed = strip_entity_attributes(content)

    print(f"  ✓ Fixed {entities_fixed} entity tags\n")

    # Show new entity tags
    print("📋 New entity tags (all):")
    new_tags = re.findall(r'<entity Name="([^"]+)">', new_content)
    for i, name in enumerate(new_tags, 1):
        print(f"  {i}. <entity Name=\"{name}\">")

    # Write back
    print(f"\n💾 Writing updated Customizations.xml...")
    with open(customizations_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    new_size = len(new_content)
    size_diff = new_size - original_size
    print(f"  ✓ Updated size: {new_size:,} bytes ({size_diff:+,} bytes)")

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\n✅ Stripped attributes from {entities_fixed} entity tags")
    print(f"📉 Size reduction: {-size_diff:,} bytes")
    print("\n✨ Entity tags now match Microsoft Teams solution format!")
    print("\n⚠️  NEXT STEPS:")
    print("  1. Run: python scripts/pack_solution.py")
    print("  2. Test import into Teams environment")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
