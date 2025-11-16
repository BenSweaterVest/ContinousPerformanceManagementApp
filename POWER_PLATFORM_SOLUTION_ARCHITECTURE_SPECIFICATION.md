# Power Platform Solution Architecture Specification

**Document Version:** 1.0
**Created:** 2025-11-16
**Purpose:** Comprehensive architectural specification for creating Power Platform solutions for Microsoft Teams (Dataverse for Teams)
**Based on Analysis of:** 6 Microsoft Official Sample Solutions

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Solution Package Structure](#solution-package-structure)
3. [Core Files Reference](#core-files-reference)
4. [Entity Architecture](#entity-architecture)
5. [Attribute Types & Metadata](#attribute-types--metadata)
6. [Relationship Patterns](#relationship-patterns)
7. [Canvas App Structure](#canvas-app-structure)
8. [Formula/Workflow Patterns](#formulaworkflow-patterns)
9. [Root Component Types](#root-component-types)
10. [Publisher Configuration](#publisher-configuration)
11. [Version Management](#version-management)
12. [Import/Export Considerations](#importexport-considerations)
13. [Appendix: Complete Checklists](#appendix-complete-checklists)

---

## Executive Summary

This specification documents the exact architecture, structure, and metadata requirements for creating Power Platform solutions that can be successfully imported into Microsoft Teams (Dataverse for Teams) environments.

### Key Findings from Microsoft Solutions Analysis

**Solutions Analyzed:**
- MSFT_AreaInspection (Area Inspection) - v1.0.812.4
- MSFT_EmployeeIdeas (Employee Ideas) - v1.0.548.3
- MSFT_CommsCenter (Bulletins) - v1.0.560.3
- MSFT_GetConnected (Get Connected) - v1.0.548.2
- MSFT_HowTo (How To) - v1.0.548.2
- MSFT_Boards (Boards) - v1.0.x.x

**Common Patterns Discovered:**
- All managed solutions use `Managed="1"`
- Publisher prefix: `msft` (for Teams apps) or `msdyn` (for Dynamics 365)
- CustomizationOptionValuePrefix: 29960 (msft) or 19235 (msdyn)
- Version format: `Major.Minor.Build.Revision` (e.g., 1.0.812.4)
- Entity names use **PascalCase** in customizations.xml
- Schema names use **lowercase** in solution.xml
- All entities include extensive metadata (30+ attributes per entity)
- System relationships required: 6 per UserOwned entity

---

## Solution Package Structure

### Physical File Organization

A packed Power Platform solution (.zip file) contains the following structure:

```
SolutionName.zip
├── [Content_Types].xml           # MIME type definitions
├── solution.xml                   # Solution manifest
├── customizations.xml             # COMPLETE entity definitions (embedded)
├── CanvasApps/                    # Power Apps canvas applications
│   ├── appname_12345_DocumentUri.msapp        # App package (ZIP)
│   └── appname_12345_BackgroundImageUri       # App background image
├── Formulas/                      # Calculated columns (XAML workflows)
│   └── entity-fieldname.xaml
└── Other/                         # Additional resources (optional)
```

### Critical Structure Notes

1. **customizations.xml is EMBEDDED, not separated**
   - Microsoft solutions have ALL entity definitions in customizations.xml
   - Typical size: 360KB - 600KB (10,000 - 21,000 lines)
   - NO separate Tables/ folder with Entity.xml files in the final package

2. **Entity definitions must be complete**
   - Each entity fully defined within `<EntityInfo>` sections
   - All attributes, forms, views embedded
   - Relationships defined in `<EntityRelationships>` section

3. **Canvas apps are ZIP archives**
   - .msapp files are actually ZIP files containing app definition
   - Can be unpacked with standard ZIP tools
   - Contain app controls, resources, connections

---

## Core Files Reference

### 1. [Content_Types].xml

**Purpose:** Defines MIME types for all files in the solution package

**Standard Structure:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="xml" ContentType="application/octet-stream" />
  <Default Extension="xaml" ContentType="application/octet-stream" />
  <Default Extension="msapp" ContentType="application/octet-stream" />
  <Override PartName="/CanvasApps/appname_12345_BackgroundImageUri"
            ContentType="application/octet-stream" />
</Types>
```

**Requirements:**
- Must be UTF-8 encoded with BOM
- Must declare all file extensions used in package
- Override entries needed for binary files without extensions

---

### 2. solution.xml (Solution Manifest)

**Purpose:** Declares solution metadata, publisher, and root components

**Complete Template:**
```xml
<ImportExportXml version="9.2.22104.224"
                 SolutionPackageVersion="9.2"
                 languagecode="1033"
                 generatedBy="CrmLive"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <SolutionManifest>
    <UniqueName>YourSolutionName</UniqueName>
    <LocalizedNames>
      <LocalizedName description="Display Name" languagecode="1033" />
    </LocalizedNames>
    <Descriptions>
      <Description description="Solution description" languagecode="1033" />
    </Descriptions>
    <Version>1.0.0.0</Version>
    <Managed>0</Managed>  <!-- 0=Unmanaged, 1=Managed -->

    <Publisher>
      <UniqueName>yourpublisher</UniqueName>
      <LocalizedNames>
        <LocalizedName description="Your Publisher Name" languagecode="1033" />
      </LocalizedNames>
      <Descriptions>
        <Description description="Publisher description" languagecode="1033" />
      </Descriptions>
      <EMailAddress xsi:nil="true"></EMailAddress>
      <SupportingWebsiteUrl xsi:nil="true"></SupportingWebsiteUrl>
      <CustomizationPrefix>prefix</CustomizationPrefix>
      <CustomizationOptionValuePrefix>10000</CustomizationOptionValuePrefix>
      <Addresses>
        <Address>
          <AddressNumber>1</AddressNumber>
          <AddressTypeCode>1</AddressTypeCode>
          <!-- All address fields set to xsi:nil="true" -->
        </Address>
        <Address>
          <AddressNumber>2</AddressNumber>
          <AddressTypeCode>1</AddressTypeCode>
          <!-- All address fields set to xsi:nil="true" -->
        </Address>
      </Addresses>
    </Publisher>

    <RootComponents>
      <!-- Entities: type="1" -->
      <RootComponent type="1" schemaName="prefix_entityname" behavior="0" />

      <!-- Option Sets: type="9" -->
      <RootComponent type="9" schemaName="prefix_optionsetname" behavior="0" />

      <!-- Canvas Apps: type="300" -->
      <RootComponent type="300" schemaName="prefix_appname_12345" behavior="0" />

      <!-- File Columns: type="431" -->
      <RootComponent type="431" schemaName="prefix_entity prefix_fieldname" behavior="0" />

      <!-- Entity Images: type="432" -->
      <RootComponent type="432" schemaName="prefix_entityname" behavior="0" />
    </RootComponents>

    <MissingDependencies />
  </SolutionManifest>
</ImportExportXml>
```

**Key Attributes:**

| Attribute | Required | Typical Value | Notes |
|-----------|----------|---------------|-------|
| version | Yes | 9.2.22104.224 | Platform version |
| SolutionPackageVersion | Yes | 9.2 | Solution package format version |
| languagecode | Yes | 1033 | 1033 = English (US) |
| generatedBy | Yes | CrmLive | "CrmLive" for online, "CrmOnPremise" for on-prem |

**Publisher Prefixes:**
- Must be 3-8 characters
- Lowercase letters only
- Common patterns:
  - `msft` = Microsoft Teams apps (prefix 29960)
  - `msdyn` = Microsoft Dynamics 365 (prefix 19235)
  - Custom: Choose unique prefix (10000-99999)

**Root Component Types:**

| Type | Component | Example |
|------|-----------|---------|
| 1 | Entity | `<RootComponent type="1" schemaName="pm_staffmember" behavior="0" />` |
| 9 | Option Set (Global) | `<RootComponent type="9" schemaName="pm_statuscode" behavior="0" />` |
| 29 | Workflow | `<RootComponent type="29" schemaName="WorkflowName" behavior="0" />` |
| 300 | Canvas App | `<RootComponent type="300" schemaName="pm_app_a1b2c" behavior="0" />` |
| 431 | File Column | `<RootComponent type="431" schemaName="pm_entity pm_image" behavior="0" />` |
| 432 | Entity Image | `<RootComponent type="432" schemaName="pm_entityname" behavior="0" />` |

**Behavior Values:**
- `0` = Standard component
- `1` = Include as shell only (deprecated)
- `2` = Managed properties

---

### 3. customizations.xml (Entity Definitions)

**Purpose:** Contains COMPLETE definitions of all entities, attributes, forms, views, and relationships

**High-Level Structure:**
```xml
<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Entities>
    <Entity>
      <Name LocalizedName="Display Name" OriginalName="Display Name">prefix_EntityName</Name>
      <EntityInfo>
        <entity Name="prefix_EntityName">
          <!-- Entity metadata (30+ attributes) -->
          <LocalizedNames>...</LocalizedNames>
          <LocalizedCollectionNames>...</LocalizedCollectionNames>
          <Descriptions>...</Descriptions>

          <attributes>
            <!-- All entity attributes defined here -->
          </attributes>

          <EntityRelationships>
            <!-- All relationships defined here -->
          </EntityRelationships>
        </entity>

        <!-- Forms, Views, etc. can go here if needed -->
      </EntityInfo>
    </Entity>
    <!-- Repeat for each entity -->
  </Entities>

  <!-- Optional: EntityRelationships section for cross-entity relationships -->
  <EntityRelationships>
    <!-- Additional relationships if needed -->
  </EntityRelationships>

  <!-- Optional: optionsets section for global option sets -->
  <optionsets>
    <!-- Global option set definitions -->
  </optionsets>
</ImportExportXml>
```

**Size Expectations:**
- Simple app (1-2 entities): 2,000-5,000 lines
- Medium app (5-10 entities): 8,000-15,000 lines
- Complex app (10+ entities): 20,000+ lines

---

## Entity Architecture

### Entity Naming Conventions

**CRITICAL: Different casing in different locations**

| Location | Format | Example |
|----------|--------|---------|
| solution.xml `schemaName` | **lowercase** | `pm_staffmember` |
| customizations.xml `<Name>` | **PascalCase** | `pm_StaffMember` |
| customizations.xml `<entity Name>` | **PascalCase** | `pm_StaffMember` |
| Relationships `ReferencingEntityName` | **PascalCase** | `pm_StaffMember` |
| Relationships `ReferencedEntityName` | **PascalCase** | `pm_StaffMember` |
| Attribute names | **lowercase** | `pm_employeeid` |
| Logical names | **lowercase** | `pm_staffmemberid` |

**Pattern for PascalCase:**
- Based on display name
- "Staff Member" → `pm_StaffMember`
- "Evaluation Question" → `pm_EvaluationQuestion`
- "One On One Meeting" → `pm_OneOnOneMeeting`

### Complete Entity Template

```xml
<entity Name="prefix_EntityName">
  <LocalizedNames>
    <LocalizedName description="Display Name" languagecode="1033" />
  </LocalizedNames>
  <LocalizedCollectionNames>
    <LocalizedCollectionName description="Display Names" languagecode="1033" />
  </LocalizedCollectionNames>
  <Descriptions>
    <Description description="Entity description" languagecode="1033" />
  </Descriptions>

  <!-- REQUIRED ENTITY METADATA (30+ attributes) -->
  <ObjectTypeCode>0</ObjectTypeCode>
  <OwnershipType>UserOwned</OwnershipType>
  <EntitySetName>prefix_entitynames</EntitySetName>
  <IsActivity>0</IsActivity>
  <IsActivityParty>0</IsActivityParty>
  <IsAuditEnabled>1</IsAuditEnabled>
  <IsAvailableOffline>0</IsAvailableOffline>
  <IsBPFEntity>0</IsBPFEntity>
  <IsBusinessProcessEnabled>0</IsBusinessProcessEnabled>
  <IsChildEntity>0</IsChildEntity>
  <IsConnectionsEnabled>0</IsConnectionsEnabled>
  <IsCustomEntity>1</IsCustomEntity>
  <IsCustomizable>1</IsCustomizable>
  <IsDocumentManagementEnabled>0</IsDocumentManagementEnabled>
  <IsDocumentRecommendationsEnabled>0</IsDocumentRecommendationsEnabled>
  <IsDuplicateDetectionEnabled>0</IsDuplicateDetectionEnabled>
  <IsEnabledForCharts>0</IsEnabledForCharts>
  <IsEnabledForExternalChannels>0</IsEnabledForExternalChannels>
  <IsEnabledForTrace>0</IsEnabledForTrace>
  <IsImportable>1</IsImportable>
  <IsInteractionCentricEnabled>0</IsInteractionCentricEnabled>
  <IsIntersect>0</IsIntersect>
  <IsKnowledgeManagementEnabled>0</IsKnowledgeManagementEnabled>
  <IsMailMergeEnabled>0</IsMailMergeEnabled>
  <IsMappable>1</IsMappable>
  <IsOfflineInMobileClient>0</IsOfflineInMobileClient>
  <IsOneNoteIntegrationEnabled>0</IsOneNoteIntegrationEnabled>
  <IsOptimisticConcurrencyEnabled>1</IsOptimisticConcurrencyEnabled>
  <IsPrivate>0</IsPrivate>
  <IsQuickCreateEnabled>0</IsQuickCreateEnabled>
  <IsReadingPaneEnabled>1</IsReadingPaneEnabled>
  <IsReadOnlyInMobileClient>0</IsReadOnlyInMobileClient>
  <IsRenameable>1</IsRenameable>
  <IsSLAEnabled>0</IsSLAEnabled>
  <IsStateModelAware>1</IsStateModelAware>
  <IsValidForAdvancedFind>1</IsValidForAdvancedFind>
  <IsValidForQueue>0</IsValidForQueue>
  <IsVisibleInMobile>0</IsVisibleInMobile>
  <IsVisibleInMobileClient>1</IsVisibleInMobileClient>
  <CanEnableSyncToExternalSearchIndex>1</CanEnableSyncToExternalSearchIndex>
  <SyncToExternalSearchIndex>0</SyncToExternalSearchIndex>
  <ChangeTrackingEnabled>0</ChangeTrackingEnabled>
  <AutoRouteToOwnerQueue>0</AutoRouteToOwnerQueue>
  <EnforceStateTransitions>0</EnforceStateTransitions>
  <EntityHelpUrlEnabled>0</EntityHelpUrlEnabled>
  <EntityHelpUrl xsi:nil="true"></EntityHelpUrl>
  <IntroducedVersion>1.0.0.0</IntroducedVersion>
  <ReportViewName>Filteredprefix_EntityName</ReportViewName>

  <attributes>
    <!-- Attributes go here -->
  </attributes>

  <EntityRelationships>
    <!-- Relationships go here -->
  </EntityRelationships>
</entity>
```

### Required System Fields (All UserOwned Entities)

**Every UserOwned entity MUST have these 17+ system fields:**

#### 1. Primary Key Field
```xml
<attribute PhysicalName="prefix_EntityNameId">
  <Type>primarykey</Type>
  <Name>prefix_entitynameid</Name>
  <LogicalName>prefix_entitynameid</LogicalName>
  <RequiredLevel>systemrequired</RequiredLevel>
  <DisplayMask>ValidForAdvancedFind|RequiredForGrid</DisplayMask>
  <ImeMode>auto</ImeMode>
  <ValidForUpdateApi>0</ValidForUpdateApi>
  <ValidForReadApi>1</ValidForReadApi>
  <ValidForCreateApi>1</ValidForCreateApi>
  <IsCustomField>0</IsCustomField>
  <IsAuditEnabled>0</IsAuditEnabled>
  <IsSecured>0</IsSecured>
  <IntroducedVersion>1.0.0.0</IntroducedVersion>
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
  <IsPrimaryId>1</IsPrimaryId>
  <MaxLength>100</MaxLength>  <!-- CRITICAL for Teams compatibility -->
  <displaynames>
    <displayname description="Entity Name" languagecode="1033" />
  </displaynames>
  <Descriptions>
    <Description description="Unique identifier for entity instances" languagecode="1033" />
  </Descriptions>
</attribute>
```

#### 2. Primary Name Field
```xml
<attribute PhysicalName="prefix_Name">
  <Type>nvarchar</Type>
  <Name>prefix_name</Name>
  <LogicalName>prefix_name</LogicalName>
  <RequiredLevel>required</RequiredLevel>
  <DisplayMask>PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid|RequiredForForm</DisplayMask>
  <ImeMode>auto</ImeMode>
  <ValidForUpdateApi>1</ValidForUpdateApi>
  <ValidForReadApi>1</ValidForReadApi>
  <ValidForCreateApi>1</ValidForCreateApi>
  <IsCustomField>1</IsCustomField>
  <IsAuditEnabled>1</IsAuditEnabled>
  <IsSecured>0</IsSecured>
  <IntroducedVersion>1.0.0.0</IntroducedVersion>
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
  <IsPrimaryName>1</IsPrimaryName>
  <Format>text</Format>
  <MaxLength>100</MaxLength>
  <Length>200</Length>
  <displaynames>
    <displayname description="Name" languagecode="1033" />
  </displaynames>
  <Descriptions>
    <Description description="Primary name field" languagecode="1033" />
  </Descriptions>
</attribute>
```

#### 3-9. Audit Fields (Created/Modified)

**CreatedBy** (lookup to systemuser):
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
  <IntroducedVersion>1.0.0.0</IntroducedVersion>
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
    <Description description="Unique identifier of the user who created the record." languagecode="1033" />
  </Descriptions>
</attribute>
```

**CreatedOn** (datetime):
```xml
<attribute PhysicalName="CreatedOn">
  <Type>datetime</Type>
  <Name>createdon</Name>
  <LogicalName>createdon</LogicalName>
  <RequiredLevel>none</RequiredLevel>
  <DisplayMask>ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>
  <ImeMode>inactive</ImeMode>
  <ValidForUpdateApi>0</ValidForUpdateApi>
  <ValidForReadApi>1</ValidForReadApi>
  <ValidForCreateApi>0</ValidForCreateApi>
  <IsCustomField>0</IsCustomField>
  <IsAuditEnabled>0</IsAuditEnabled>
  <IsSecured>0</IsSecured>
  <IntroducedVersion>1.0.0.0</IntroducedVersion>
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
  <IsFilterable>1</IsFilterable>
  <IsRetrievable>1</IsRetrievable>
  <IsLocalizable>0</IsLocalizable>
  <Format>datetime</Format>
  <CanChangeDateTimeBehavior>0</CanChangeDateTimeBehavior>
  <Behavior>1</Behavior>
  <displaynames>
    <displayname description="Created On" languagecode="1033" />
  </displaynames>
  <Descriptions>
    <Description description="Date and time when the record was created." languagecode="1033" />
  </Descriptions>
</attribute>
```

**Additional Audit Fields** (follow same pattern):
- `createdonbehalfby` (lookup)
- `modifiedby` (lookup)
- `modifiedon` (datetime)
- `modifiedonbehalfby` (lookup)

#### 10-13. Ownership Fields

**OwnerId** (owner - special type):
```xml
<attribute PhysicalName="OwnerId">
  <Type>owner</Type>
  <Name>ownerid</Name>
  <LogicalName>ownerid</LogicalName>
  <RequiredLevel>systemrequired</RequiredLevel>
  <DisplayMask>ValidForAdvancedFind|ValidForForm|ValidForGrid|RequiredForForm</DisplayMask>
  <ImeMode>auto</ImeMode>
  <ValidForUpdateApi>1</ValidForUpdateApi>
  <ValidForReadApi>1</ValidForReadApi>
  <ValidForCreateApi>1</ValidForCreateApi>
  <IsCustomField>0</IsCustomField>
  <IsAuditEnabled>0</IsAuditEnabled>
  <IsSecured>0</IsSecured>
  <IntroducedVersion>1.0.0.0</IntroducedVersion>
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
  <IsFilterable>0</IsFilterable>
  <IsRetrievable>0</IsRetrievable>
  <IsLocalizable>0</IsLocalizable>
  <LookupStyle>single</LookupStyle>
  <LookupTypes>
    <LookupType>systemuser</LookupType>
    <LookupType>team</LookupType>
  </LookupTypes>
  <displaynames>
    <displayname description="Owner" languagecode="1033" />
  </displaynames>
  <Descriptions>
    <Description description="Owner Id" languagecode="1033" />
  </Descriptions>
</attribute>
```

**Additional Ownership Fields:**
- `owningbusinessunit` (lookup to businessunit)
- `owningteam` (lookup to team)
- `owninguser` (lookup to systemuser)

#### 14-15. State Management

**StateCode** (state):
```xml
<attribute PhysicalName="StateCode">
  <Type>state</Type>
  <Name>statecode</Name>
  <LogicalName>statecode</LogicalName>
  <RequiredLevel>systemrequired</RequiredLevel>
  <DisplayMask>ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>
  <ImeMode>auto</ImeMode>
  <ValidForUpdateApi>1</ValidForUpdateApi>
  <ValidForReadApi>1</ValidForReadApi>
  <ValidForCreateApi>0</ValidForCreateApi>
  <IsCustomField>0</IsCustomField>
  <IsAuditEnabled>1</IsAuditEnabled>
  <IsSecured>0</IsSecured>
  <IntroducedVersion>1.0.0.0</IntroducedVersion>
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
  <IsFilterable>0</IsFilterable>
  <IsRetrievable>0</IsRetrievable>
  <IsLocalizable>0</IsLocalizable>
  <displaynames>
    <displayname description="Status" languagecode="1033" />
  </displaynames>
  <Descriptions>
    <Description description="Status of the record" languagecode="1033" />
  </Descriptions>
  <StateOptionSet>
    <OptionSetType>state</OptionSetType>
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
  </StateOptionSet>
</attribute>
```

**StatusCode** (status):
```xml
<attribute PhysicalName="StatusCode">
  <Type>status</Type>
  <Name>statuscode</Name>
  <LogicalName>statuscode</LogicalName>
  <RequiredLevel>none</RequiredLevel>
  <DisplayMask>ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>
  <ImeMode>auto</ImeMode>
  <ValidForUpdateApi>1</ValidForUpdateApi>
  <ValidForReadApi>1</ValidForReadApi>
  <ValidForCreateApi>1</ValidForCreateApi>
  <IsCustomField>0</IsCustomField>
  <IsAuditEnabled>1</IsAuditEnabled>
  <IsSecured>0</IsSecured>
  <IntroducedVersion>1.0.0.0</IntroducedVersion>
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
  <displaynames>
    <displayname description="Status Reason" languagecode="1033" />
  </displaynames>
  <Descriptions>
    <Description description="Reason for the status of the record" languagecode="1033" />
  </Descriptions>
  <StatusOptionSet>
    <OptionSetType>status</OptionSetType>
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
  </StatusOptionSet>
</attribute>
```

#### 16-19. Additional System Fields

**ImportSequenceNumber** (int):
- Used for data migration tracking
- Type: `int`
- MinValue: -2147483648, MaxValue: 2147483647

**OverriddenCreatedOn** (datetime):
- For data migration - preserves original creation date
- Type: `datetime`
- Format: `date`

**TimeZoneRuleVersionNumber** (int):
- Tracks time zone rule version
- Type: `int`

**UTCConversionTimeZoneCode** (int):
- Time zone code for UTC conversion
- Type: `int`

**VersionNumber** (bigint):
- Optimistic concurrency version
- Type: `bigint`
- IsValidForCreate="0", IsValidForUpdate="0"

---

## Attribute Types & Metadata

### Common Attribute Types

| Type | Use Case | Key Attributes | Example |
|------|----------|----------------|---------|
| `nvarchar` | Short text (< 4000 chars) | Length, MaxLength, Format | Name, email, phone |
| `memo` | Long text (> 4000 chars) | MaxLength, Format | Description, notes |
| `int` | Integer numbers | MinValue, MaxValue, Format | Count, quantity |
| `decimal` | Decimal numbers | Precision, MinValue, MaxValue | Price, percentage |
| `datetime` | Date/time values | Format, Behavior, CanChangeDateTimeBehavior | Created date, deadline |
| `bit` | Boolean (yes/no) | DefaultValue | IsActive, IsComplete |
| `lookup` | Reference to another entity | LookupStyle, LookupTypes | CreatedBy, OwnerId |
| `owner` | User or Team reference | LookupTypes (systemuser, team) | OwnerId |
| `primarykey` | Entity unique ID | MaxLength=100 (Teams), IsPrimaryId=1 | EntityId |
| `picklist` | Local option set | OptionSet definition | Priority, category |
| `state` | Entity state | StateOptionSet (Active/Inactive) | StateCode |
| `status` | Entity status reason | StatusOptionSet | StatusCode |

### Standard Attribute Metadata Template

**Every attribute should have these properties:**

```xml
<attribute PhysicalName="FieldName">
  <!-- Type & Identity -->
  <Type>nvarchar</Type>
  <Name>prefix_fieldname</Name>
  <LogicalName>prefix_fieldname</LogicalName>

  <!-- Requirement & Validation -->
  <RequiredLevel>none</RequiredLevel>  <!-- none, recommended, systemrequired, applicationrequired -->

  <!-- Display & UI -->
  <DisplayMask>ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>
  <ImeMode>auto</ImeMode>

  <!-- API Permissions -->
  <ValidForUpdateApi>1</ValidForUpdateApi>
  <ValidForReadApi>1</ValidForReadApi>
  <ValidForCreateApi>1</ValidForCreateApi>

  <!-- Field Properties -->
  <IsCustomField>1</IsCustomField>
  <IsAuditEnabled>1</IsAuditEnabled>
  <IsSecured>0</IsSecured>
  <IntroducedVersion>1.0.0.0</IntroducedVersion>

  <!-- Customization Flags -->
  <IsCustomizable>1</IsCustomizable>
  <IsRenameable>1</IsRenameable>
  <CanModifySearchSettings>1</CanModifySearchSettings>
  <CanModifyRequirementLevelSettings>1</CanModifyRequirementLevelSettings>
  <CanModifyAdditionalSettings>1</CanModifyAdditionalSettings>

  <!-- Search & Filter -->
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

  <!-- Type-Specific Attributes -->
  <Format>text</Format>  <!-- or email, url, phone, textarea, etc. -->
  <MaxLength>100</MaxLength>
  <Length>200</Length>

  <!-- Localization -->
  <displaynames>
    <displayname description="Field Display Name" languagecode="1033" />
  </displaynames>
  <Descriptions>
    <Description description="Field description" languagecode="1033" />
  </Descriptions>
</attribute>
```

### Type-Specific Examples

#### Text Field (nvarchar)
```xml
<attribute PhysicalName="pm_EmployeeID">
  <Type>nvarchar</Type>
  <Name>pm_employeeid</Name>
  <LogicalName>pm_employeeid</LogicalName>
  <RequiredLevel>none</RequiredLevel>
  <DisplayMask>ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>
  <!-- ... standard metadata ... -->
  <Format>text</Format>
  <MaxLength>50</MaxLength>
  <Length>100</Length>
  <displaynames>
    <displayname description="Employee ID" languagecode="1033" />
  </displaynames>
</attribute>
```

#### Long Text Field (memo)
```xml
<attribute PhysicalName="pm_Notes">
  <Type>memo</Type>
  <Name>pm_notes</Name>
  <LogicalName>pm_notes</LogicalName>
  <!-- ... standard metadata ... -->
  <Format>textarea</Format>
  <MaxLength>10000</MaxLength>
  <displaynames>
    <displayname description="Notes" languagecode="1033" />
  </displaynames>
</attribute>
```

#### Number Field (int)
```xml
<attribute PhysicalName="pm_Rating">
  <Type>int</Type>
  <Name>pm_rating</Name>
  <LogicalName>pm_rating</LogicalName>
  <!-- ... standard metadata ... -->
  <Format></Format>
  <MinValue>1</MinValue>
  <MaxValue>5</MaxValue>
  <displaynames>
    <displayname description="Rating" languagecode="1033" />
  </displaynames>
</attribute>
```

#### Decimal Field
```xml
<attribute PhysicalName="pm_Score">
  <Type>decimal</Type>
  <Name>pm_score</Name>
  <LogicalName>pm_score</LogicalName>
  <!-- ... standard metadata ... -->
  <Precision>2</Precision>
  <MinValue>0.00</MinValue>
  <MaxValue>100.00</MaxValue>
  <displaynames>
    <displayname description="Score" languagecode="1033" />
  </displaynames>
</attribute>
```

#### Date Field
```xml
<attribute PhysicalName="pm_DueDate">
  <Type>datetime</Type>
  <Name>pm_duedate</Name>
  <LogicalName>pm_duedate</LogicalName>
  <!-- ... standard metadata ... -->
  <Format>date</Format>
  <CanChangeDateTimeBehavior>1</CanChangeDateTimeBehavior>
  <Behavior>1</Behavior>  <!-- 0=UserLocal, 1=DateOnly, 2=TimeZoneIndependent -->
  <displaynames>
    <displayname description="Due Date" languagecode="1033" />
  </displaynames>
</attribute>
```

#### Yes/No Field (bit)
```xml
<attribute PhysicalName="pm_IsActive">
  <Type>bit</Type>
  <Name>pm_isactive</Name>
  <LogicalName>pm_isactive</LogicalName>
  <!-- ... standard metadata ... -->
  <DefaultValue>1</DefaultValue>
  <displaynames>
    <displayname description="Is Active" languagecode="1033" />
  </displaynames>
  <BooleanOptionSet>
    <TrueOption value="1">
      <labels>
        <label description="Yes" languagecode="1033" />
      </labels>
    </TrueOption>
    <FalseOption value="0">
      <labels>
        <label description="No" languagecode="1033" />
      </labels>
    </FalseOption>
  </BooleanOptionSet>
</attribute>
```

#### Local Option Set (picklist)
```xml
<attribute PhysicalName="pm_Priority">
  <Type>picklist</Type>
  <Name>pm_priority</Name>
  <LogicalName>pm_priority</LogicalName>
  <!-- ... standard metadata ... -->
  <displaynames>
    <displayname description="Priority" languagecode="1033" />
  </displaynames>
  <OptionSet>
    <OptionSetType>picklist</OptionSetType>
    <options>
      <option value="1">
        <labels>
          <label description="Low" languagecode="1033" />
        </labels>
      </option>
      <option value="2">
        <labels>
          <label description="Medium" languagecode="1033" />
        </labels>
      </option>
      <option value="3">
        <labels>
          <label description="High" languagecode="1033" />
        </labels>
      </option>
    </options>
  </OptionSet>
</attribute>
```

#### Lookup Field
```xml
<attribute PhysicalName="pm_StaffMemberId">
  <Type>lookup</Type>
  <Name>pm_staffmemberid</Name>
  <LogicalName>pm_staffmemberid</LogicalName>
  <!-- ... standard metadata ... -->
  <LookupStyle>single</LookupStyle>
  <LookupTypes>
    <LookupType>pm_staffmember</LookupType>
  </LookupTypes>
  <displaynames>
    <displayname description="Staff Member" languagecode="1033" />
  </displaynames>
</attribute>
```

---

## Relationship Patterns

### Relationship Types

Dataverse supports three main relationship types:

1. **OneToMany (1:N)** - One parent record, many child records
2. **ManyToOne (N:1)** - Many child records, one parent record (reverse of 1:N)
3. **ManyToMany (N:N)** - Many records related to many records (uses intersect entity)

### Required System Relationships

**Every UserOwned entity MUST have 6 system relationships:**

#### 1. Business Unit Relationship
```xml
<EntityRelationship Name="business_unit_prefix_entityname">
  <EntityRelationshipType>OneToMany</EntityRelationshipType>
  <IsCustomRelationship>0</IsCustomRelationship>
  <IntroducedVersion>1.0</IntroducedVersion>
  <IsHierarchical>0</IsHierarchical>
  <ReferencingEntityName>prefix_EntityName</ReferencingEntityName>
  <ReferencedEntityName>BusinessUnit</ReferencedEntityName>
  <CascadeAssign>NoCascade</CascadeAssign>
  <CascadeDelete>NoCascade</CascadeDelete>
  <CascadeReparent>NoCascade</CascadeReparent>
  <CascadeShare>NoCascade</CascadeShare>
  <CascadeUnshare>NoCascade</CascadeUnshare>
  <CascadeArchive>NoCascade</CascadeArchive>
  <ReferencingAttributeName>owningbusinessunit</ReferencingAttributeName>
  <RelationshipDescription>
    <Descriptions>
      <Description description="" languagecode="1033" />
    </Descriptions>
  </RelationshipDescription>
  <IsCustomizable>1</IsCustomizable>
  <IsValidForAdvancedFind>0</IsValidForAdvancedFind>
  <SchemaName>business_unit_prefix_entityname</SchemaName>
  <SecurityTypes>Append</SecurityTypes>
</EntityRelationship>
```

#### 2. Created By Relationship
```xml
<EntityRelationship Name="lk_prefix_entityname_createdby">
  <EntityRelationshipType>OneToMany</EntityRelationshipType>
  <IsCustomRelationship>0</IsCustomRelationship>
  <IntroducedVersion>1.0</IntroducedVersion>
  <IsHierarchical>0</IsHierarchical>
  <ReferencingEntityName>prefix_EntityName</ReferencingEntityName>
  <ReferencedEntityName>SystemUser</ReferencedEntityName>
  <CascadeAssign>NoCascade</CascadeAssign>
  <CascadeDelete>NoCascade</CascadeDelete>
  <CascadeReparent>NoCascade</CascadeReparent>
  <CascadeShare>NoCascade</CascadeShare>
  <CascadeUnshare>NoCascade</CascadeUnshare>
  <CascadeArchive>NoCascade</CascadeArchive>
  <ReferencingAttributeName>createdby</ReferencingAttributeName>
  <RelationshipDescription>
    <Descriptions>
      <Description description="" languagecode="1033" />
    </Descriptions>
  </RelationshipDescription>
  <IsCustomizable>1</IsCustomizable>
  <IsValidForAdvancedFind>1</IsValidForAdvancedFind>
  <SchemaName>lk_prefix_entityname_createdby</SchemaName>
  <SecurityTypes>Append</SecurityTypes>
</EntityRelationship>
```

#### 3. Modified By Relationship
```xml
<EntityRelationship Name="lk_prefix_entityname_modifiedby">
  <EntityRelationshipType>OneToMany</EntityRelationshipType>
  <IsCustomRelationship>0</IsCustomRelationship>
  <IntroducedVersion>1.0</IntroducedVersion>
  <IsHierarchical>0</IsHierarchical>
  <ReferencingEntityName>prefix_EntityName</ReferencingEntityName>
  <ReferencedEntityName>SystemUser</ReferencedEntityName>
  <CascadeAssign>NoCascade</CascadeAssign>
  <CascadeDelete>NoCascade</CascadeDelete>
  <CascadeReparent>NoCascade</CascadeReparent>
  <CascadeShare>NoCascade</CascadeShare>
  <CascadeUnshare>NoCascade</CascadeUnshare>
  <CascadeArchive>NoCascade</CascadeArchive>
  <ReferencingAttributeName>modifiedby</ReferencingAttributeName>
  <RelationshipDescription>
    <Descriptions>
      <Description description="" languagecode="1033" />
    </Descriptions>
  </RelationshipDescription>
  <IsCustomizable>1</IsCustomizable>
  <IsValidForAdvancedFind>1</IsValidForAdvancedFind>
  <SchemaName>lk_prefix_entityname_modifiedby</SchemaName>
  <SecurityTypes>Append</SecurityTypes>
</EntityRelationship>
```

#### 4. Owner Relationship
```xml
<EntityRelationship Name="owner_prefix_entityname">
  <EntityRelationshipType>OneToMany</EntityRelationshipType>
  <IsCustomRelationship>0</IsCustomRelationship>
  <IntroducedVersion>1.0</IntroducedVersion>
  <IsHierarchical>0</IsHierarchical>
  <ReferencingEntityName>prefix_EntityName</ReferencingEntityName>
  <ReferencedEntityName>Owner</ReferencedEntityName>
  <CascadeAssign>NoCascade</CascadeAssign>
  <CascadeDelete>NoCascade</CascadeDelete>
  <CascadeReparent>NoCascade</CascadeReparent>
  <CascadeShare>NoCascade</CascadeShare>
  <CascadeUnshare>NoCascade</CascadeUnshare>
  <CascadeArchive>NoCascade</CascadeArchive>
  <ReferencingAttributeName>ownerid</ReferencingAttributeName>
  <RelationshipDescription>
    <Descriptions>
      <Description description="" languagecode="1033" />
    </Descriptions>
  </RelationshipDescription>
  <IsCustomizable>1</IsCustomizable>
  <IsValidForAdvancedFind>1</IsValidForAdvancedFind>
  <SchemaName>owner_prefix_entityname</SchemaName>
  <SecurityTypes>Append</SecurityTypes>
</EntityRelationship>
```

#### 5. Team Ownership Relationship
```xml
<EntityRelationship Name="team_prefix_entityname">
  <EntityRelationshipType>OneToMany</EntityRelationshipType>
  <IsCustomRelationship>0</IsCustomRelationship>
  <IntroducedVersion>1.0</IntroducedVersion>
  <IsHierarchical>0</IsHierarchical>
  <ReferencingEntityName>prefix_EntityName</ReferencingEntityName>
  <ReferencedEntityName>Team</ReferencedEntityName>
  <CascadeAssign>NoCascade</CascadeAssign>
  <CascadeDelete>NoCascade</CascadeDelete>
  <CascadeReparent>NoCascade</CascadeReparent>
  <CascadeShare>NoCascade</CascadeShare>
  <CascadeUnshare>NoCascade</CascadeUnshare>
  <CascadeArchive>NoCascade</CascadeArchive>
  <ReferencingAttributeName>owningteam</ReferencingAttributeName>
  <RelationshipDescription>
    <Descriptions>
      <Description description="" languagecode="1033" />
    </Descriptions>
  </RelationshipDescription>
  <IsCustomizable>1</IsCustomizable>
  <IsValidForAdvancedFind>0</IsValidForAdvancedFind>
  <SchemaName>team_prefix_entityname</SchemaName>
  <SecurityTypes>Append</SecurityTypes>
</EntityRelationship>
```

#### 6. User Ownership Relationship
```xml
<EntityRelationship Name="user_prefix_entityname">
  <EntityRelationshipType>OneToMany</EntityRelationshipType>
  <IsCustomRelationship>0</IsCustomRelationship>
  <IntroducedVersion>1.0</IntroducedVersion>
  <IsHierarchical>0</IsHierarchical>
  <ReferencingEntityName>prefix_EntityName</ReferencingEntityName>
  <ReferencedEntityName>SystemUser</ReferencedEntityName>
  <CascadeAssign>NoCascade</CascadeAssign>
  <CascadeDelete>NoCascade</CascadeDelete>
  <CascadeReparent>NoCascade</CascadeReparent>
  <CascadeShare>NoCascade</CascadeShare>
  <CascadeUnshare>NoCascade</CascadeUnshare>
  <CascadeArchive>NoCascade</CascadeArchive>
  <ReferencingAttributeName>owninguser</ReferencingAttributeName>
  <RelationshipDescription>
    <Descriptions>
      <Description description="" languagecode="1033" />
    </Descriptions>
  </RelationshipDescription>
  <IsCustomizable>1</IsCustomizable>
  <IsValidForAdvancedFind>0</IsValidForAdvancedFind>
  <SchemaName>user_prefix_entityname</SchemaName>
  <SecurityTypes>Append</SecurityTypes>
</EntityRelationship>
```

**Key Differences in System Relationships:**
- `IntroducedVersion="1.0"` (NOT "1.0.0.0")
- All cascades set to `NoCascade`
- NO `EntityRelationshipRoles` section
- NO `CascadeRollupView` attribute
- `IsCustomRelationship="0"`

### Custom Entity Relationships

For relationships between your custom entities:

#### OneToMany Custom Relationship
```xml
<EntityRelationship Name="prefix_parententity_childentity">
  <EntityRelationshipType>OneToMany</EntityRelationshipType>
  <IsCustomRelationship>1</IsCustomRelationship>
  <IntroducedVersion>1.0.0.0</IntroducedVersion>
  <IsHierarchical>0</IsHierarchical>
  <ReferencingEntityName>prefix_ChildEntity</ReferencingEntityName>
  <ReferencedEntityName>prefix_ParentEntity</ReferencedEntityName>
  <CascadeAssign>Cascade</CascadeAssign>
  <CascadeDelete>RemoveLink</CascadeDelete>  <!-- or Cascade, Restrict -->
  <CascadeReparent>Cascade</CascadeReparent>
  <CascadeShare>Cascade</CascadeShare>
  <CascadeUnshare>Cascade</CascadeUnshare>
  <CascadeArchive>NoCascade</CascadeArchive>
  <CascadeRollupView>NoCascade</CascadeRollupView>
  <IsValidForAdvancedFind>1</IsValidForAdvancedFind>
  <ReferencingAttributeName>prefix_parententityid</ReferencingAttributeName>
  <RelationshipDescription>
    <Descriptions>
      <Description description="Relationship between Parent and Child" languagecode="1033" />
    </Descriptions>
  </RelationshipDescription>
  <IsCustomizable>1</IsCustomizable>
  <SchemaName>prefix_parententity_childentity</SchemaName>
  <SecurityTypes>Append</SecurityTypes>
  <EntityRelationshipRoles>
    <EntityRelationshipRole>
      <NavPaneDisplayOption>UseCollectionName</NavPaneDisplayOption>
      <NavPaneArea>Details</NavPaneArea>
      <NavPaneOrder>10000</NavPaneOrder>
      <NavigationPropertyName>prefix_parententity_childentity</NavigationPropertyName>
      <RelationshipRoleType>1</RelationshipRoleType>
    </EntityRelationshipRole>
    <EntityRelationshipRole>
      <NavPaneDisplayOption>UseCollectionName</NavPaneDisplayOption>
      <NavPaneArea>Details</NavPaneArea>
      <NavPaneOrder>10000</NavPaneOrder>
      <NavigationPropertyName>prefix_ParentEntityId</NavigationPropertyName>
      <RelationshipRoleType>0</RelationshipRoleType>
    </EntityRelationshipRole>
  </EntityRelationshipRoles>
</EntityRelationship>
```

**Cascade Options:**
- `NoCascade` - No cascade action
- `Cascade` - Perform action on related records
- `RemoveLink` - Remove relationship but keep records
- `Restrict` - Prevent deletion if related records exist
- `UserOwned` - Cascade only if user owns both records

**Common Cascade Patterns:**

| Scenario | Assign | Delete | Reparent | Share | Unshare |
|----------|--------|--------|----------|-------|---------|
| Tight coupling (delete children) | Cascade | Cascade | Cascade | Cascade | Cascade |
| Loose coupling (keep children) | Cascade | RemoveLink | Cascade | Cascade | Cascade |
| Prevent orphans | Cascade | Restrict | Cascade | Cascade | Cascade |
| System relationships | NoCascade | NoCascade | NoCascade | NoCascade | NoCascade |

---

## Canvas App Structure

### Canvas App File (.msapp)

Canvas apps are ZIP archives with the following internal structure:

```
appname.msapp (ZIP file)
├── AppCheckerResult.sarif
├── Connections/
│   └── Connections.json
├── DataSources/
│   ├── CustomGallerySample.json
│   └── prefix_entityname.json
├── Controls/
│   └── 1.json  # Screen definitions
├── Header.json
├── Properties.json
├── References/
│   ├── DataSources.json
│   └── Resources.json
├── Resources/
│   └── PublishInfo.json
├── Src/
│   └── *.fx.yaml  # Formula files
└── pkgs/
    └── Wadl/
```

### Canvas App Registration in Solution

In solution.xml:
```xml
<RootComponent type="300" schemaName="prefix_appname_a1b2c" behavior="0" />
```

In file structure:
```
CanvasApps/
├── prefix_appname_a1b2c_DocumentUri.msapp
└── prefix_appname_a1b2c_BackgroundImageUri
```

In [Content_Types].xml:
```xml
<Default Extension="msapp" ContentType="application/octet-stream" />
<Override PartName="/CanvasApps/prefix_appname_a1b2c_BackgroundImageUri"
          ContentType="application/octet-stream" />
```

---

## Formula/Workflow Patterns

### Calculated Columns (XAML Formulas)

Formulas are stored as XAML files in the Formulas/ directory.

**Naming Convention:**
```
entityname-fieldname.xaml
```

Example: `msft_employeeidea_campaign-msft_calc_daysuntilend.xaml`

**Formula Structure:**
```xml
<Activity x:Class="XrmWorkflow00000000000000000000000000000000"
          xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
          xmlns:mcwc="clr-namespace:Microsoft.Crm.Workflow.ClientActivities;assembly=Microsoft.Crm.Workflow, Version=9.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35"
          xmlns:mva="clr-namespace:Microsoft.VisualBasic.Activities;assembly=System.Activities, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35"
          xmlns:mxs="clr-namespace:Microsoft.Xrm.Sdk;assembly=Microsoft.Xrm.Sdk, Version=9.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35"
          xmlns:mxswa="clr-namespace:Microsoft.Xrm.Sdk.Workflow.Activities;assembly=Microsoft.Xrm.Sdk.Workflow, Version=9.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35"
          xmlns:s="clr-namespace:System;assembly=mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089"
          xmlns:scg="clr-namespace:System.Collections.Generic;assembly=mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089"
          xmlns:sco="clr-namespace:System.Collections.ObjectModel;assembly=mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089"
          xmlns:srs="clr-namespace:System.Runtime.Serialization;assembly=System.Runtime.Serialization, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089"
          xmlns:this="clr-namespace:"
          xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <x:Members>
    <x:Property Name="InputEntities" Type="InArgument(scg:IDictionary(x:String, mxs:Entity))" />
    <x:Property Name="CreatedEntities" Type="InArgument(scg:IDictionary(x:String, mxs:Entity))" />
  </x:Members>

  <mxswa:Workflow>
    <!-- Formula logic here -->
  </mxswa:Workflow>
</Activity>
```

**Common Formula Operations:**

| Operation | XAML Element | Example Use |
|-----------|--------------|-------------|
| Get field value | `<mxswa:GetEntityProperty>` | Read entity field |
| Set field value | `<mxswa:SetEntityProperty>` | Update calculated field |
| Date diff | `<InArgument x:Key="ExpressionOperator">DiffInDays</InArgument>` | Calculate days between dates |
| Current time | `<InArgument x:Key="ExpressionOperator">Now</InArgument>` | Get current timestamp |
| Conditional | `<mxswa:ActivityReference AssemblyQualifiedName="...ConditionBranch">` | If/then logic |

### Registration in Solution

Formulas don't appear as root components, but are registered via calculated field attributes:

```xml
<attribute PhysicalName="prefix_CalculatedField">
  <Type>int</Type>
  <Name>prefix_calculatedfield</Name>
  <!-- ... standard metadata ... -->
  <IsCalculated>1</IsCalculated>
  <CalculationDefinition>
    <!-- Reference to formula file -->
  </CalculationDefinition>
</attribute>
```

---

## Root Component Types

Complete reference of component types found in Microsoft solutions:

| Type | Component Name | Description | Example |
|------|----------------|-------------|---------|
| 1 | Entity | Custom or system entity | Staff Member, Evaluation |
| 2 | Attribute | Entity attribute (rarely root) | Custom field |
| 9 | Option Set | Global option set | Status codes, categories |
| 10 | Entity Relationship | N:N relationship | Many-to-many |
| 11 | Entity Relationship Role | Relationship role | Connection roles |
| 12 | Entity Relationship Relationships | Related relationships | Hierarchical |
| 29 | Workflow | Process/Workflow | Power Automate flow |
| 31 | Report | SSRS report | Custom report |
| 48 | SiteMap | Navigation sitemap | App navigation |
| 59 | Chart | Visualization chart | Dashboard chart |
| 60 | Dashboard | System dashboard | Overview dashboard |
| 61 | Web Resource | JavaScript, HTML, CSS, images | Custom web files |
| 62 | Connection Role | Connection role definition | Partner, Stakeholder |
| 80 | Hierarchical Rule | Hierarchy rule | Org chart |
| 82 | Complex Control | Custom control | PCF control |
| 300 | Canvas App | Power Apps canvas app | Mobile/tablet app |
| 371 | Connector | Custom connector | External API |
| 380 | Environment Variable Definition | Config variable | API endpoint URL |
| 381 | Environment Variable Value | Variable value | Production URL |
| 430 | Entity Analytics Configuration | Analytics config | Usage analytics |
| 431 | File Column | File/image column | Entity image field |
| 432 | Entity Image | Primary image | Profile picture |

**Most Common in Teams Apps:**

- **Type 1 (Entity)** - All custom entities
- **Type 9 (Option Set)** - Global picklists
- **Type 300 (Canvas App)** - The app itself
- **Type 431 (File Column)** - Image/file fields
- **Type 432 (Entity Image)** - Primary entity image

---

## Publisher Configuration

### Publisher Options

**For Dataverse for Teams apps:**
```xml
<Publisher>
  <UniqueName>yourpublisher</UniqueName>
  <CustomizationPrefix>prefix</CustomizationPrefix>
  <CustomizationOptionValuePrefix>10000</CustomizationOptionValuePrefix>
</Publisher>
```

**Prefix Requirements:**
- 3-8 lowercase letters
- Must be unique in environment
- Prepended to all entity/field names
- Examples: `pm`, `msft`, `contoso`

**Option Value Prefix:**
- 10000-99999 range
- Used for option set values
- Must be unique in environment
- Ensures no conflicts between publishers

**Microsoft Prefixes (for reference):**
- `msft` - 29960 (Teams apps)
- `msdyn` - 19235 (Dynamics 365)
- `cr` - Standard prefix

---

## Version Management

### Version Format

Dataverse solutions use 4-part versioning:

```
Major.Minor.Build.Revision
```

Examples from Microsoft solutions:
- `1.0.812.4` (Area Inspection)
- `1.0.548.3` (Employee Ideas)
- `1.0.560.3` (Bulletins)

**Semantic Versioning Guidelines:**

| Part | When to Increment | Example |
|------|-------------------|---------|
| Major | Breaking changes, major features | 1.x.x.x → 2.0.0.0 |
| Minor | New features, non-breaking | 1.0.x.x → 1.1.0.0 |
| Build | Bug fixes, patches | 1.0.0.x → 1.0.1.0 |
| Revision | Hotfixes, minor tweaks | 1.0.0.0 → 1.0.0.1 |

**In solution.xml:**
```xml
<Version>1.0.0.0</Version>
```

**IntroducedVersion in Components:**
```xml
<IntroducedVersion>1.0.0.0</IntroducedVersion>
```

For new components added in updates:
```xml
<IntroducedVersion>1.1.0.0</IntroducedVersion>
```

---

## Import/Export Considerations

### Managed vs. Unmanaged Solutions

**Unmanaged (`<Managed>0</Managed>`):**
- Fully editable after import
- Can be deleted completely
- Use for development and source control
- All components customizable

**Managed (`<Managed>1</Managed>`):**
- Locked from editing (unless allowed)
- Cannot be directly deleted
- Use for distribution to customers
- Protects intellectual property

**Microsoft samples are all Managed (1)**

### Teams Environment Specific Requirements

**Critical Differences from Standard Dataverse:**

1. **MaxLength on PrimaryKey required**
   ```xml
   <Type>primarykey</Type>
   <MaxLength>100</MaxLength>  <!-- MUST have for Teams -->
   ```

2. **Stricter validation**
   - All metadata attributes verified
   - System relationships required
   - Entity name casing enforced

3. **Limited system entity access**
   - Can't modify many system entities
   - Restricted relationship types

4. **No certain components**
   - No plugins (custom workflow activities)
   - No custom actions (limited)
   - No server-side sync

### Pre-Import Checklist

Before importing to Teams:

- [ ] All entities have PascalCase names in customizations.xml
- [ ] All entities have lowercase schema names in solution.xml
- [ ] Primary key fields have MaxLength="100"
- [ ] All 17 system fields present on each entity
- [ ] 6 system relationships per UserOwned entity
- [ ] Primary name field has "PrimaryName" in DisplayMask
- [ ] customizations.xml has complete embedded entity definitions
- [ ] All RootComponents declared in solution.xml
- [ ] Publisher prefix consistent throughout
- [ ] Version number incremented from previous
- [ ] [Content_Types].xml includes all file extensions

### Common Import Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Entity not found in MetadataCache | Missing entity metadata OR incomplete customizations.xml | Embed full definitions in customizations.xml, add all entity metadata |
| PrimaryName attribute not found | Missing "PrimaryName" in DisplayMask | Add to DisplayMask: `PrimaryName\|ValidFor...` |
| New string attributes must have max length | Primary key missing MaxLength | Add `<MaxLength>100</MaxLength>` to primarykey |
| AsyncOperation relationship error | Missing system relationships | Add all 6 system relationships per entity |
| Invalid entity name | Wrong casing | Use PascalCase in customizations.xml |

---

## Appendix: Complete Checklists

### Entity Creation Checklist

**For each new entity:**

- [ ] Create entity definition in customizations.xml
- [ ] Use PascalCase for entity Name attribute
- [ ] Add all 30+ entity metadata attributes
- [ ] Add primary key field with MaxLength=100
- [ ] Add primary name field with PrimaryName in DisplayMask
- [ ] Add all 17 system fields
- [ ] Add 6 system relationships
- [ ] Add custom business fields
- [ ] Add custom relationships (if any)
- [ ] Add to RootComponents in solution.xml (lowercase schema name)
- [ ] Update EntitySetName (plural)
- [ ] Set IntroducedVersion

### Solution Package Checklist

**Before packing:**

- [ ] [Content_Types].xml present with all extensions
- [ ] solution.xml complete with all RootComponents
- [ ] customizations.xml has embedded entity definitions
- [ ] Canvas apps in CanvasApps/ folder (if any)
- [ ] Formulas in Formulas/ folder (if any)
- [ ] All entity names consistent (PascalCase vs lowercase)
- [ ] Publisher info complete and correct
- [ ] Version number incremented
- [ ] All files UTF-8 encoded

### Pre-Import Testing Checklist

**Validation steps:**

- [ ] XML files are well-formed (use xmllint or XML validator)
- [ ] Unpack solution and review structure
- [ ] Count entities vs RootComponents (should match)
- [ ] Count relationships (6 system + N custom per entity)
- [ ] Verify all lookup fields have matching relationships
- [ ] Check for orphaned references
- [ ] Verify prefix consistency
- [ ] Test import in dev environment first

---

## Summary: Key Architectural Principles

### 1. Structure

- customizations.xml contains COMPLETE entity definitions (embedded, not separate files)
- Entity names use PascalCase in customizations.xml, lowercase in solution.xml
- All files must be properly structured XML

### 2. Metadata

- Every entity needs 30+ metadata attributes
- Every entity needs 17+ system fields
- Every attribute needs 20+ metadata properties
- Primary keys need MaxLength=100 for Teams

### 3. Relationships

- UserOwned entities require 6 system relationships
- Custom relationships need cascade behavior defined
- System relationships use IntroducedVersion="1.0"
- Custom relationships use IntroducedVersion="1.0.0.0"

### 4. Components

- Declare ALL components in solution.xml RootComponents
- Use correct component type numbers
- Canvas apps are type 300
- Entities are type 1
- Option sets are type 9

### 5. Teams-Specific

- Stricter validation than standard Dataverse
- MaxLength required on primarykey
- Limited system entity access
- Must test in Teams environment

---

**End of Specification**

For questions or issues, refer to:
- Microsoft Learn: Power Platform documentation
- IMPORT-TROUBLESHOOTING-GUIDE.md in this repository
- Microsoft sample solutions in ref/ folder

**Document Maintainer:** Auto-generated from analysis
**Last Analysis Date:** 2025-11-16
**Solutions Analyzed:** 6 official Microsoft Teams sample apps
