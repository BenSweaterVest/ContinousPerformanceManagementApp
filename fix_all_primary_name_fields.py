#!/usr/bin/env python3
"""
Update DisplayMask to include PrimaryName flag for ALL fields that have IsPrimaryName=1.
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

    if not entity_file.exists():
        print(f"✗ Not found: {entity}")
        continue

    with open(entity_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the attribute that has IsPrimaryName=1
    pattern = r'(<attribute PhysicalName="[^"]+">.*?)<DisplayMask>(ValidForAdvancedFind)</DisplayMask>(.*?<IsPrimaryName>1</IsPrimaryName>.*?</attribute>)'

    def replace_display_mask(match):
        return match.group(1) + '<DisplayMask>PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid|RequiredForForm</DisplayMask>' + match.group(3)

    new_content, count = re.subn(pattern, replace_display_mask, content, flags=re.DOTALL)

    if count > 0:
        with open(entity_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Updated {entity} ({count} field(s))")
    else:
        # Check if already has PrimaryName in DisplayMask
        if re.search(r'<DisplayMask>PrimaryName.*?<IsPrimaryName>1</IsPrimaryName>', content, re.DOTALL):
            print(f"  ✓ {entity} already has correct DisplayMask")
        else:
            print(f"  ? {entity} - no match found (might have different format)")

print("\n✓ All Entity.xml files processed")
