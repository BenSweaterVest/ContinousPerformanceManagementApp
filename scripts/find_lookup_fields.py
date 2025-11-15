#!/usr/bin/env python3
"""
Find all custom lookup fields (pm_ prefix) in our solution.
System lookups (createdby, modifiedby, owning*, etc.) don't need custom relationship definitions.
"""

import re
from pathlib import Path
import xml.etree.ElementTree as ET

entities = [
    'pm_staffmember',
    'pm_evaluationquestion',
    'pm_weeklyevaluation',
    'pm_selfevaluation',
    'pm_idpentry',
    'pm_meetingnote',
    'pm_goal',
    'pm_recognition',
    'pm_actionitem'
]

tables_path = Path('/home/user/ContinousPerformanceManagementApp/solution/Tables')

lookups = []

for entity in entities:
    entity_file = tables_path / entity / 'Entity.xml'

    with open(entity_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all lookup attributes
    lookup_pattern = r'<attribute PhysicalName="(pm_\w+)">.*?<Type>lookup</Type>.*?<Targets>\s*<Target>(.*?)</Target>\s*</Targets>'
    lookup_matches = re.findall(lookup_pattern, content, re.DOTALL)

    for field_name, target_entity in lookup_matches:
        lookups.append({
            'entity': entity,
            'field': field_name,
            'target': target_entity
        })
        print(f"{entity}.{field_name} -> {target_entity}")

print(f"\nTotal custom lookup fields: {len(lookups)}")

# Write to a file for reference
with open('/home/user/ContinousPerformanceManagementApp/lookup_fields.txt', 'w') as f:
    for lookup in lookups:
        f.write(f"{lookup['entity']}.{lookup['field']} -> {lookup['target']}\n")

print("\nSaved to lookup_fields.txt")
