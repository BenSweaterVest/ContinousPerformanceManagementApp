#!/usr/bin/env python3
"""
Fix the 6 entities that are missing primarykey attributes.
This time use a more flexible pattern.
"""

import re
from pathlib import Path

# The full set of attributes to add
PRIMARYKEY_FULL_ATTRIBUTES = '''<IsValidForCreate>0</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>0</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>1</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <ImeMode>auto</ImeMode>
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
          <MaxLength>100</MaxLength>
          <IsSearchable>0</IsSearchable>
          <IsFilterable>1</IsFilterable>
          <IsRetrievable>1</IsRetrievable>
          <IsLocalizable>0</IsLocalizable>'''

entities = [
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

    # Pattern: Find primarykey attribute, add attributes before IntroducedVersion
    # More flexible: just look for IsPrimaryId followed by IntroducedVersion
    pattern = r'(<attribute PhysicalName="' + entity + r'id">.*?<IsPrimaryId>1</IsPrimaryId>\s+)(<IntroducedVersion>)'

    def add_attributes(match):
        # Check if already has these attributes
        if 'ValidForCreateApi' in match.group(1):
            return match.group(0)  # Already fixed
        return match.group(1) + PRIMARYKEY_FULL_ATTRIBUTES + '\n          ' + match.group(2)

    new_content, count = re.subn(pattern, add_attributes, content, flags=re.DOTALL)

    if count > 0:
        with open(entity_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Fixed {entity}")
    else:
        print(f"  ? {entity} - pattern didn't match or already fixed")

print("\n✓ All entities fixed. Now re-merging...")
