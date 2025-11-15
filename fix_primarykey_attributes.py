#!/usr/bin/env python3
"""
Add all required attributes to primarykey fields to match Microsoft's structure.
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

# Template for additional primarykey attributes (based on Microsoft Boards)
PRIMARYKEY_ADDITIONS = '''<ImeMode>auto</ImeMode>
          <ValidForUpdateApi>0</ValidForUpdateApi>
          <ValidForReadApi>1</ValidForReadApi>
          <ValidForCreateApi>1</ValidForCreateApi>
          <SourceType>0</SourceType>
          <IsGlobalFilterEnabled>0</IsGlobalFilterEnabled>
          <IsSortableEnabled>0</IsSortableEnabled>
          <CanModifyGlobalFilterSettings>1</CanModifyGlobalFilterSettings>
          <CanModifyIsSortableSettings>1</CanModifyIsSortableSettings>
          <IsDataSourceSecret>0</IsDataSourceSecret>
          <AutoNumberFormat></AutoNumberFormat>
          <IsSearchable>0</IsSearchable>
          <IsFilterable>1</IsFilterable>
          <IsRetrievable>1</IsRetrievable>
          <IsLocalizable>0</IsLocalizable>'''

tables_path = Path('/home/user/ContinousPerformanceManagementApp/solution/Tables')

for entity in entities:
    entity_file = tables_path / entity / 'Entity.xml'

    with open(entity_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the primary ID attribute and add missing attributes
    # Pattern: Find <Type>primarykey</Type> followed by attributes, insert before IntroducedVersion
    pattern = r'(<attribute PhysicalName="' + entity + r'id">.*?<Type>primarykey</Type>.*?<IsSecured>0</IsSecured>\s+)(<IntroducedVersion>)'

    def add_attributes(match):
        # Check if ImeMode already exists
        if 'ImeMode' in match.group(1):
            return match.group(0)  # Already has the additions
        return match.group(1) + PRIMARYKEY_ADDITIONS + '\n          ' + match.group(2)

    new_content, count = re.subn(pattern, add_attributes, content, flags=re.DOTALL)

    if count > 0:
        with open(entity_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Added primarykey attributes to {entity}")
    else:
        print(f"  - {entity} (already has attributes or not found)")

print("\n✓ All primarykey fields updated")
