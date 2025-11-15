#!/usr/bin/env python3
"""
Convert solution from Unmanaged to Managed.

All 5 Microsoft Teams sample solutions are managed.
This might be required for Teams import.
"""

from pathlib import Path

def convert_to_managed():
    """Convert Solution.xml from Unmanaged to Managed."""
    print("\n" + "="*80)
    print("CONVERTING SOLUTION TO MANAGED")
    print("="*80 + "\n")

    solution_path = Path(__file__).parent.parent / "solution" / "Other" / "Solution.xml"

    if not solution_path.exists():
        print(f"❌ ERROR: File not found: {solution_path}")
        return False

    print(f"📂 Reading: {solution_path}")
    with open(solution_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check current state
    if "<Managed>1</Managed>" in content:
        print("  ℹ️  Solution is already managed")
        return True
    elif "<Managed>0</Managed>" in content:
        print("  📝 Current: Unmanaged (0)")
        content = content.replace("<Managed>0</Managed>", "<Managed>1</Managed>")
        print("  ✓ Changed to: Managed (1)")
    else:
        print("  ❌ ERROR: Could not find <Managed> element")
        return False

    print(f"\n💾 Writing updated Solution.xml...")
    with open(solution_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("  ✓ Solution.xml updated")

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("\n✅ Solution converted from Unmanaged to Managed")
    print("\n📋 Next steps:")
    print("  1. Run: python scripts/pack_solution.py")
    print("  2. Test import into Teams environment")
    print("\n⚠️  Note: All 5 Microsoft Teams sample solutions are managed")
    print("   This conversion aligns with Microsoft's Teams solution format")
    print("\n" + "="*80 + "\n")

    return True


if __name__ == "__main__":
    success = convert_to_managed()
    exit(0 if success else 1)
