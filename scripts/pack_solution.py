#!/usr/bin/env python3
"""
Pack the solution into a distributable ZIP file.

This script creates a ZIP package from the unpacked solution directory.
The ZIP structure must match Dataverse solution format:
  - [Content_Types].xml at root
  - Other/
  - CanvasApps/
  - Workflows/
  - Tables/
"""

import zipfile
from pathlib import Path
import os

def pack_solution():
    """Pack the solution directory into a ZIP file."""
    print("\n" + "="*80)
    print("PACKING SOLUTION")
    print("="*80 + "\n")

    # Paths
    project_root = Path(__file__).parent.parent
    solution_dir = project_root / "solution"
    output_file = project_root / "PerformanceManagement_1_0_1_0.zip"

    # Verify solution directory exists
    if not solution_dir.exists():
        print(f"❌ ERROR: Solution directory not found: {solution_dir}")
        return False

    print(f"📂 Source directory: {solution_dir}")
    print(f"📦 Output file: {output_file}")

    # Remove existing ZIP if present
    if output_file.exists():
        print(f"🗑️  Removing existing package...")
        output_file.unlink()

    # Create ZIP file
    print(f"\n📦 Creating ZIP package...")
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through all files in solution directory
        file_count = 0
        for root, dirs, files in os.walk(solution_dir):
            for file in files:
                # Get full file path
                file_path = Path(root) / file

                # Calculate archive path (relative to solution dir)
                archive_path = file_path.relative_to(solution_dir)

                # Add to ZIP
                zipf.write(file_path, archive_path)
                file_count += 1

                # Show progress for key files
                if file in ['[Content_Types].xml', 'Solution.xml', 'Customizations.xml']:
                    print(f"  ✓ Added: {archive_path}")

        print(f"\n  ✓ Added {file_count} files total")

    # Verify the ZIP was created
    if not output_file.exists():
        print(f"\n❌ ERROR: Failed to create ZIP file")
        return False

    # Show file size
    file_size_bytes = output_file.stat().st_size
    file_size_mb = file_size_bytes / (1024 * 1024)

    print("\n" + "="*80)
    print("SUCCESS")
    print("="*80)
    print(f"\n✅ Solution packed successfully!")
    print(f"\n📄 Output file: {output_file.name}")
    print(f"📊 File size: {file_size_mb:.2f} MB ({file_size_bytes:,} bytes)")
    print(f"📂 Location: {output_file.parent}")

    print("\n📋 Next steps:")
    print("  1. Review the package")
    print("  2. Import into Teams Power Apps environment")
    print("  3. Map connection references during import")
    print("  4. Turn on flows after import")

    print("\n" + "="*80 + "\n")

    return True


if __name__ == "__main__":
    success = pack_solution()
    exit(0 if success else 1)
