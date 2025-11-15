#!/usr/bin/env python3
"""
Add DisplayMask to fields that have IsPrimaryName=1 but no DisplayMask.
"""

import re
from pathlib import Path

entities = [
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

    # Find the attribute that has IsPrimaryName=1 but no DisplayMask before it
    # Pattern: RequiredLevel followed directly by IsPrimaryName (no DisplayMask in between)
    pattern = r'(<RequiredLevel>[^<]+</RequiredLevel>)\s+(<IsPrimaryName>1</IsPrimaryName>)'

    def add_display_mask(match):
        return match.group(1) + '\n          <DisplayMask>PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid|RequiredForForm</DisplayMask>\n          ' + match.group(2)

    new_content, count = re.subn(pattern, add_display_mask, content)

    if count > 0:
        with open(entity_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Added DisplayMask to {entity}")
    else:
        print(f"  - {entity} (already has DisplayMask or different format)")

print("\n✓ All Entity.xml files processed")
