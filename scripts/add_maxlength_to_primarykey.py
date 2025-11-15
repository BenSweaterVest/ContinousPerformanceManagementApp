#!/usr/bin/env python3
"""
Add MaxLength to primarykey fields as Teams/Dataverse might require it.
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

    # Add MaxLength after AutoNumberFormat in primarykey fields
    pattern = r'(<attribute PhysicalName="' + entity + r'id">.*?<Type>primarykey</Type>.*?<AutoNumberFormat></AutoNumberFormat>)(\s+<IsSearchable>)'

    def add_maxlength(match):
        # Check if MaxLength already exists
        if 'MaxLength' in match.group(0):
            return match.group(0)
        return match.group(1) + '\n          <MaxLength>100</MaxLength>' + match.group(2)

    new_content, count = re.subn(pattern, add_maxlength, content, flags=re.DOTALL)

    if count > 0:
        with open(entity_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Added MaxLength to primarykey in {entity}")
    else:
        print(f"  - {entity} (already has MaxLength or pattern not matched)")

print("\n✓ All primarykey fields updated with MaxLength")
