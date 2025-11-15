#!/usr/bin/env python3
"""
Remove MaxLength from primarykey fields - Microsoft doesn't have this attribute.
Based on comparison with Microsoft Boards solution.
"""

import re
from pathlib import Path

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

for entity in entities:
    entity_file = tables_path / entity / 'Entity.xml'

    with open(entity_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove MaxLength line from primarykey fields
    # Pattern: find the MaxLength line and its surrounding whitespace
    pattern = r'(\s*<MaxLength>100</MaxLength>\n)(?=\s*<IsSearchable>)'

    # Check if this is in a primarykey attribute section
    primarykey_pattern = r'(<attribute PhysicalName="' + entity + r'id">.*?<Type>primarykey</Type>.*?)<MaxLength>100</MaxLength>\s*\n(\s*<IsSearchable>.*?</attribute>)'

    if re.search(primarykey_pattern, content, re.DOTALL):
        new_content = re.sub(primarykey_pattern, r'\1\2', content, flags=re.DOTALL)

        if new_content != content:
            with open(entity_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ Removed MaxLength from {entity}")
        else:
            print(f"  - {entity} - no change needed")
    else:
        print(f"  ? {entity} - pattern not found or already removed")

print("\n✓ All primarykey MaxLength attributes removed")
