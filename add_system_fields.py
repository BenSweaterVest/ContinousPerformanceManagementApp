#!/usr/bin/env python3
"""
Add required Dataverse system fields to all Entity.xml files.
These fields are present in all Microsoft-exported solutions.
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path

# Define the system fields template based on Microsoft's Boards solution
SYSTEM_FIELDS_TEMPLATE = '''
        <!-- Standard Dataverse System Fields -->
        <attribute PhysicalName="CreatedBy">
          <Type>lookup</Type>
          <Name>createdby</Name>
          <LogicalName>createdby</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>0</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>0</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>0</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <LookupStyle>single</LookupStyle>
          <LookupTypes />
          <displaynames>
            <displayname description="Created By" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Unique identifier of the user who created the record." languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="CreatedOn">
          <Type>datetime</Type>
          <Name>createdon</Name>
          <LogicalName>createdon</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>0</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>0</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>0</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <Format>datetime</Format>
          <Behavior>1</Behavior>
          <displaynames>
            <displayname description="Created On" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Date and time when the record was created." languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="CreatedOnBehalfBy">
          <Type>lookup</Type>
          <Name>createdonbehalfby</Name>
          <LogicalName>createdonbehalfby</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>0</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>0</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>0</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <LookupStyle>single</LookupStyle>
          <LookupTypes />
          <displaynames>
            <displayname description="Created By (Delegate)" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Unique identifier of the delegate user who created the record." languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="ImportSequenceNumber">
          <Type>int</Type>
          <Name>importsequencenumber</Name>
          <LogicalName>importsequencenumber</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>1</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>0</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>1</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <MinValue>-2147483648</MinValue>
          <MaxValue>2147483647</MaxValue>
          <displaynames>
            <displayname description="Import Sequence Number" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Sequence number of the import that created this record." languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="ModifiedBy">
          <Type>lookup</Type>
          <Name>modifiedby</Name>
          <LogicalName>modifiedby</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>0</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>0</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>0</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <LookupStyle>single</LookupStyle>
          <LookupTypes />
          <displaynames>
            <displayname description="Modified By" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Unique identifier of the user who modified the record." languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="ModifiedOn">
          <Type>datetime</Type>
          <Name>modifiedon</Name>
          <LogicalName>modifiedon</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>0</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>0</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>0</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <Format>datetime</Format>
          <Behavior>1</Behavior>
          <displaynames>
            <displayname description="Modified On" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Date and time when the record was modified." languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="ModifiedOnBehalfBy">
          <Type>lookup</Type>
          <Name>modifiedonbehalfby</Name>
          <LogicalName>modifiedonbehalfby</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>0</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>0</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>0</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <LookupStyle>single</LookupStyle>
          <LookupTypes />
          <displaynames>
            <displayname description="Modified By (Delegate)" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Unique identifier of the delegate user who modified the record." languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="OverriddenCreatedOn">
          <Type>datetime</Type>
          <Name>overriddencreatedon</Name>
          <LogicalName>overriddencreatedon</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>1</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>0</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>1</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <Format>datetime</Format>
          <Behavior>1</Behavior>
          <displaynames>
            <displayname description="Record Created On" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Date and time that the record was migrated." languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="OwnerId">
          <Type>owner</Type>
          <Name>ownerid</Name>
          <LogicalName>ownerid</LogicalName>
          <RequiredLevel>systemrequired</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>1</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>1</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>0</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <LookupStyle>single</LookupStyle>
          <LookupTypes />
          <displaynames>
            <displayname description="Owner" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Owner Id" languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="OwningBusinessUnit">
          <Type>lookup</Type>
          <Name>owningbusinessunit</Name>
          <LogicalName>owningbusinessunit</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>0</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>0</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>0</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <LookupStyle>single</LookupStyle>
          <LookupTypes />
          <displaynames>
            <displayname description="Owning Business Unit" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Unique identifier for the business unit that owns the record" languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="OwningTeam">
          <Type>lookup</Type>
          <Name>owningteam</Name>
          <LogicalName>owningteam</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>0</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>0</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>0</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <LookupStyle>single</LookupStyle>
          <LookupTypes />
          <displaynames>
            <displayname description="Owning Team" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Unique identifier for the team that owns the record." languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="OwningUser">
          <Type>lookup</Type>
          <Name>owninguser</Name>
          <LogicalName>owninguser</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>0</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>0</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>0</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <LookupStyle>single</LookupStyle>
          <LookupTypes />
          <displaynames>
            <displayname description="Owning User" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Unique identifier for the user that owns the record." languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="statecode">
          <Type>state</Type>
          <Name>statecode</Name>
          <LogicalName>statecode</LogicalName>
          <RequiredLevel>systemrequired</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>0</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>1</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>0</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <displaynames>
            <displayname description="Status" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Status of the record" languagecode="1033" />
          </Descriptions>
          <optionset Name="ENTITY_NAME_statecode">
            <OptionSetType>state</OptionSetType>
            <IntroducedVersion>1.0.0.0</IntroducedVersion>
            <IsCustomizable>1</IsCustomizable>
            <IsGlobal>0</IsGlobal>
            <options>
              <option value="0" defaultstatus="1">
                <labels>
                  <label description="Active" languagecode="1033" />
                </labels>
              </option>
              <option value="1" defaultstatus="2">
                <labels>
                  <label description="Inactive" languagecode="1033" />
                </labels>
              </option>
            </options>
          </optionset>
        </attribute>
        <attribute PhysicalName="statuscode">
          <Type>status</Type>
          <Name>statuscode</Name>
          <LogicalName>statuscode</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>1</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>1</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>0</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <displaynames>
            <displayname description="Status Reason" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Reason for the status of the record" languagecode="1033" />
          </Descriptions>
          <optionset Name="ENTITY_NAME_statuscode">
            <OptionSetType>status</OptionSetType>
            <IntroducedVersion>1.0.0.0</IntroducedVersion>
            <IsCustomizable>1</IsCustomizable>
            <IsGlobal>0</IsGlobal>
            <options>
              <option value="1" state="0">
                <labels>
                  <label description="Active" languagecode="1033" />
                </labels>
              </option>
              <option value="2" state="1">
                <labels>
                  <label description="Inactive" languagecode="1033" />
                </labels>
              </option>
            </options>
          </optionset>
        </attribute>
        <attribute PhysicalName="TimeZoneRuleVersionNumber">
          <Type>int</Type>
          <Name>timezoneruleversionnumber</Name>
          <LogicalName>timezoneruleversionnumber</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>1</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>1</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>1</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <MinValue>-1</MinValue>
          <MaxValue>2147483647</MaxValue>
          <displaynames>
            <displayname description="Time Zone Rule Version Number" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="For internal use only." languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="UTCConversionTimeZoneCode">
          <Type>int</Type>
          <Name>utcconversiontimezonecode</Name>
          <LogicalName>utcconversiontimezonecode</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>1</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>1</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>1</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <MinValue>-1</MinValue>
          <MaxValue>2147483647</MaxValue>
          <displaynames>
            <displayname description="UTC Conversion Time Zone Code" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Time zone code that was in use when the record was created." languagecode="1033" />
          </Descriptions>
        </attribute>
        <attribute PhysicalName="VersionNumber">
          <Type>bigint</Type>
          <Name>versionnumber</Name>
          <LogicalName>versionnumber</LogicalName>
          <RequiredLevel>none</RequiredLevel>
          <DisplayMask>ValidForAdvancedFind</DisplayMask>
          <IsValidForCreate>0</IsValidForCreate>
          <IsValidForRead>1</IsValidForRead>
          <IsValidForUpdate>0</IsValidForUpdate>
          <IsCustomField>0</IsCustomField>
          <IsAuditEnabled>1</IsAuditEnabled>
          <IsSecured>0</IsSecured>
          <IntroducedVersion>1.0.0.0</IntroducedVersion>
          <IsCustomizable>1</IsCustomizable>
          <IsRenameable>1</IsRenameable>
          <CanModifySearchSettings>1</CanModifySearchSettings>
          <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
          <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
          <MinValue>-9223372036854775808</MinValue>
          <MaxValue>9223372036854775807</MaxValue>
          <displaynames>
            <displayname description="Version Number" languagecode="1033" />
          </displaynames>
          <Descriptions>
            <Description description="Version Number" languagecode="1033" />
          </Descriptions>
        </attribute>
'''

def process_entity_file(filepath, entity_name):
    """Add system fields to an Entity.xml file"""

    print(f"Processing {entity_name}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if system fields are already added
    if 'PhysicalName="CreatedBy"' in content:
        print(f"  ✓ System fields already present in {entity_name}")
        return

    # Fix primary key type from uniqueidentifier to primarykey
    content = content.replace(
        f'<Type>uniqueidentifier</Type>\n          <Name>{entity_name}id</Name>',
        f'<Type>primarykey</Type>\n          <Name>{entity_name}id</Name>'
    )

    # Add system fields before the closing </attributes> tag
    # Replace ENTITY_NAME placeholder with actual entity name in optionsets
    system_fields = SYSTEM_FIELDS_TEMPLATE.replace('ENTITY_NAME', entity_name)

    content = content.replace(
        '      </attributes>',
        f'{system_fields}\n      </attributes>'
    )

    # Write back the modified content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✓ Added system fields to {entity_name}")

def main():
    """Process all Entity.xml files"""

    solution_path = Path('/home/user/ContinousPerformanceManagementApp/solution/Tables')

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

    for entity in entities:
        entity_file = solution_path / entity / 'Entity.xml'
        if entity_file.exists():
            process_entity_file(entity_file, entity)
        else:
            print(f"  ✗ File not found: {entity_file}")

    print("\n✓ All Entity.xml files have been updated with required system fields!")
    print("\nNext steps:")
    print("1. Run the pack-solution.ps1 script to create a new solution ZIP")
    print("2. Import the new solution into Dataverse for Teams")

if __name__ == '__main__':
    main()
