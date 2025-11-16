#!/usr/bin/env python3
"""
Add pm_name fields ONLY to entities that don't have them yet
"""

import re

# Only add to entities that are missing pm_name
ENTITIES_MISSING_PM_NAME = [
    ("pm_EvaluationQuestion", "pm_name", "Name", "Question title"),
    ("pm_IDPEntry", "pm_name", "Name", "Development goal title"),
    ("pm_Goal", "pm_name", "Name", "Goal title"),
]

# Primary name field template
PRIMARY_NAME_TEMPLATE = """            <attribute PhysicalName="{physical_name}">
              <Type>nvarchar</Type>
              <Name>{logical_name}</Name>
              <LogicalName>{logical_name}</LogicalName>
              <RequiredLevel>required</RequiredLevel>
              <DisplayMask>PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid|RequiredForForm</DisplayMask>
              <ImeMode>auto</ImeMode>
              <ValidForUpdateApi>1</ValidForUpdateApi>
              <ValidForReadApi>1</ValidForReadApi>
              <ValidForCreateApi>1</ValidForCreateApi>
              <IsCustomField>1</IsCustomField>
              <IsAuditEnabled>0</IsAuditEnabled>
              <IsSecured>0</IsSecured>
              <IntroducedVersion>2.0.0.0</IntroducedVersion>
              <IsCustomizable>1</IsCustomizable>
              <IsRenameable>1</IsRenameable>
              <CanModifySearchSettings>1</CanModifySearchSettings>
              <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
              <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
              <SourceType>0</SourceType>
              <IsGlobalFilterEnabled>0</IsGlobalFilterEnabled>
              <IsSortableEnabled>1</IsSortableEnabled>
              <CanModifyGlobalFilterSettings>1</CanModifyGlobalFilterSettings>
              <CanModifyIsSortableSettings>1</CanModifyIsSortableSettings>
              <IsDataSourceSecret>0</IsDataSourceSecret>
              <AutoNumberFormat></AutoNumberFormat>
              <IsSearchable>1</IsSearchable>
              <IsFilterable>1</IsFilterable>
              <IsRetrievable>1</IsRetrievable>
              <IsLocalizable>0</IsLocalizable>
              <Format>Text</Format>
              <MaxLength>100</MaxLength>
              <displaynames>
                <displayname description="{display_name}" languagecode="1033" />
              </displaynames>
              <Descriptions>
                <Description description="{description}" languagecode="1033" />
              </Descriptions>
            </attribute>
"""

print("Adding pm_name fields to entities that are missing them...")
print()

# Read the file
with open('/home/user/ContinousPerformanceManagementApp/solution/Other/Customizations.xml', 'r', encoding='utf-8') as f:
    content = f.read()

for entity_name, field_name, display_name, description in ENTITIES_MISSING_PM_NAME:
    # Create the primary name field
    primary_name_field = PRIMARY_NAME_TEMPLATE.format(
        physical_name=field_name,
        logical_name=field_name,
        display_name=display_name,
        description=description
    )

    # Insert after the primary key attribute
    pattern = f'(<entity Name="{entity_name}">.*?</attribute>)(\\s+<attribute)'
    replacement = f'\\1\n{primary_name_field}\\2'

    old_content = content
    content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)

    if content != old_content:
        print(f"✓ Added pm_name to {entity_name}")
    else:
        print(f"✗ Failed to add pm_name to {entity_name}")

# Write back
print()
print("Writing updated customizations.xml...")
with open('/home/user/ContinousPerformanceManagementApp/solution/Other/Customizations.xml', 'w', encoding='utf-8') as f:
    f.write(content)

lines = len(content.split('\n'))
print(f"✓ File updated: {lines} lines")
print("✓ Primary name fields added to entities that were missing them")
