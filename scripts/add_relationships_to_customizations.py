#!/usr/bin/env python3
"""
Add EntityRelationships section to Customizations.xml.
"""

from pathlib import Path

customizations_path = Path('/home/user/ContinousPerformanceManagementApp/solution/Other/Customizations.xml')
relationships_path = Path('/home/user/ContinousPerformanceManagementApp/relationships.xml')

# Read both files
with open(customizations_path, 'r', encoding='utf-8') as f:
    customizations_content = f.read()

with open(relationships_path, 'r', encoding='utf-8') as f:
    relationships_content = f.read()

# Replace the empty EntityRelationships tag with the full section
customizations_content = customizations_content.replace(
    '  <EntityRelationships />',
    relationships_content
)

# Write back
with open(customizations_path, 'w', encoding='utf-8') as f:
    f.write(customizations_content)

print("✓ Added EntityRelationships to Customizations.xml")

# Check file size
file_size = customizations_path.stat().st_size
print(f"✓ Customizations.xml size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
