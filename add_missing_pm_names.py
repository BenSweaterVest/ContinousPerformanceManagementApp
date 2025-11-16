#!/usr/bin/env python3
"""
Add pm_name primary name fields ONLY to entities that don't have them
"""

import re

# Primary name field template (NO Format element for Teams compatibility)
PRIMARY_NAME_TEMPLATE = """            <attribute PhysicalName="pm_name">
              <Type>nvarchar</Type>
              <Name>pm_name</Name>
              <LogicalName>pm_name</LogicalName>
              <RequiredLevel>required</RequiredLevel>
              <DisplayMask>PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid|RequiredForForm</DisplayMask>
              <MaxLength>100</MaxLength>
              <Length>100</Length>
              <ImeMode>auto</ImeMode>
              <ValidForUpdateApi>1</ValidForUpdateApi>
              <ValidForReadApi>1</ValidForReadApi>
              <ValidForCreateApi>1</ValidForCreateApi>
              <IsCustomField>1</IsCustomField>
              <IsAuditEnabled>0</IsAuditEnabled>
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
              <IntroducedVersion>2.0.0.0</IntroducedVersion>
              <IsCustomizable>1</IsCustomizable>
              <IsRenameable>1</IsRenameable>
              <CanModifySearchSettings>1</CanModifySearchSettings>
              <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
              <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
              <displaynames>
                <displayname description="Name" languagecode="1033" />
              </displaynames>
              <Descriptions>
                <Description description="Primary name field" languagecode="1033" />
              </Descriptions>
            </attribute>"""

# Entities that need pm_name added
entities_needing_pm_name = [
    'pm_EvaluationQuestion',
    'pm_IDPEntry',
    'pm_Goal'
]

# Read the file
with open('solution/Other/Customizations.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# Process each entity
for entity_name in entities_needing_pm_name:
    # Find the entity's primary key field and insert pm_name after it
    # Pattern: find the entity's attributes section and the first closing </attribute> tag
    pattern = rf'(<entity Name="{entity_name}">.*?<attributes>.*?</attribute>)'

    def add_pm_name(match):
        return match.group(1) + '\n' + PRIMARY_NAME_TEMPLATE

    content = re.sub(pattern, add_pm_name, content, flags=re.DOTALL)
    print(f"Added pm_name to {entity_name}")

# Write back
with open('solution/Other/Customizations.xml', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nVerification:")
pm_name_count = content.count('PhysicalName="pm_name"')
print(f"Total pm_name fields: {pm_name_count}")

for entity_name in ['pm_StaffMember', 'pm_EvaluationQuestion', 'pm_WeeklyEvaluation', 'pm_SelfEvaluation',
                     'pm_IDPEntry', 'pm_MeetingNote', 'pm_Goal', 'pm_Recognition', 'pm_ActionItem']:
    entity_section = re.search(rf'<entity Name="{entity_name}">.*?</entity>', content, re.DOTALL)
    if entity_section:
        has_pm_name = 'PhysicalName="pm_name"' in entity_section.group(0)
        print(f"  {entity_name}: {'✓' if has_pm_name else '✗'}")
