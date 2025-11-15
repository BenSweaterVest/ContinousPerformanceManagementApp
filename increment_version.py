#!/usr/bin/env python3
"""
Version Increment Script for Performance Management Solution

Increments the version number in Solution.xml and updates related files.

Usage:
    python increment_version.py [major|minor|build|revision]

Examples:
    python increment_version.py revision    # 1.0.0.0 -> 1.0.0.1 (default)
    python increment_version.py build       # 1.0.0.0 -> 1.0.1.0
    python increment_version.py minor       # 1.0.0.0 -> 1.1.0.0
    python increment_version.py major       # 1.0.0.0 -> 2.0.0.0
"""

import re
import sys
from pathlib import Path
from typing import Tuple

def get_current_version() -> Tuple[str, int, int, int, int]:
    """Read current version from Solution.xml"""
    solution_xml = Path("solution/Other/Solution.xml")

    if not solution_xml.exists():
        print(f"❌ ERROR: {solution_xml} not found!")
        print("   Make sure you run this from the repository root.")
        sys.exit(1)

    content = solution_xml.read_text(encoding='utf-8-sig')

    # Find version tag
    match = re.search(r'<Version>(\d+)\.(\d+)\.(\d+)\.(\d+)</Version>', content)
    if not match:
        print("❌ ERROR: Could not find <Version> tag in Solution.xml")
        sys.exit(1)

    major, minor, build, revision = map(int, match.groups())
    version_str = f"{major}.{minor}.{build}.{revision}"

    return version_str, major, minor, build, revision

def increment_version(component: str, major: int, minor: int, build: int, revision: int) -> str:
    """Increment the specified version component"""
    if component == "major":
        return f"{major + 1}.0.0.0"
    elif component == "minor":
        return f"{major}.{minor + 1}.0.0"
    elif component == "build":
        return f"{major}.{minor}.{build + 1}.0"
    elif component == "revision":
        return f"{major}.{minor}.{build}.{revision + 1}"
    else:
        print(f"❌ ERROR: Invalid component '{component}'")
        print("   Valid options: major, minor, build, revision")
        sys.exit(1)

def update_solution_xml(old_version: str, new_version: str):
    """Update version in Solution.xml"""
    solution_xml = Path("solution/Other/Solution.xml")
    content = solution_xml.read_text(encoding='utf-8-sig')

    # Replace version
    content = content.replace(
        f"<Version>{old_version}</Version>",
        f"<Version>{new_version}</Version>"
    )

    solution_xml.write_text(content, encoding='utf-8-sig')
    print(f"   ✓ Updated Solution.xml")

def update_pack_scripts(old_version: str, new_version: str):
    """Update version in pack scripts"""
    old_file = f"PerformanceManagement_{old_version.replace('.', '_')}.zip"
    new_file = f"PerformanceManagement_{new_version.replace('.', '_')}.zip"

    updated_files = []

    # Update pack-solution.ps1
    pack_script = Path("deployment/pack-solution.ps1")
    if pack_script.exists():
        content = pack_script.read_text(encoding='utf-8')
        content = content.replace(
            f'$outputFile = "{old_file}"',
            f'$outputFile = "{new_file}"'
        )
        pack_script.write_text(content, encoding='utf-8')
        updated_files.append("deployment/pack-solution.ps1")

    # Update pack-solution-manual.ps1
    pack_manual = Path("deployment/pack-solution-manual.ps1")
    if pack_manual.exists():
        content = pack_manual.read_text(encoding='utf-8')
        content = content.replace(
            f'$outputFile = "{old_file}"',
            f'$outputFile = "{new_file}"'
        )
        pack_manual.write_text(content, encoding='utf-8')
        updated_files.append("deployment/pack-solution-manual.ps1")

    # Update import-solution.ps1
    import_script = Path("deployment/import-solution.ps1")
    if import_script.exists():
        content = import_script.read_text(encoding='utf-8')
        content = content.replace(
            f'$packageFile = "{old_file}"',
            f'$packageFile = "{new_file}"'
        )
        import_script.write_text(content, encoding='utf-8')
        updated_files.append("deployment/import-solution.ps1")

    if updated_files:
        print(f"   ✓ Updated {len(updated_files)} pack/import scripts")
        for file in updated_files:
            print(f"     • {file}")

def main():
    print("=" * 70)
    print("Performance Management Solution - Version Increment")
    print("=" * 70)
    print()

    # Get component to increment (default: revision)
    component = sys.argv[1] if len(sys.argv) > 1 else "revision"

    # Validate component
    valid_components = ["major", "minor", "build", "revision"]
    if component not in valid_components:
        print(f"❌ ERROR: Invalid component '{component}'")
        print(f"   Valid options: {', '.join(valid_components)}")
        print()
        print("Usage:")
        print("   python increment_version.py [major|minor|build|revision]")
        sys.exit(1)

    # Get current version
    old_version, major, minor, build, revision = get_current_version()
    print(f"Current version: {old_version}")

    # Calculate new version
    new_version = increment_version(component, major, minor, build, revision)
    print(f"New version:     {new_version} (incrementing {component})")
    print()

    # Confirm
    response = input("Proceed with version update? (y/N): ")
    if response.lower() != 'y':
        print("❌ Aborted by user")
        sys.exit(0)

    print()
    print("Updating files...")

    # Update Solution.xml
    update_solution_xml(old_version, new_version)

    # Update pack scripts
    update_pack_scripts(old_version, new_version)

    print()
    print("=" * 70)
    print(f"✅ SUCCESS: Version updated to {new_version}")
    print("=" * 70)
    print()
    print("Files updated:")
    print("  • solution/Other/Solution.xml")
    print("  • deployment/pack-solution.ps1")
    print("  • deployment/pack-solution-manual.ps1")
    print("  • deployment/import-solution.ps1")
    print()
    print("Next steps:")
    print("  1. Review the changes")
    print("  2. Run deployment scripts to create new package")
    print(f"  3. Commit: git add . && git commit -m 'Bump version to {new_version}'")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Aborted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
