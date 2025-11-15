#!/usr/bin/env python3
"""
Add missing API attributes to all custom nvarchar and memo fields.
Based on Microsoft Boards solution structure.
"""

import re
from pathlib import Path
import xml.etree.ElementTree as ET

# Attributes to add to nvarchar/memo fields (based on Microsoft's pattern)
NVARCHAR_ATTRIBUTES_TEMPLATE = '''<ImeMode>auto</ImeMode>
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
          <AutoNumberFormat></AutoNumberFormat>
          <IsSearchable>1</IsSearchable>
          <IsFilterable>0</IsFilterable>
          <IsRetrievable>1</IsRetrievable>
          <IsLocalizable>0</IsLocalizable>
          <Format>text</Format>'''

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

def add_maxlength_to_field(content, length_value):
    """Add MaxLength based on Length value"""
    # MaxLength is typically the same as Length for display purposes
    # but can be different - Microsoft often uses MaxLength=100 for primary names with Length=1600
    return f'<MaxLength>{length_value}</MaxLength>\n          '

for entity in entities:
    entity_file = tables_path / entity / 'Entity.xml'

    print(f"\nProcessing {entity}...")

    with open(entity_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all nvarchar/memo attributes that don't have API attributes
    # Pattern: nvarchar or memo attributes with Length but missing ValidForUpdateApi
    pattern = r'(<attribute PhysicalName="(pm_\w+)">\s*<Type>(nvarchar|memo)</Type>.*?<DisplayMask>.*?</DisplayMask>\s*)(<IsPrimaryName>1</IsPrimaryName>\s*)?(<Length>(\d+)</Length>\s*)(<IntroducedVersion>)'

    changes_made = []

    def add_attributes(match):
        full_match = match.group(0)

        # Skip if already has ValidForUpdateApi
        if 'ValidForUpdateApi' in full_match:
            return full_match

        field_name = match.group(2)
        field_type = match.group(3)
        before_length = match.group(1)
        is_primary = match.group(4) if match.group(4) else ''
        length_elem = match.group(5)
        length_value = match.group(6)
        introduced = match.group(7)

        print(f"  Adding attributes to {field_name} ({field_type}, Length={length_value})")
        changes_made.append(field_name)

        # For primary name fields, use MaxLength=100, otherwise use same as Length
        if is_primary:
            maxlength = '<MaxLength>100</MaxLength>\n          '
        else:
            maxlength = f'<MaxLength>{length_value}</MaxLength>\n          '

        # For memo fields, don't add Format=text
        if field_type == 'memo':
            attributes = NVARCHAR_ATTRIBUTES_TEMPLATE.replace('\n          <Format>text</Format>', '')
        else:
            attributes = NVARCHAR_ATTRIBUTES_TEMPLATE

        return before_length + is_primary + length_elem + maxlength + attributes + '\n          ' + introduced

    new_content = re.sub(pattern, add_attributes, content, flags=re.DOTALL)

    if changes_made:
        with open(entity_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Updated {entity}")
    else:
        print(f"  - {entity} - no changes needed")

print("\n✓ All custom fields updated with API attributes")
