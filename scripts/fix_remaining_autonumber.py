#!/usr/bin/env python3
"""
Fix remaining auto-numbered fields that have DisplayMask but still missing API attributes.
"""

import re
from pathlib import Path

entities_with_autonumber = [
    'pm_meetingnote',
    'pm_recognition',
    'pm_actionitem'
]

tables_path = Path('/home/user/ContinousPerformanceManagementApp/solution/Tables')

API_ATTRS = '''<ImeMode>auto</ImeMode>
          <ValidForUpdateApi>1</ValidForUpdateApi>
          <ValidForReadApi>1</ValidForReadApi>
          <ValidForCreateApi>1</ValidForCreateApi>
          <IsCustomField>1</IsCustomField>
          <IsAuditEnabled>1</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <SourceType>0</SourceType>
          <IsGlobalFilterEnabled>0</IsGlobalFilterEnabled>
          <IsSortableEnabled>0</IsSortableEnabled>
          <CanModifyGlobalFilterSettings>1</CanModifyGlobalFilterSettings>
          <CanModifyIsSortableSettings>1</CanModifyIsSortableSettings>
          <IsDataSourceSecret>0</IsDataSourceSecret>
          <IsSearchable>1</IsSearchable>
          <IsFilterable>0</IsFilterable>
          <IsRetrievable>1</IsRetrievable>
          <IsLocalizable>0</IsLocalizable>
          <Format>text</Format>
          <MaxLength>100</MaxLength>'''

for entity in entities_with_autonumber:
    entity_file = tables_path / entity / 'Entity.xml'

    print(f"Processing {entity}...")

    with open(entity_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: pm_name field with DisplayMask and AutoNumberFormat but no ValidForUpdateApi
    pattern = r'(<attribute PhysicalName="pm_name">.*?<DisplayMask>.*?</DisplayMask>\s*<IsPrimaryName>1</IsPrimaryName>\s*<Length>\d+</Length>\s*)(<AutoNumberFormat>.*?</AutoNumberFormat>\s*)(<IntroducedVersion>)'

    def fix_field(match):
        # Check if already has ValidForUpdateApi
        if 'ValidForUpdateApi' in match.group(0):
            return match.group(0)

        print(f"  Fixing auto-numbered pm_name field")

        before_autonumber = match.group(1)
        autonumber = match.group(2)
        introduced = match.group(3)

        return before_autonumber + autonumber + API_ATTRS + '\n          ' + introduced

    new_content, count = re.subn(pattern, fix_field, content, flags=re.DOTALL)

    if count > 0:
        with open(entity_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Fixed {entity}")
    else:
        print(f"  - {entity} - no change or already fixed")

print("\n✓ All remaining auto-numbered fields fixed")
