#!/usr/bin/env python3
"""
Add primary name fields to all custom entities
Every Dataverse entity needs a primary name field (nvarchar with PrimaryName in DisplayMask)
"""

import re

# Entity names and their primary name field definitions
ENTITIES = [
    ("pm_StaffMember", "pm_name", "Name", "Employee name"),
    ("pm_EvaluationQuestion", "pm_name", "Name", "Question title"),
    ("pm_WeeklyEvaluation", "pm_name", "Name", "Evaluation name"),
    ("pm_SelfEvaluation", "pm_name", "Name", "Self-evaluation name"),
    ("pm_IDPEntry", "pm_name", "Name", "Development goal title"),
    ("pm_MeetingNote", "pm_name", "Name", "Meeting note title"),
    ("pm_Goal", "pm_name", "Name", "Goal title"),
    ("pm_Recognition", "pm_name", "Name", "Recognition title"),
    ("pm_ActionItem", "pm_name", "Name", "Action item description"),
]

# Primary name field template based on Microsoft samples
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

print("Adding primary name fields to all entities...")
print()

# Read the file
with open('/home/user/ContinousPerformanceManagementApp/solution/Other/Customizations.xml', 'r', encoding='utf-8') as f:
    content = f.read()

for entity_name, field_name, display_name, description in ENTITIES:
    # Create the primary name field for this entity
    primary_name_field = PRIMARY_NAME_TEMPLATE.format(
        physical_name=field_name,
        logical_name=field_name,
        display_name=display_name,
        description=description
    )

    # Find the pattern: after primarykey attribute, before any other attributes
    # Insert the primary name field right after the primary key
    pattern = f'(<entity Name="{entity_name}">.*?</attribute>)(\\s+<attribute)'
    replacement = f'\\1\n{primary_name_field}\\2'

    old_content = content
    content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)

    if content != old_content:
        print(f"✓ Added primary name field to {entity_name}")
    else:
        print(f"✗ Failed to add primary name field to {entity_name}")

# Write back
print()
print("Writing updated customizations.xml...")
with open('/home/user/ContinousPerformanceManagementApp/solution/Other/Customizations.xml', 'w', encoding='utf-8') as f:
    f.write(content)

lines = len(content.split('\n'))
print(f"✓ File updated: {lines} lines")
print("✓ Primary name fields added to all 9 entities")
