#!/usr/bin/env python3
"""
Update DisplayMask for all primary name fields in Entity.xml files.
"""

from pathlib import Path

entities = [
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

    # Replace the old DisplayMask with the new one
    old_mask = '<DisplayMask>ValidForAdvancedFind</DisplayMask>'
    new_mask = '<DisplayMask>PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid|RequiredForForm</DisplayMask>'

    # Check if this entity has a pm_name field that needs updating
    if 'PhysicalName="pm_name"' in content and old_mask in content:
        # Find the pm_name attribute section and update only that one
        lines = content.split('\n')
        in_pm_name = False
        updated = False

        for i, line in enumerate(lines):
            if 'PhysicalName="pm_name"' in line:
                in_pm_name = True
            elif in_pm_name and old_mask in line:
                lines[i] = line.replace(old_mask, new_mask)
                updated = True
                in_pm_name = False
            elif in_pm_name and '</attribute>' in line:
                in_pm_name = False

        if updated:
            content = '\n'.join(lines)
            with open(entity_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated {entity}")
        else:
            print(f"  - {entity} (no change needed)")
    else:
        print(f"  - {entity} (already correct or no pm_name field)")

print("\n✓ All Entity.xml files processed")
