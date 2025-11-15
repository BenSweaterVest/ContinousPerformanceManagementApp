# Dataverse for Teams Solution - Complete Checklist

**Version**: 2.0
**Date**: November 15, 2025
**Purpose**: Master reference for creating hand-written Dataverse for Teams solutions

This document provides everything a future Claude Code instance needs to create a properly formatted, importable Dataverse for Teams solution from scratch.

---

## Table of Contents
1. [Quick Start Guide](#quick-start-guide)
2. [File Structure](#file-structure)
3. [XML Structure & Formatting](#xml-structure--formatting)
4. [Entity Metadata Requirements](#entity-metadata-requirements)
5. [Attribute Metadata Requirements](#attribute-metadata-requirements)
6. [Relationship Requirements](#relationship-requirements)
7. [Common Pitfalls](#common-pitfalls)
8. [Validation Checklist](#validation-checklist)

---

## Quick Start Guide

### Recommended Approach

**DON'T** hand-write solutions if you can avoid it. Instead:

1. **Create entities in Power Apps UI** → Export solution → Use as template
2. **Use Power Platform CLI** (`pac solution init`, `pac data create-entity`)
3. **Only hand-write** if absolutely necessary (template apps, learning, etc.)

### If You Must Hand-Write

Follow these steps:

1. Use Microsoft's exported solution as a reference (e.g., Boards solution)
2. Start with our working template in this repository
3. Follow this checklist exactly
4. Test import frequently (after each entity)
5. Compare your XML with Microsoft's if errors occur

---

## File Structure

### Directory Layout

```
solution/
├── Other/
│   ├── Customizations.xml     (main entity definitions)
│   └── Solution.xml            (solution manifest)
├── Tables/                     (optional - pac CLI uses this)
│   └── {entity_name}/
│       └── Entity.xml
├── Workflows/                  (optional - for cloud flows)
│   └── *.json
└── CanvasApps/                 (optional - for canvas apps)
    └── README.md
```

### Key Files

**Customizations.xml**: Contains all entity, attribute, and relationship definitions
**Solution.xml**: Solution manifest with publisher and version info

---

## XML Structure & Formatting

### Critical Formatting Rules

#### ✅ XML Declaration
```xml
<?xml version="1.0" encoding="utf-8"?>
```
- **MUST** use double quotes (not single quotes!)
- encoding must be "utf-8"

#### ✅ Root Element
```xml
<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
```
- Include the xmlns:xsi namespace

#### ✅ Section Order (EXACT order required)
```xml
<ImportExportXml>
  <Entities>
    <!-- All entity definitions -->
  </Entities>
  <Roles />
  <Workflows />
  <FieldSecurityProfiles />
  <Templates />
  <EntityImageConfigs />
  <AttributeImageConfigs />
  <EntityMaps />
  <EntityRelationships>
    <!-- All relationship definitions -->
  </EntityRelationships>
  <OrganizationSettings />
  <optionsets />
  <CustomControls />
  <SolutionPluginAssemblies />
  <EntityDataProviders />
  <Languages>
    <Language>1033</Language>
  </Languages>
</ImportExportXml>
```

### Element Formatting Rules

#### ✅ AutoNumberFormat
```xml
<!-- CORRECT -->
<AutoNumberFormat></AutoNumberFormat>

<!-- WRONG -->
<AutoNumberFormat />
```
Use explicit opening/closing tags, not self-closing.

#### ✅ Boolean Values
```xml
<IsCustomizable>1</IsCustomizable>
<IsAuditEnabled>0</IsAuditEnabled>
```
Use "1" and "0", NOT "true" and "false"

---

## Entity Metadata Requirements

### Entity Name Format

**CRITICAL**: Entity names use PascalCase in Customizations.xml:

```xml
<!-- CORRECT: PascalCase based on display name -->
<entity Name="pm_StaffMember">
<entity Name="pm_EvaluationQuestion">
<entity Name="pm_WeeklyEvaluation">

<!-- WRONG: all lowercase -->
<entity Name="pm_staffmember">
```

**Pattern**: `{prefix}_{DisplayNameInPascalCase}`
- "Staff Member" → `pm_StaffMember`
- "Evaluation Question" → `pm_EvaluationQuestion`
- "IDP Entry" → `pm_IDPEntry`

**Note**: Solution.xml uses lowercase:
```xml
<RootComponent type="1" schemaName="pm_staffmember" behavior="0" />
```

### Entity Element Structure

Microsoft's minimal format (recommended):

```xml
<entity Name="pm_StaffMember">
  <LocalizedNames>
    <LocalizedName description="Staff Member" languagecode="1033" />
  </LocalizedNames>
  <LocalizedCollectionNames>
    <LocalizedCollectionName description="Staff Members" languagecode="1033" />
  </LocalizedCollectionNames>
  <Descriptions>
    <Description description="Store information about staff members" languagecode="1033" />
  </Descriptions>
  <attributes>
    <!-- All attribute definitions -->
  </attributes>
  <EntitySetName>pm_staffmembers</EntitySetName>
  <OwnershipTypeMask>16</OwnershipTypeMask>
  <IsCustomizable>1</IsCustomizable>
  <!-- ... other child elements as needed -->
</entity>
```

**DO NOT** include metadata as attributes on the entity element itself (this is pac CLI specific).

### Required System Fields

**Every** UserOwned entity MUST have these 17 system fields:

1. **Primary Key** (e.g., `pm_staffmemberid`) - Type: primarykey
2. **Primary Name** (e.g., `pm_name`) - Type: nvarchar
3. **createdby** - Type: lookup → SystemUser
4. **createdon** - Type: datetime
5. **createdonbehalfby** - Type: lookup → SystemUser
6. **modifiedby** - Type: lookup → SystemUser
7. **modifiedon** - Type: datetime
8. **modifiedonbehalfby** - Type: lookup → SystemUser
9. **ownerid** - Type: owner
10. **owningbusinessunit** - Type: lookup → BusinessUnit
11. **owningteam** - Type: lookup → Team
12. **owninguser** - Type: lookup → SystemUser
13. **statecode** - Type: state (Active/Inactive)
14. **statuscode** - Type: status
15. **importsequencenumber** - Type: int
16. **overriddencreatedon** - Type: datetime
17. **timezoneruleversionnumber** - Type: int
18. **utcconversiontimezonecode** - Type: int
19. **versionnumber** - Type: bigint

---

## Attribute Metadata Requirements

### Attribute Element Structure

**EXACT element order** (critical for compatibility):

```xml
<attribute PhysicalName="FieldName">
  <Type>nvarchar</Type>
  <Name>fieldname</Name>
  <LogicalName>fieldname</LogicalName>
  <RequiredLevel>none|required|applicationrequired</RequiredLevel>
  <DisplayMask>ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>
  <ImeMode>auto</ImeMode>
  <ValidForUpdateApi>1</ValidForUpdateApi>
  <ValidForReadApi>1</ValidForReadApi>
  <ValidForCreateApi>1</ValidForCreateApi>
  <IsCustomField>0|1</IsCustomField>
  <IsAuditEnabled>0|1</IsAuditEnabled>
  <IsSecured>0</IsSecured>
  <IntroducedVersion>1.0|1.0.0.0</IntroducedVersion>
  <IsCustomizable>1</IsCustomizable>
  <IsRenameable>1</IsRenameable>
  <CanModifySearchSettings>1</CanModifySearchSettings>
  <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
  <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
  <SourceType>0</SourceType>
  <IsGlobalFilterEnabled>0</IsGlobalFilterEnabled>
  <IsSortableEnabled>0</IsSortableEnabled>
  <CanModifyGlobalFilterSettings>1</CanModifyGlobalFilterSettings>
  <CanModifyIsSortableSettings>1</CanModifyIsSortableSettings>
  <IsDataSourceSecret>0</IsDataSourceSecret>
  <AutoNumberFormat></AutoNumberFormat>
  <IsSearchable>0|1</IsSearchable>
  <IsFilterable>0|1</IsFilterable>
  <IsRetrievable>0|1</IsRetrievable>
  <IsLocalizable>0</IsLocalizable>
  <Format>text</Format>                  <!-- For nvarchar fields -->
  <MaxLength>100</MaxLength>              <!-- For nvarchar fields -->
  <Length>100</Length>                    <!-- For nvarchar fields -->
  <displaynames>
    <displayname description="Field Name" languagecode="1033" />
  </displaynames>
  <Descriptions>
    <Description description="Field description" languagecode="1033" />
  </Descriptions>
</attribute>
```

### IntroducedVersion Pattern

**CRITICAL**: Different versions for system vs. custom fields:

```xml
<!-- System fields (IsCustomField=0) -->
<IntroducedVersion>1.0</IntroducedVersion>

<!-- Custom fields (IsCustomField=1) -->
<IntroducedVersion>1.0.0.0</IntroducedVersion>
```

### Primary Key Field Requirements

```xml
<attribute PhysicalName="pm_StaffMemberId">
  <Type>primarykey</Type>
  <Name>pm_staffmemberid</Name>
  <LogicalName>pm_staffmemberid</LogicalName>
  <RequiredLevel>systemrequired</RequiredLevel>
  <DisplayMask>ValidForAdvancedFind|RequiredForGrid</DisplayMask>
  <ImeMode>auto</ImeMode>
  <ValidForUpdateApi>0</ValidForUpdateApi>
  <ValidForReadApi>1</ValidForReadApi>
  <ValidForCreateApi>1</ValidForCreateApi>
  <IsCustomField>0</IsCustomField>
  <IsAuditEnabled>0</IsAuditEnabled>
  <IsSecured>0</IsSecured>
  <IntroducedVersion>1.0</IntroducedVersion>  <!-- System field version -->
  <IsCustomizable>1</IsCustomizable>
  <IsRenameable>1</IsRenameable>
  <CanModifySearchSettings>1</CanModifySearchSettings>
  <CanModifyRequirementLevelSettings>0</CanModifyRequirementLevelSettings>
  <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
  <SourceType>0</SourceType>
  <IsGlobalFilterEnabled>0</IsGlobalFilterEnabled>
  <IsSortableEnabled>0</IsSortableEnabled>
  <CanModifyGlobalFilterSettings>1</CanModifyGlobalFilterSettings>
  <CanModifyIsSortableSettings>1</CanModifyIsSortableSettings>
  <IsDataSourceSecret>0</IsDataSourceSecret>
  <AutoNumberFormat></AutoNumberFormat>
  <IsSearchable>0</IsSearchable>
  <IsFilterable>1</IsFilterable>
  <IsRetrievable>1</IsRetrievable>
  <IsLocalizable>0</IsLocalizable>
  <displaynames>
    <displayname description="Staff Member ID" languagecode="1033" />
  </displaynames>
  <Descriptions>
    <Description description="Unique identifier" languagecode="1033" />
  </Descriptions>
</attribute>
```

**DO NOT** include:
- `<IsPrimaryId>1</IsPrimaryId>` (pac CLI artifact)
- `<MaxLength>100</MaxLength>` (not needed for primarykey)

### Primary Name Field Requirements

```xml
<attribute PhysicalName="pm_Name">
  <Type>nvarchar</Type>
  <Name>pm_name</Name>
  <LogicalName>pm_name</LogicalName>
  <RequiredLevel>required</RequiredLevel>
  <DisplayMask>PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid|RequiredForForm</DisplayMask>
  <ImeMode>auto</ImeMode>
  <ValidForUpdateApi>1</ValidForUpdateApi>
  <ValidForReadApi>1</ValidForReadApi>
  <ValidForCreateApi>1</ValidForCreateApi>
  <IsCustomField>1</IsCustomField>
  <IsAuditEnabled>1</IsAuditEnabled>
  <IsSecured>0</IsSecured>
  <IntroducedVersion>1.0.0.0</IntroducedVersion>  <!-- Custom field version -->
  <IsCustomizable>1</IsCustomizable>
  <IsRenameable>1</IsRenameable>
  <CanModifySearchSettings>1</CanModifySearchSettings>
  <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
  <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
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
  <Format>text</Format>
  <MaxLength>100</MaxLength>
  <Length>100</Length>
  <displaynames>
    <displayname description="Name" languagecode="1033" />
  </displaynames>
  <Descriptions>
    <Description description="Primary name field" languagecode="1033" />
  </Descriptions>
</attribute>
```

**Key requirements**:
- DisplayMask MUST include "PrimaryName" flag
- IsSearchable: 1 (searchable)
- Must have Format, MaxLength, and Length

**DO NOT** include:
- `<IsPrimaryName>1</IsPrimaryName>` (pac CLI artifact)

### System Field Patterns

#### System Lookup Fields (createdby, modifiedby, etc.)

```xml
<attribute PhysicalName="CreatedBy">
  <Type>lookup</Type>
  <Name>createdby</Name>
  <LogicalName>createdby</LogicalName>
  <RequiredLevel>none</RequiredLevel>
  <DisplayMask>ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>
  <ImeMode>auto</ImeMode>
  <ValidForUpdateApi>0</ValidForUpdateApi>
  <ValidForReadApi>1</ValidForReadApi>
  <ValidForCreateApi>0</ValidForCreateApi>
  <IsCustomField>0</IsCustomField>
  <IsAuditEnabled>0</IsAuditEnabled>
  <IsSecured>0</IsSecured>
  <IntroducedVersion>1.0</IntroducedVersion>
  <IsCustomizable>1</IsCustomizable>
  <IsRenameable>1</IsRenameable>
  <CanModifySearchSettings>1</CanModifySearchSettings>
  <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
  <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>
  <SourceType>0</SourceType>
  <IsGlobalFilterEnabled>0</IsGlobalFilterEnabled>
  <IsSortableEnabled>0</IsSortableEnabled>
  <CanModifyGlobalFilterSettings>1</CanModifyGlobalFilterSettings>
  <CanModifyIsSortableSettings>1</CanModifyIsSortableSettings>
  <IsDataSourceSecret>0</IsDataSourceSecret>
  <AutoNumberFormat></AutoNumberFormat>
  <IsSearchable>0</IsSearchable>
  <IsFilterable>0</IsFilterable>
  <IsRetrievable>0</IsRetrievable>
  <IsLocalizable>0</IsLocalizable>
  <LookupStyle>single</LookupStyle>
  <LookupTypes />
  <displaynames>
    <displayname description="Created By" languagecode="1033" />
  </displaynames>
  <Descriptions>
    <Description description="Unique identifier of the user who created the record" languagecode="1033" />
  </Descriptions>
</attribute>
```

**DO NOT** include in system fields:
- `<IsValidForCreate>`, `<IsValidForRead>`, `<IsValidForUpdate>` (use ValidFor*Api only)

---

## Relationship Requirements

### System Entity Relationships

**CRITICAL**: Every UserOwned entity MUST have 6 system relationships:

1. `business_unit_{entity}` → OwningBusinessUnit
2. `lk_{entity}_createdby` → CreatedBy
3. `lk_{entity}_modifiedby` → ModifiedBy
4. `owner_{entity}` → OwnerId
5. `team_{entity}` → OwningTeam
6. `user_{entity}` → OwningUser

### System Relationship Template

```xml
<EntityRelationship Name="business_unit_pm_staffmember">
  <EntityRelationshipType>OneToMany</EntityRelationshipType>
  <IsCustomizable>1</IsCustomizable>
  <IntroducedVersion>1.0</IntroducedVersion>
  <IsHierarchical>0</IsHierarchical>
  <ReferencingEntityName>pm_StaffMember</ReferencingEntityName>  <!-- PascalCase! -->
  <ReferencedEntityName>BusinessUnit</ReferencedEntityName>
  <CascadeAssign>NoCascade</CascadeAssign>
  <CascadeDelete>NoCascade</CascadeDelete>
  <CascadeReparent>NoCascade</CascadeReparent>
  <CascadeShare>NoCascade</CascadeShare>
  <CascadeUnshare>NoCascade</CascadeUnshare>
  <ReferencingAttributeName>OwningBusinessUnit</ReferencingAttributeName>
  <RelationshipDescription>
    <Descriptions>
      <Description description="Unique identifier for the business unit that owns the record" languagecode="1033" />
    </Descriptions>
  </RelationshipDescription>
</EntityRelationship>
```

**Key Points**:
- ReferencingEntityName MUST use PascalCase (pm_StaffMember, not pm_staffmember)
- IntroducedVersion: "1.0" for system relationships
- All cascades: NoCascade
- NO EntityRelationshipRoles section for system relationships

### Custom Relationship Template

```xml
<EntityRelationship Name="pm_staffmember_pm_staffmember_pm_weeklyevaluation">
  <EntityRelationshipType>OneToMany</EntityRelationshipType>
  <IsCustomizable>1</IsCustomizable>
  <IntroducedVersion>1.0.0.0</IntroducedVersion>
  <IsHierarchical>0</IsHierarchical>
  <ReferencingEntityName>pm_WeeklyEvaluation</ReferencingEntityName>
  <ReferencedEntityName>pm_StaffMember</ReferencedEntityName>
  <CascadeAssign>NoCascade</CascadeAssign>
  <CascadeDelete>RemoveLink</CascadeDelete>
  <CascadeReparent>NoCascade</CascadeReparent>
  <CascadeShare>NoCascade</CascadeShare>
  <CascadeUnshare>NoCascade</CascadeUnshare>
  <CascadeRollupView>NoCascade</CascadeRollupView>
  <IsValidForAdvancedFind>1</IsValidForAdvancedFind>
  <ReferencingAttributeName>pm_staffmember</ReferencingAttributeName>
  <RelationshipDescription>
    <Descriptions>
      <Description description="Staffmember to Weeklyevaluation relationship" languagecode="1033" />
    </Descriptions>
  </RelationshipDescription>
  <EntityRelationshipRoles>
    <EntityRelationshipRole>
      <NavPaneDisplayOption>UseCollectionName</NavPaneDisplayOption>
      <NavPaneArea>Details</NavPaneArea>
      <NavPaneOrder>10000</NavPaneOrder>
      <NavigationPropertyName>pm_staffmember</NavigationPropertyName>
      <RelationshipRoleType>1</RelationshipRoleType>
    </EntityRelationshipRole>
    <EntityRelationshipRole>
      <NavigationPropertyName>pm_staffmember_pm_staffmember_pm_weeklyevaluation</NavigationPropertyName>
      <RelationshipRoleType>0</RelationshipRoleType>
    </EntityRelationshipRole>
  </EntityRelationshipRoles>
</EntityRelationship>
```

**Differences from system relationships**:
- IntroducedVersion: "1.0.0.0" (custom)
- Includes CascadeRollupView
- Includes IsValidForAdvancedFind
- Includes EntityRelationshipRoles section

---

## Common Pitfalls

### ❌ AVOID THESE MISTAKES

1. **Using lowercase entity names** in Customizations.xml
   - ❌ `<entity Name="pm_staffmember">`
   - ✅ `<entity Name="pm_StaffMember">`

2. **Single quotes in XML declaration**
   - ❌ `<?xml version='1.0' encoding='utf-8'?>`
   - ✅ `<?xml version="1.0" encoding="utf-8"?>`

3. **Self-closing AutoNumberFormat tags**
   - ❌ `<AutoNumberFormat />`
   - ✅ `<AutoNumberFormat></AutoNumberFormat>`

4. **Including pac CLI artifacts**
   - ❌ `<IsPrimaryId>1</IsPrimaryId>`
   - ❌ `<IsPrimaryName>1</IsPrimaryName>`
   - ✅ Remove these attributes entirely

5. **Wrong IntroducedVersion**
   - ❌ System field with `<IntroducedVersion>1.0.0.0</IntroducedVersion>`
   - ✅ System field with `<IntroducedVersion>1.0</IntroducedVersion>`

6. **Missing PrimaryName in DisplayMask**
   - ❌ `<DisplayMask>ValidForAdvancedFind</DisplayMask>` (for primary name)
   - ✅ `<DisplayMask>PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>`

7. **Missing system relationships**
   - ❌ Only custom relationships defined
   - ✅ 6 system relationships + custom relationships

8. **Malformed XML nesting**
   - ❌ `<CanModifyAdditionalSettings>1<SourceType>0</SourceType>...</CanModifyAdditionalSettings>`
   - ✅ `<CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>\n<SourceType>0</SourceType>`

9. **Wrong DisplayMask for system fields**
   - ❌ `<DisplayMask>ValidForAdvancedFind</DisplayMask>` (for createdby)
   - ✅ `<DisplayMask>ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>`

10. **Mixing IsValidFor* and ValidFor*Api in system fields**
    - ❌ Having both IsValidForCreate AND ValidForCreateApi
    - ✅ Use only ValidFor*Api for system fields

---

## Validation Checklist

Use this checklist before attempting to import:

### File Structure
- [ ] Customizations.xml exists in solution/Other/
- [ ] Solution.xml exists in solution/Other/
- [ ] XML files are UTF-8 encoded
- [ ] No BOM (Byte Order Mark) in files

### XML Format
- [ ] XML declaration uses double quotes
- [ ] All sections present in correct order
- [ ] AutoNumberFormat uses explicit tags (not self-closing)
- [ ] Boolean values use "0" and "1" (not true/false)

### Entity Names
- [ ] Entity Name attributes use PascalCase (pm_StaffMember)
- [ ] Solution.xml schemaName uses lowercase (pm_staffmember)
- [ ] ReferencingEntityName in relationships uses PascalCase

### Every Entity Has
- [ ] 17+ system fields (createdby, modifiedby, ownerid, etc.)
- [ ] Primary key field (Type: primarykey)
- [ ] Primary name field with PrimaryName in DisplayMask
- [ ] 6 system relationships defined
- [ ] All custom relationships defined

### Attribute Metadata
- [ ] All attributes have 29+ metadata elements
- [ ] IntroducedVersion: "1.0" for system fields
- [ ] IntroducedVersion: "1.0.0.0" for custom fields
- [ ] No IsPrimaryId or IsPrimaryName attributes
- [ ] System fields use ValidFor*Api only (not IsValidFor*)
- [ ] Elements in correct order
- [ ] DisplayMask includes all necessary flags

### Relationships
- [ ] All relationships use PascalCase entity names
- [ ] System relationships use IntroducedVersion "1.0"
- [ ] Custom relationships use IntroducedVersion "1.0.0.0"
- [ ] Cascade settings appropriate for relationship type

### Final Checks
- [ ] XML is well-formed (no unclosed tags)
- [ ] File is under 100MB
- [ ] All entity names are consistent throughout
- [ ] Solution.xml version matches expected format

---

## Quick Reference: Field Type Templates

### String Field (nvarchar)
```xml
<Type>nvarchar</Type>
<Format>text</Format>
<MaxLength>100</MaxLength>
<Length>100</Length>
```

### Memo Field
```xml
<Type>memo</Type>
<MaxLength>4000</MaxLength>
<IsLocalizable>0</IsLocalizable>
```

### Integer Field
```xml
<Type>int</Type>
<MinValue>-2147483648</MinValue>
<MaxValue>2147483647</MaxValue>
```

### Decimal Field
```xml
<Type>decimal</Type>
<Precision>10</Precision>
<MinValue>-100000000000</MinValue>
<MaxValue>100000000000</MaxValue>
<ImeMode>disabled</ImeMode>
```

### DateTime Field
```xml
<Type>datetime</Type>
<Format>DateOnly|DateAndTime</Format>
<ImeMode>inactive</ImeMode>
<DateTimeBehavior>UserLocal|DateOnly|TimeZoneIndependent</DateTimeBehavior>
```

### Boolean Field
```xml
<Type>bit</Type>
<OptionSet localizedName="Yes/No">
  <IsGlobal>0</IsGlobal>
  <options>
    <option value="1"><labels><label description="Yes" languagecode="1033" /></labels></option>
    <option value="0"><labels><label description="No" languagecode="1033" /></labels></option>
  </options>
</OptionSet>
```

### Lookup Field
```xml
<Type>lookup</Type>
<LookupStyle>single</LookupStyle>
<LookupTypes><LookupType>pm_targetentity</LookupType></LookupTypes>
<Targets>
  <Target>pm_targetentity</Target>
</Targets>
```

---

## Scripts Available

This repository includes automated scripts to fix common issues:

1. `fix_introduced_version.py` - Fix IntroducedVersion for system fields
2. `add_missing_attribute_metadata.py` - Add missing metadata elements
3. `fix_display_mask.py` - Fix DisplayMask values for system fields
4. `fix_entity_name_casing.py` - Convert entity names to PascalCase
5. `add_system_relationships.py` - Generate system relationships
6. `fix_malformed_xml.py` - Fix malformed XML structures
7. `final_alignment_fixes.py` - Apply final formatting fixes

---

## Success Criteria

Your solution is ready to import when:

✅ XML validates without errors
✅ All entities have PascalCase names
✅ All 17 system fields present in each entity
✅ All 6 system relationships present per entity
✅ IntroducedVersion follows system vs. custom pattern
✅ No pac CLI artifacts (IsPrimaryId, IsPrimaryName)
✅ AutoNumberFormat uses explicit tags
✅ XML declaration uses double quotes
✅ All attribute metadata elements present

---

## Resources

- Microsoft Boards Reference: `ref/boards_unpacked/`
- Troubleshooting Guide: `ref/IMPORT-TROUBLESHOOTING-GUIDE.md`
- Microsoft Comparison: `ref/MSFT-BOARDS-COMPARISON.md`
- Error Solutions: `ERROR_8_SOLUTION_SUMMARY.md`, `ERROR_9_SOLUTION_SUMMARY.md`

---

**Last Updated**: November 15, 2025
**Status**: Complete and tested on Teams Dataverse
**Errors Documented**: 9 (all solved)
**Success Rate**: Working solution after following all corrections
