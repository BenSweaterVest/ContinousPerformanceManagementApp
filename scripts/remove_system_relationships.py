#!/usr/bin/env python3
"""
Remove all system-generated entity relationships.

Keep only custom relationships between our entities.
Let Dataverse for Teams auto-generate system relationships it supports.

System relationships to remove:
- business_unit_*
- lk_*_createdby
- lk_*_modifiedby
- owner_*
- team_*
- user_*
- systemuser_*

Custom relationships to KEEP:
- pm_* to pm_* (our entity relationships)
"""

import re
from pathlib import Path

def remove_system_relationships(content: str) -> tuple[str, int, int]:
    """Remove system-generated EntityRelationship entries."""

    # Pattern to match EntityRelationship blocks
    pattern = r'<EntityRelationship Name="([^"]+)">.*?</EntityRelationship>'

    relationships = re.findall(pattern, content, re.DOTALL)

    # System relationship prefixes
    system_prefixes = [
        'business_unit_',
        'lk_',
        'owner_',
        'team_',
        'user_',
        'systemuser_'
    ]

    removed_count = 0
    kept_count = 0

    for rel in relationships:
        rel_name = rel[0] if isinstance(rel, tuple) else rel
        is_system = any(rel_name.startswith(prefix) for prefix in system_prefixes)

        if is_system:
            removed_count += 1
        else:
            kept_count += 1

    # Remove system relationships
    def should_keep(match):
        nonlocal removed_count
        rel_name = match.group(1)
        is_system = any(rel_name.startswith(prefix) for prefix in system_prefixes)

        if is_system:
            return ''  # Remove
        else:
            return match.group(0)  # Keep

    new_content = re.sub(pattern, should_keep, content, flags=re.DOTALL)

    return new_content, removed_count, kept_count


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("REMOVING SYSTEM-GENERATED RELATIONSHIPS")
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

    # Show current relationships
    print("📋 Current relationships:")
    current_rels = re.findall(r'<EntityRelationship Name="([^"]+)">', content)
    print(f"  Total: {len(current_rels)}")

    system_count = sum(1 for r in current_rels if any(r.startswith(p) for p in
                      ['business_unit_', 'lk_', 'owner_', 'team_', 'user_', 'systemuser_']))
    custom_count = len(current_rels) - system_count

    print(f"  System (to remove): {system_count}")
    print(f"  Custom (to keep): {custom_count}\n")

    # List custom relationships we're keeping
    print("✅ Custom relationships to KEEP:")
    custom_rels = [r for r in current_rels if not any(r.startswith(p) for p in
                  ['business_unit_', 'lk_', 'owner_', 'team_', 'user_', 'systemuser_'])]
    for rel in custom_rels:
        print(f"  - {rel}")

    # Remove system relationships
    print(f"\n🔧 Removing system-generated relationships...")
    new_content, removed, kept = remove_system_relationships(content)

    print(f"  ✓ Removed {removed} system relationships")
    print(f"  ✓ Kept {kept} custom relationships\n")

    # Write back
    print(f"💾 Writing updated Customizations.xml...")
    with open(customizations_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    new_size = len(new_content)
    size_diff = new_size - original_size
    print(f"  ✓ Updated size: {new_size:,} bytes ({size_diff:+,} bytes)")

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\n✅ Removed {removed} system relationships")
    print(f"✅ Kept {kept} custom relationships")
    print(f"📉 Size reduction: {-size_diff:,} bytes")
    print("\n💡 Rationale:")
    print("  System relationships (business_unit, owner, team, user, etc.) reference")
    print("  system entities that may trigger AsyncOperation/ProcessSession links.")
    print("  Dataverse for Teams will auto-generate supported system relationships")
    print("  during import, avoiding references to non-existent entities.")
    print("\n⚠️  NEXT STEPS:")
    print("  1. Run: python scripts/pack_solution.py")
    print("  2. Test import into Teams environment")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
