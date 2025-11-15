#!/usr/bin/env python3
"""
Add missing API attributes to ALL remaining custom nvarchar and memo fields.
Simple approach: find each field, check if it has ValidForUpdateApi, if not, add all attributes.
"""

import re
from pathlib import Path

# API attributes template (without Format, we'll add that conditionally)
API_ATTRS_BASE = '''<ImeMode>auto</ImeMode>
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

    original_content = content
    fields_updated = []

    # Find all custom nvarchar/memo fields
    field_pattern = r'<attribute PhysicalName="(pm_\w+)">.*?</attribute>'
    field_matches = list(re.finditer(field_pattern, content, re.DOTALL))

    for match in field_matches:
        field_content = match.group(0)
        field_name = match.group(1)

        # Check if it's nvarchar or memo
        if '<Type>nvarchar</Type>' not in field_content and '<Type>memo</Type>' not in field_content:
            continue

        # Skip if already has ValidForUpdateApi
        if 'ValidForUpdateApi' in field_content:
            continue

        # Determine field type
        is_nvarchar = '<Type>nvarchar</Type>' in field_content
        field_type = 'nvarchar' if is_nvarchar else 'memo'

        print(f"  Fixing {field_name} ({field_type})")
        fields_updated.append(field_name)

        # Build the API attributes to insert
        if is_nvarchar:
            api_attrs = API_ATTRS_BASE + '\n          <Format>text</Format>'
        else:
            api_attrs = API_ATTRS_BASE

        # Check if we need to add MaxLength for nvarchar fields
        if is_nvarchar and 'MaxLength>' not in field_content and 'Length>' in field_content:
            # Extract Length value
            length_match = re.search(r'<Length>(\d+)</Length>', field_content)
            if length_match:
                length_value = length_match.group(1)
                # For primary name, use 100, otherwise use same as Length
                if 'IsPrimaryName' in field_content:
                    maxlength = '<MaxLength>100</MaxLength>\n          '
                else:
                    maxlength = f'<MaxLength>{length_value}</MaxLength>\n          '

                # Insert MaxLength after Length
                field_content = re.sub(
                    r'(<Length>\d+</Length>)\s*\n',
                    r'\1\n          ' + maxlength,
                    field_content
                )
                print(f"    Also added MaxLength")

        # Insert API attributes before IntroducedVersion
        new_field_content = re.sub(
            r'(\s*)(<IntroducedVersion>)',
            r'\n          ' + api_attrs + r'\n          \2',
            field_content
        )

        # Replace in content
        content = content.replace(field_content, new_field_content)

    if fields_updated:
        with open(entity_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Updated {entity} ({len(fields_updated)} fields)")
    else:
        print(f"  - No updates needed")

print("\n✓ All custom fields fixed")
