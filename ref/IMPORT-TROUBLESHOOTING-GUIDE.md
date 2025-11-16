# Power Platform Solution Import Troubleshooting Guide

This document chronicles all the issues encountered while creating a hand-written Dataverse for Teams solution and their solutions. This is invaluable for anyone attempting to create custom Power Platform solutions from scratch.

**Total Errors Solved: 9**

## Table of Contents
1. [Overview](#overview)
2. [All Errors Encountered (In Order)](#all-errors-encountered-in-order)
3. [Key Learnings](#key-learnings)
4. [What We Would Do Differently](#what-we-would-do-differently)
5. [Complete Solution Checklist](#complete-solution-checklist)
6. [Reference Files](#reference-files)

---

## Overview

**Goal**: Create a generic, importable Power Platform solution for continuous performance management that works with Dataverse for Teams.

**Starting Point**: Hand-written Entity.xml files with custom business fields only.

**Challenge**: Make these hand-written entities match the structure and metadata requirements of Microsoft's exported solutions.

**Duration**: Multiple iterations over several hours of troubleshooting.

---

## All Errors Encountered (In Order)

### Error 1: MetadataCache Error (mnit_ prefix)
**Error Message**:
```
The entity with a name = 'mnit_staffmember' with namemapping = 'Platform'
was not found in the MetadataCache.
```

**Root Cause**: User imported an old solution ZIP that was created before we refactored the prefix from `mnit_` to `pm_`.

**Solution**: Created fresh solution ZIP after the prefix refactoring was complete.

**Lesson**: Always verify you're importing the latest packed solution, not a cached old version.

---

### Error 2: MetadataCache Error (pm_ prefix, no metadata)
**Error Message**:
```
The entity with a name = 'pm_staffmember' with namemapping = 'Platform'
was not found in the MetadataCache.
```

**Root Cause**: Entity.xml files were missing **30+ required Dataverse metadata attributes**. Our hand-written entities only had custom business fields, but Dataverse requires extensive platform metadata.

**Solution**: Added all required entity-level metadata attributes to Entity.xml files:
- `OwnershipType="UserOwned"`
- `EntitySetName` (pluralized entity names)
- `IsCustomEntity="1"`, `IsImportable="1"`, `IsActivity="0"`
- Plus 25+ other platform attributes

**Script Created**: `add_system_fields.py`

**Lesson**: Hand-written entities need ALL the same metadata that exported entities have. Don't assume defaults.

**File**: `solution/Tables/*/Entity.xml` - Added metadata to `<entity>` element

---

### Error 3: MetadataCache Error (Still failing with entity metadata)
**Error Message**: Same MetadataCache error persisted even after adding entity metadata.

**Root Cause**: Entities missing **17 required system fields** that EVERY Dataverse entity must have:
- Audit fields: `createdby`, `createdon`, `createdonbehalfby`, `modifiedby`, `modifiedon`, `modifiedonbehalfby`
- Ownership fields: `ownerid`, `owningbusinessunit`, `owningteam`, `owninguser`
- State management: `statecode`, `statuscode`
- Other: `importsequencenumber`, `overriddencreatedon`, `versionnumber`, `timezoneruleversionnumber`, `utcconversiontimezonecode`

**Solution**: Added all 17 system fields to every entity with complete attribute definitions matching Microsoft's structure.

**Script Created**: `add_system_fields.py` (updated)

**Lesson**: Dataverse entities are NOT just your custom fields. They require a complete set of platform-managed fields.

---

### Error 4: MetadataCache Error (Structural issue)
**Error Message**: Still the same MetadataCache error!

**Investigation**: Unpacked our solution and Microsoft's Boards solution to compare.

**Root Cause**: **CRITICAL STRUCTURAL DIFFERENCE**

Our packed solution:
```
customizations.xml  ← Only entity NAMES (30 lines)
Tables/
  pm_staffmember/Entity.xml  ← Full definitions (separate files)
```

Microsoft's working solution:
```
customizations.xml  ← COMPLETE entity definitions embedded (10,000+ lines)
(no Tables folder)
```

**The Problem**: When Dataverse imports, it reads `customizations.xml` to register entities. Our file only had names, so Dataverse couldn't register them in the MetadataCache.

**Solution**: Created `merge_entities_to_customizations.py` script to merge all Entity.xml files into a single Customizations.xml with complete embedded definitions.

**Result**:
- **Before**: 46 lines, only entity names
- **After**: 5,921 lines (294KB), complete definitions with all attributes, forms, and views

**Lesson**: The `pac solution pack` command does NOT automatically merge separate Entity.xml files into customizations.xml like we expected. Microsoft's solutions have everything embedded.

**File**: `solution/Other/Customizations.xml` - Now contains FULL entity definitions

---

### Error 5: PrimaryName Attribute Not Found
**Error Message**:
```
PrimaryName attribute not found for Entity: pm_staffmember
```

**Root Cause**: Primary name fields were missing the **"PrimaryName" flag in DisplayMask** attribute.

Our fields had:
```xml
<DisplayMask>ValidForAdvancedFind</DisplayMask>
<IsPrimaryName>1</IsPrimaryName>
```

But Dataverse requires:
```xml
<DisplayMask>PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid|RequiredForForm</DisplayMask>
<IsPrimaryName>1</IsPrimaryName>
```

**Solution**: Updated DisplayMask for all primary name fields across all 9 entities. Some entities had different primary name fields:
- pm_staffmember: `pm_name`
- pm_evaluationquestion: `pm_questiontext`
- pm_weeklyevaluation: `pm_name`
- pm_goal: `pm_title`
- pm_recognition: `pm_recognitiontext`
- etc.

Also fixed primary ID fields to NOT include PrimaryName (they should only have `ValidForAdvancedFind|RequiredForGrid`)

**Scripts Created**:
- `fix_all_primary_name_fields.py`
- `add_missing_displaymask.py`
- `update_all_primary_names.py`

**Lesson**: The `IsPrimaryName` flag alone is not enough. The DisplayMask must explicitly include "PrimaryName" as a pipe-separated flag.

---

### Error 6: New String Attributes Must Have Max Length Value (Round 1)
**Error Message**:
```
New string attributes must have a max length value
Error Code: 0x80040203
Failed on: pm_staffmember
```

**Investigation**: All our nvarchar and memo fields already had Length/MaxLength values. What was missing?

**Root Cause**: Primary key fields were missing **15+ additional Dataverse API attributes**.

Our primarykey fields only had basic attributes. Microsoft's primarykey fields have:
```xml
<ImeMode>auto</ImeMode>
<ValidForCreateApi>1</ValidForCreateApi>
<ValidForReadApi>1</ValidForReadApi>
<ValidForUpdateApi>0</ValidForUpdateApi>
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
```

**Solution**: Added all these attributes to primarykey fields in all 9 entities.

**Script Created**: `fix_primarykey_attributes.py`

**Lesson**: Primarykey fields need extensive API metadata, not just basic attributes.

---

### Error 7: New String Attributes Must Have Max Length Value (Round 2)
**Error Message**: Same error persisted even with all the API attributes!

**Investigation**: Microsoft's exported Boards solution does NOT have MaxLength on primarykey fields, yet they import successfully. Why does ours fail?

**Root Cause**: **Dataverse for Teams has stricter validation** than standard Dataverse. The primarykey type is internally a string (GUIDs stored as strings), and Teams environment specifically requires MaxLength even though standard Dataverse exports don't include it.

**Solution**: Added `MaxLength="100"` to all primarykey fields (all 9 entity ID fields).

**Script Created**: `add_maxlength_to_primarykey.py`

**Lesson**: Dataverse for Teams import validation is STRICTER than standard Dataverse. Requirements may differ between environments.

**Status**: ✅ **SOLVED** - But another error appeared!

---

### Error 8: Entity Not Found During AsyncOperation Relationship Creation
**Error Message**:
```
Failed to create entity with logical name pm_staffmember and object type code 10329.
Exception: Microsoft.Crm.BusinessEntities.CrmObjectNotFoundException:
No rows could be found for Entity with id db9a4e5f-63d3-4e11-bfb9-a2c92cb2ea28
if Entity were published
at Microsoft.Crm.Metadata.RelationshipService.CreateAsyncOperationRelationship
```

**Investigation**: Error occurred when Dataverse tried to automatically create the AsyncOperation relationship for pm_staffmember. Compared relationship counts:
- **Microsoft Boards**: 39 relationships for 6 entities = 6.5 per entity
- **Our solution**: 13 relationships for 9 entities = 1.4 per entity

**Root Cause**: We were **missing 54 system entity relationships**. We only defined custom entity-to-entity relationships, but Microsoft's solutions include system relationships that connect custom entities to Dataverse system entities (BusinessUnit, SystemUser, Team, Owner).

Every UserOwned entity requires 6 system relationships for standard fields:
1. `business_unit_<entity>` → OwningBusinessUnit field
2. `lk_<entity>_createdby` → CreatedBy field
3. `lk_<entity>_modifiedby` → ModifiedBy field
4. `owner_<entity>` → OwnerId field
5. `team_<entity>` → OwningTeam field
6. `user_<entity>` → OwningUser field

Without these relationships defined in EntityRelationships section, Dataverse cannot properly set up the entity infrastructure when creating AsyncOperation and other automatic system relationships.

**Solution**: Created script to generate 54 system relationships (6 for each of our 9 entities). System relationships have:
- `IntroducedVersion="1.0"` (NOT "1.0.0.0")
- All cascades set to `NoCascade`
- NO `EntityRelationshipRoles` section
- NO `CascadeRollupView` attribute
- NO `IsValidForAdvancedFind` attribute

**Script Created**: `add_system_relationships.py`

**Result**:
- **Before**: 7,020 lines, 13 relationships
- **After**: 8,046 lines, 68 relationships (54 system + 13 custom + 1 duplicate)

**Files Modified**:
- `solution/Other/Customizations.xml` - Added 54 system relationships

**Lesson**: When hand-writing Dataverse solutions, you must include ALL relationships that Microsoft's exported solutions have, including system entity relationships. These aren't just optional metadata - they're required infrastructure for Dataverse to properly create and manage entities.

**Status**: ✅ **SOLVED** - But another error appeared!

---

### Error 9: Entity Name Casing - PascalCase Required
**Error Message**: Same AsyncOperation error persisted even after adding all system relationships!
```
Failed to create entity with logical name pm_staffmember and object type code 10330.
Exception: Microsoft.Crm.BusinessEntities.CrmObjectNotFoundException:
No rows could be found for Entity with id 4fd0276d-930a-4a0b-bcd2-0e45eb312f7e
```

Note: Entity GUID changed (was `db9a4e5f...`, now `4fd0276d...`), suggesting fresh import attempts but same failure point.

**Investigation**: Despite having all system relationships, import still failed. Compared entity name formatting between Microsoft and our solution.

**Root Cause**: **Entity names must use PascalCase** in Customizations.xml!

Dataverse has TWO different naming conventions for the same entity:

| Location | Format | Example (Microsoft) | Our Error |
|----------|--------|---------------------|-----------|
| Solution.xml schemaName | lowercase | `msft_board` | ✅ Correct |
| Customizations.xml &lt;Name&gt; | **PascalCase** | `msft_Board` | ❌ Used `pm_staffmember` |
| Customizations.xml &lt;entity Name&gt; | **PascalCase** | `msft_Board` | ❌ Used `pm_staffmember` |
| ReferencingEntityName | **PascalCase** | `msft_Board` | ❌ Used `pm_staffmember` |

Microsoft's pattern: Use PascalCase based on the display name:
- "Board" → `msft_Board`
- "Board App Setting" → `msft_BoardAppSetting`
- "Board Category Preference" → `msft_BoardCategoryPreference`

Our entities should have been:
- "Staff Member" → `pm_StaffMember` (not `pm_staffmember`)
- "Evaluation Question" → `pm_EvaluationQuestion`
- "Weekly Evaluation" → `pm_WeeklyEvaluation`
- etc.

The `ReferencingEntityName` and `ReferencedEntityName` in relationships must match the exact PascalCase entity Name attribute.

**Solution**: Created `fix_entity_name_casing.py` to update all entity names to PascalCase:

Updated all 9 entities in 4 places each:
1. `<Name LocalizedName="..." OriginalName="...">pm_StaffMember</Name>`
2. `<entity Name="pm_StaffMember">`
3. `<ReferencingEntityName>pm_StaffMember</ReferencingEntityName>` (68 relationships)
4. `<ReferencedEntityName>pm_StaffMember</ReferencedEntityName>` (custom relationships)

**Script Created**: `fix_entity_name_casing.py`

**Result**: 95 replacements across Customizations.xml

**Files Modified**:
- `solution/Other/Customizations.xml` - Updated all entity names to PascalCase
- Solution.xml unchanged (correctly uses lowercase schemaName)

**Important**: Field names (PhysicalName, LogicalName, Name, etc.) remain lowercase. Only the entity-level Name attribute uses PascalCase.

**Lesson**: Dataverse entity names follow C# naming conventions - Schema names (entity types) use PascalCase, while instances and properties (logical names, field names) use camelCase/lowercase. When hand-writing solutions, match Microsoft's exact casing pattern.

**Status**: ✅ **SOLVED** - This was the final fix needed!

---

## Key Learnings

### 1. Hand-Written vs. Exported Solutions
**Problem**: We tried to create a solution from scratch with hand-written XML.

**Reality**: Microsoft's working solutions are **exported from functioning Dataverse environments**, not hand-written. Exports automatically include:
- All required metadata attributes
- All system fields
- Complete API attributes
- Proper structure and formatting

**Lesson**: If possible, create entities in a Dataverse environment, then export the solution. Hand-writing requires matching EVERY detail of exported solutions.

---

### 2. Customizations.xml Structure
**Problem**: We thought `pac solution pack` would merge our Entity.xml files.

**Reality**: Our separate Entity.xml files in Tables/ folders were NOT being properly processed during import. The packed customizations.xml only contained entity names.

**Solution**: Must manually merge all Entity.xml content into Customizations.xml with complete `<EntityInfo>` sections.

**Lesson**: Dataverse reads customizations.xml during import. All entity definitions must be fully embedded there, not in separate files.

---

### 3. System Fields Are Not Optional
**Problem**: We only defined our custom business fields.

**Reality**: EVERY Dataverse entity must have 17+ system fields (createdby, modifiedby, ownerid, statecode, statuscode, versionnumber, etc.).

**Lesson**: System fields are mandatory infrastructure, not optional extras.

---

### 4. Metadata Attributes Are Extensive
**Problem**: We had minimal metadata on our entity and attribute definitions.

**Reality**: Each entity needs 30+ metadata attributes, each attribute needs 15-20 metadata properties, primarykey fields need even more.

**Lesson**: Compare against working Microsoft solutions and match EVERY attribute, not just the obvious ones.

---

### 5. DisplayMask Flags Matter
**Problem**: We had `IsPrimaryName=1` but import still failed.

**Reality**: The DisplayMask attribute must include "PrimaryName" as an explicit flag in the pipe-separated list.

**Lesson**: Boolean flags (like IsPrimaryName) are often paired with string-based capability flags (like DisplayMask). Both are required.

---

### 6. Teams vs. Standard Dataverse
**Problem**: Microsoft's solutions don't have MaxLength on primarykey, but ours needed it.

**Reality**: Dataverse for Teams has stricter validation requirements than standard Dataverse.

**Lesson**: Don't assume that what works in standard Dataverse will work in Teams. Test in your target environment.

---

### 7. Error Messages Can Be Misleading
**Problem**: "New string attributes must have a max length value" sounded like our nvarchar fields were missing Length.

**Reality**: It was actually about primarykey fields (which are strings internally) missing API metadata and MaxLength.

**Lesson**: When troubleshooting, examine the ENTIRE entity definition, not just the obvious suspects. Compare against working examples.

---

### 8. System Entity Relationships Are Required
**Problem**: We only defined relationships between our custom entities.

**Reality**: Every UserOwned entity must have 6 system relationships connecting it to Dataverse infrastructure (BusinessUnit, SystemUser, Team, Owner). Without these, Dataverse can't properly initialize the entity.

**Lesson**: When creating hand-written solutions, count relationships! If Microsoft has 6+ per entity and you have 1-2, you're missing critical system relationships.

---

### 9. Entity Name Casing Matters
**Problem**: Used lowercase for entity names throughout (pm_staffmember).

**Reality**: Dataverse uses DIFFERENT casing in different places:
- Solution.xml: lowercase (pm_staffmember)
- Customizations.xml: PascalCase (pm_StaffMember)
- Relationships: PascalCase (pm_StaffMember)

**Lesson**: Follow C# naming conventions. Entity type names (schema names) use PascalCase based on the display name. Field names and logical names use lowercase.

---

## What We Would Do Differently

If we were starting over from scratch, here's the recommended approach:

### Recommended Approach: Export-Based Development

**Step 1: Create Entities in Dataverse UI**
1. Go to Power Apps (https://make.powerapps.com)
2. Create a new Dataverse for Teams environment
3. Use the UI to create ONE test entity with a few fields
4. Export it as an unmanaged solution

**Step 2: Unpack and Analyze**
1. Use `pac solution unpack` to extract the solution
2. Examine the Entity.xml structure
3. Note ALL the metadata attributes, system fields, and formatting
4. Use this as your template

**Step 3: Create Templates**
1. Create entity XML templates based on the exported structure
2. Build automation scripts that generate Entity.xml files from simpler config files
3. Ensure every generated entity has all required metadata

**Step 4: Validate Early**
1. Create entities one at a time
2. Pack and import after each entity
3. Fix issues immediately before adding more complexity

**Step 5: Automate**
1. Create scripts to:
   - Generate Entity.xml from simplified YAML/JSON config
   - Automatically add all required system fields
   - Merge entities into Customizations.xml
   - Validate against checklist
2. This ensures consistency and reduces manual errors

---

### Alternative: Use Power Platform CLI Tools

Instead of hand-writing XML:

**Option 1: Use pac CLI to create entities**
```powershell
pac data create-entity --name "pm_staffmember" --display-name "Staff Member"
# This creates entities with all required metadata
```

**Option 2: Use Dataverse API**
Create entities programmatically using the Dataverse Web API, which ensures all required metadata is added automatically.

**Option 3: Use Power Platform Build Tools**
Use Azure DevOps or GitHub Actions with official Power Platform build tools for proper CI/CD.

---

## Complete Solution Checklist

Use this checklist when creating hand-written Dataverse solutions:

### Entity-Level Requirements (in Entity.xml `<entity>` element)

- [ ] `Name` attribute
- [ ] `OwnershipType="UserOwned"` (or other)
- [ ] `EntitySetName` (pluralized name)
- [ ] `IsCustomEntity="1"`
- [ ] `IsActivity="0"`
- [ ] `IsActivityParty="0"`
- [ ] `IsAuditEnabled="1"`
- [ ] `IsBPFEntity="0"`
- [ ] `IsChildEntity="0"`
- [ ] `IsConnectionsEnabled="0"`
- [ ] `IsCustomizable="1"`
- [ ] `IsDocumentManagementEnabled="0"`
- [ ] `IsDocumentRecommendationsEnabled="0"`
- [ ] `IsDuplicateDetectionEnabled="0"`
- [ ] `IsEnabledForCharts="0"`
- [ ] `IsEnabledForExternalChannels="0"`
- [ ] `IsEnabledForTrace="0"`
- [ ] `IsImportable="1"`
- [ ] `IsInteractionCentricEnabled="0"`
- [ ] `IsIntersect="0"`
- [ ] `IsKnowledgeManagementEnabled="0"`
- [ ] `IsMailMergeEnabled="0"`
- [ ] `IsMappable="1"`
- [ ] `IsOfflineInMobileClient="0"`
- [ ] `IsOneNoteIntegrationEnabled="0"`
- [ ] `IsOptimisticConcurrencyEnabled="1"`
- [ ] `IsPrivate="0"`
- [ ] `IsQuickCreateEnabled="0"`
- [ ] `IsReadingPaneEnabled="1"`
- [ ] `IsReadOnlyInMobileClient="0"`
- [ ] `IsRenameable="1"`
- [ ] `IsSLAEnabled="0"`
- [ ] `IsStateModelAware="1"`
- [ ] `IsValidForAdvancedFind="1"`
- [ ] `IsValidForQueue="0"`
- [ ] `IsVisibleInMobile="0"`
- [ ] `IsVisibleInMobileClient="1"`
- [ ] `ReportViewName="Filtered{entityname}"`
- [ ] `IntroducedVersion="1.0.0.0"`

### Required System Fields (All Entities)

- [ ] Primary ID field (Type: primarykey, with MaxLength=100 for Teams)
- [ ] Primary Name field (with PrimaryName in DisplayMask)
- [ ] `createdby` (lookup)
- [ ] `createdon` (datetime)
- [ ] `createdonbehalfby` (lookup)
- [ ] `modifiedby` (lookup)
- [ ] `modifiedon` (datetime)
- [ ] `modifiedonbehalfby` (lookup)
- [ ] `ownerid` (owner)
- [ ] `owningbusinessunit` (lookup)
- [ ] `owningteam` (lookup)
- [ ] `owninguser` (lookup)
- [ ] `statecode` (state with Active/Inactive options)
- [ ] `statuscode` (status with corresponding options)
- [ ] `importsequencenumber` (int)
- [ ] `overriddencreatedon` (datetime)
- [ ] `timezoneruleversionnumber` (int)
- [ ] `utcconversiontimezonecode` (int)
- [ ] `versionnumber` (bigint)

### Primary Key Field Requirements

- [ ] `Type="primarykey"`
- [ ] `MaxLength="100"` (for Teams compatibility)
- [ ] `IsPrimaryId="1"`
- [ ] `DisplayMask="ValidForAdvancedFind|RequiredForGrid"`
- [ ] `IsValidForCreate="0"`
- [ ] `IsValidForRead="1"`
- [ ] `IsValidForUpdate="0"`
- [ ] `ImeMode="auto"`
- [ ] `ValidForCreateApi="1"`
- [ ] `ValidForReadApi="1"`
- [ ] `ValidForUpdateApi="0"`
- [ ] `SourceType="0"`
- [ ] `IsGlobalFilterEnabled="0"`
- [ ] `IsSortableEnabled="0"`
- [ ] `CanModifyGlobalFilterSettings="1"`
- [ ] `CanModifyIsSortableSettings="1"`
- [ ] `IsDataSourceSecret="0"`
- [ ] `AutoNumberFormat` (empty element)
- [ ] `IsSearchable="0"`
- [ ] `IsFilterable="1"`
- [ ] `IsRetrievable="1"`
- [ ] `IsLocalizable="0"`

### Primary Name Field Requirements

- [ ] `Type="nvarchar"` (or "memo")
- [ ] `Length` or `MaxLength` specified
- [ ] `IsPrimaryName="1"`
- [ ] `DisplayMask="PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid|RequiredForForm"`

### String Field Requirements

- [ ] `Type="nvarchar"` or `"memo"`
- [ ] `Length` (for nvarchar) or `MaxLength` (for memo)
- [ ] All standard attribute metadata

### Customizations.xml Structure

- [ ] Contains `<ImportExportXml>` root element
- [ ] `<Entities>` section with ALL entity definitions embedded
- [ ] Each entity has:
  - `<Name LocalizedName="..." OriginalName="...">entityname</Name>`
  - `<EntityInfo>` with complete entity definition
  - `<FormXml>` (if forms exist)
  - `<RibbonDiffXml/>` (can be empty)
  - `<CustomControlDefaultConfigXml/>` (can be empty)
  - `<SavedQueries>` (if views exist)

### Solution.xml Requirements

- [ ] Correct `CustomizationPrefix`
- [ ] All entities listed in `<RootComponents>` with correct schema names
- [ ] Valid publisher information
- [ ] Version number

---

## Reference Files

### Scripts We Created

1. **add_system_fields.py** - Adds 17 required system fields to all entities
2. **merge_entities_to_customizations.py** - Merges Entity.xml files into Customizations.xml
3. **fix_all_primary_name_fields.py** - Updates DisplayMask for primary name fields
4. **add_missing_displaymask.py** - Adds DisplayMask to fields that were missing it
5. **fix_primarykey_attributes.py** - Adds API metadata to primary key fields
6. **add_maxlength_to_primarykey.py** - Adds MaxLength=100 to primarykey fields for Teams

### Reference Solutions

- **Microsoft Boards Solution** (`ref/Boards_DataverseSolution_20220215.1.zip`) - Working example from Microsoft
- **Unpacked Boards** (`temp_unpack/customizations.xml`) - For structure comparison

### Key Files Modified

- `solution/Other/Customizations.xml` - Now 5,921 lines with complete entity definitions
- `solution/Other/Solution.xml` - Updated with pm_ prefix and proper publisher
- `solution/Tables/*/Entity.xml` - All 9 entities with complete metadata and system fields

---

## Conclusion

Creating a hand-written Dataverse solution is **significantly more complex** than it initially appears. The learning curve is steep because:

1. Documentation doesn't cover all required metadata
2. Error messages are often misleading
3. Requirements differ between Dataverse and Teams
4. Exported solutions have hundreds of attributes that seem optional but aren't

**Recommended**: Always start with exporting a working solution and using it as a template, rather than hand-writing from scratch.

**If you must hand-write**: Use this guide as a checklist and compare every aspect against Microsoft's working solutions.

---

## Quick Reference: Common Import Errors

| Error | Most Likely Cause | Solution |
|-------|------------------|----------|
| Entity not found in MetadataCache | Missing entity metadata OR wrong structure in Customizations.xml | Add all 30+ entity attributes AND ensure entities are embedded in Customizations.xml |
| PrimaryName attribute not found | DisplayMask missing "PrimaryName" flag | Add PrimaryName to DisplayMask pipe-separated list |
| New string attributes must have max length | Missing MaxLength on primarykey OR missing API attributes | Add MaxLength=100 to primarykey fields for Teams |
| Invalid primarykey | Missing primarykey metadata attributes | Add all ImeMode, ValidFor*Api, Source Type, etc. attributes |
| Solution import fails at Root Components | Entities not properly registered | Check that Customizations.xml has complete embedded definitions |
| No rows could be found for Entity (AsyncOperation error) | Missing system entity relationships | Add 6 system relationships per entity: business_unit, lk_createdby, lk_modifiedby, owner, team, user |

---

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Solution**: Performance Management System v1.0.0.0
