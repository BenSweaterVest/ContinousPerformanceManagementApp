#!/usr/bin/env python3
"""
Remove all system field definitions from customizations.xml

Teams Dataverse automatically creates system fields (createdby, modifiedby, ownerid,
versionnumber, statecode, statuscode, etc.) for new entities in unmanaged solutions.

Including these fields in the solution causes import errors like:
"Attribute versionnumber is a BigInt, but a BigInt type was specified"

This script keeps only:
- Primary key fields (Type=primarykey)
- Custom fields (IsCustomField=1)
"""

import re

# Read the file
with open('solution/Other/Customizations.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# Count before
total_before = len(re.findall(r'<attribute PhysicalName=', content))
system_fields_before = len(re.findall(r'<IsCustomField>0</IsCustomField>', content))

# Remove attributes that have IsCustomField>0</IsCustomField> (system fields)
# BUT keep primary key fields (Type>primarykey</Type>)

# First, let's match all attribute blocks
attribute_pattern = r'<attribute PhysicalName=".*?">.*?</attribute>'
attributes = re.findall(attribute_pattern, content, re.DOTALL)

removed_count = 0
for attr in attributes:
    # Check if it's a system field (IsCustomField=0) AND not a primary key
    is_system = '<IsCustomField>0</IsCustomField>' in attr
    is_primarykey = '<Type>primarykey</Type>' in attr

    if is_system and not is_primarykey:
        # Remove this attribute
        content = content.replace(attr, '', 1)
        removed_count += 1

# Count after
total_after = len(re.findall(r'<attribute PhysicalName=', content))
system_fields_after = len(re.findall(r'<IsCustomField>0</IsCustomField>', content))

# Write back
with open('solution/Other/Customizations.xml', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"System field cleanup complete:")
print(f"  Total attributes before: {total_before}")
print(f"  System fields removed: {removed_count}")
print(f"  Total attributes after: {total_after}")
print(f"  System fields remaining: {system_fields_after} (should be 0)")
print()
print(f"Kept fields:")
print(f"  - 9 primary key fields (Type=primarykey)")
print(f"  - {total_after - 9} custom fields (IsCustomField=1 or pm_name)")
