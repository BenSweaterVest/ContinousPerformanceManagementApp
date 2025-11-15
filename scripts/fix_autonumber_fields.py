#!/usr/bin/env python3
"""
Fix auto-numbered primary name fields that are missing API attributes and DisplayMask.
These fields have AutoNumberFormat but no DisplayMask.
"""

import re
from pathlib import Path

# Entities with auto-numbered primary names
entities_with_autonumber = [
    'pm_selfevaluation',
    'pm_meetingnote',
    'pm_recognition',
    'pm_actionitem'
]

tables_path = Path('/home/user/ContinousPerformanceManagementApp/solution/Tables')

API_ATTRS = '''<DisplayMask>PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid|RequiredForForm</DisplayMask>
          <ImeMode>auto</ImeMode>
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

    # Pattern: Find pm_name field with IsPrimaryName and AutoNumberFormat but missing ValidForUpdateApi
    pattern = r'(<attribute PhysicalName="pm_name">.*?<Type>nvarchar</Type>.*?<RequiredLevel>.*?</RequiredLevel>\s*)(<IsPrimaryName>1</IsPrimaryName>\s*<Length>\d+</Length>\s*)(<AutoNumberFormat>.*?</AutoNumberFormat>\s*)(<IntroducedVersion>)'

    def fix_field(match):
        # Check if already has ValidForUpdateApi
        if 'ValidForUpdateApi' in match.group(0):
            return match.group(0)

        print(f"  Fixing auto-numbered pm_name field")

        before_isprimary = match.group(1)
        isprimary_and_length = match.group(2)
        autonumber = match.group(3)
        introduced = match.group(4)

        return before_isprimary + isprimary_and_length + autonumber + API_ATTRS + '\n          ' + introduced

    new_content, count = re.subn(pattern, fix_field, content, flags=re.DOTALL)

    if count > 0:
        with open(entity_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Fixed {entity}")
    else:
        print(f"  - {entity} - no change or already fixed")

print("\n✓ All auto-numbered fields fixed")
