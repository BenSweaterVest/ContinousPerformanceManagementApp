#!/usr/bin/env python3
"""
Remove system fields from entity definitions in customizations.xml
For new entities in unmanaged solutions, Dataverse creates system fields automatically
"""

import re
import xml.etree.ElementTree as ET

print("Removing system fields from all entities...")
print()

# Read the file
with open('/home/user/ContinousPerformanceManagementApp/solution/Other/Customizations.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all attribute blocks that have IsCustomField>0</IsCustomField> (system fields)
# We need to remove entire attribute blocks from <attribute PhysicalName="..."> to </attribute>

# Strategy: Parse and rebuild, keeping only custom fields and primary key
lines = content.split('\n')
new_lines = []
inside_attribute = False
attribute_buffer = []
keep_attribute = False
is_primary_key = False

for line in lines:
    # Check if we're starting an attribute
    if '<attribute PhysicalName=' in line:
        inside_attribute = True
        attribute_buffer = [line]
        keep_attribute = False
        is_primary_key = False
        continue

    # If we're inside an attribute
    if inside_attribute:
        attribute_buffer.append(line)

        # Check if it's a primary key (always keep these)
        if '<Type>primarykey</Type>' in line:
            is_primary_key = True
            keep_attribute = True

        # Check if it's a custom field
        if '<IsCustomField>1</IsCustomField>' in line:
            keep_attribute = True

        # Check if we're ending the attribute
        if '</attribute>' in line:
            inside_attribute = False

            # Only keep if it's custom or primary key
            if keep_attribute or is_primary_key:
                new_lines.extend(attribute_buffer)
            else:
                # This was a system field, skip it
                pass

            attribute_buffer = []
            continue
    else:
        # Not inside an attribute, keep the line
        new_lines.append(line)

new_content = '\n'.join(new_lines)

# Write back
print("Writing updated customizations.xml...")
with open('/home/user/ContinousPerformanceManagementApp/solution/Other/Customizations.xml', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✓ File updated: {len(new_lines)} lines")
print("✓ System fields removed, keeping only custom fields and primary keys")
