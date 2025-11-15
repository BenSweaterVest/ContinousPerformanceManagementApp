#!/usr/bin/env python3
"""
Fix DisplayMask for primary name attributes in all Entity.xml files.
"""

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

    if not entity_file.exists():
        print(f"✗ Not found: {entity}")
        continue

    with open(entity_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the pm_name attribute section and update DisplayMask
    # Looking for pattern where DisplayMask is ValidForAdvancedFind and IsPrimaryName is present
    old_pattern = '<DisplayMask>ValidForAdvancedFind</DisplayMask>\n              <IsPrimaryName>1</IsPrimaryName>'
    new_pattern = '<DisplayMask>PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid|RequiredForForm</DisplayMask>\n              <IsPrimaryName>1</IsPrimaryName>'

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)

        with open(entity_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Updated {entity}")
    else:
        print(f"  - {entity} already has correct DisplayMask or different format")

print("\n✓ All Entity.xml files updated")
print("Re-running merge script...")
