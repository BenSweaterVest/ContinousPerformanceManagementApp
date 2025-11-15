#!/usr/bin/env python3
"""
Add missing API attributes to ALL custom nvarchar and memo fields.
This script handles fields with Length, MaxLength, or both.
Based on Microsoft Boards solution structure.
"""

import re
from pathlib import Path

# Attributes to add to custom text fields (based on Microsoft's pattern)
API_ATTRIBUTES = '''<ImeMode>auto</ImeMode>
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
          <IsLocalizable>0</IsLocalizable>'''

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

    print(f"\nProcessing {entity}...")

    with open(entity_file, 'r', encoding='utf-8') as f:
        content = f.read()

    changes_made = []

    # Pattern: Find nvarchar or memo fields with pm_ prefix that don't already have ValidForUpdateApi
    # This captures the section up to IntroducedVersion
    pattern = r'(<attribute PhysicalName="(pm_\w+)">\s*<Type>(nvarchar|memo)</Type>.*?<DisplayMask>.*?</DisplayMask>\s*(?:<IsPrimaryName>1</IsPrimaryName>\s*)?)(?!.*?<ValidForUpdateApi>)(.*?)(<IntroducedVersion>)'

    def add_attributes(match):
        full_match = match.group(0)

        # Skip if already has ValidForUpdateApi (double check)
        if 'ValidForUpdateApi' in full_match:
            return full_match

        field_name = match.group(2)
        field_type = match.group(3)
        before_attrs = match.group(1)  # Everything before we insert
        middle_attrs = match.group(4)  # Length/MaxLength/etc already there
        introduced = match.group(5)    # IntroducedVersion tag

        print(f"  Adding API attributes to {field_name} ({field_type})")
        changes_made.append(field_name)

        # For nvarchar fields, add Format=text
        # For memo fields, don't add Format
        if field_type == 'nvarchar':
            api_attrs = API_ATTRIBUTES + '\n          <Format>text</Format>'
        else:
            api_attrs = API_ATTRIBUTES

        # Check if we need to add MaxLength
        # For nvarchar: if it has Length but not MaxLength, add MaxLength
        if field_type == 'nvarchar' and 'Length>' in middle_attrs and 'MaxLength>' not in middle_attrs:
            # Extract Length value
            length_match = re.search(r'<Length>(\d+)</Length>', middle_attrs)
            if length_match:
                length_value = length_match.group(1)
                # For primary name fields, use MaxLength=100
                if 'IsPrimaryName' in before_attrs:
                    maxlength = '<MaxLength>100</MaxLength>\n          '
                else:
                    maxlength = f'<MaxLength>{length_value}</MaxLength>\n          '
                middle_attrs = middle_attrs.rstrip() + '\n          ' + maxlength
                print(f"    Also adding MaxLength to {field_name}")

        return before_attrs + middle_attrs + api_attrs + '\n          ' + introduced

    new_content = re.sub(pattern, add_attributes, content, flags=re.DOTALL)

    if changes_made:
        with open(entity_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Updated {entity} ({len(changes_made)} fields)")
    else:
        print(f"  - {entity} - no changes needed")

print("\n✓ All custom fields updated with API attributes")
