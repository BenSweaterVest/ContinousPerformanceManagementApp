# Solution Fixes Journey
**10 Iterations from Failure to Success**

## Overview

This document chronicles the systematic debugging process that took the Performance Management solution from repeated import failures to a successful deployment on Teams Dataverse. Each iteration represents a specific error discovered during import, the root cause analysis, and the fix applied.

**Final Result**: Version 2.0.0.7 - Successfully imports to Microsoft Teams Dataverse

**Total Iterations**: 10 major fixes (versions 2.0.0.0 through 2.0.0.7)

**Key Learning**: Teams Dataverse has stricter validation than full Dataverse. Many issues stemmed from incompatibilities between desktop Dataverse and the lightweight Teams version.

## The Journey

### Iteration 0: Initial Import Attempt (Version 2.0.0.0)

**What We Tried**:
- Exported solution from desktop Power Apps
- Attempted import to Teams Dataverse environment

**Error**:
```
Invalid string format Text for column pm_name.
Please use a correct format.
```

**Root Cause**:
All primary name fields (`pm_name`) contained `<Format>text</Format>` elements. Teams Dataverse doesn't accept Format elements on nvarchar (string) type columns.

**Analysis**:
Desktop Dataverse automatically adds `<Format>` tags to indicate display formatting. Teams Dataverse rejects these as invalid.

**Fix**: Iteration 1

---

### Iteration 1: Remove Text Format (Version 2.0.0.1)

**Changes Applied**:
- Created `remove_text_format.py` script
- Removed all `<Format>text</Format>` elements from Customizations.xml
- Found and removed 6 occurrences in pm_name fields

**Script**:
```python
import re

with open('solution/Other/Customizations.xml', 'r') as f:
    content = f.read()

# Remove <Format>text</Format> lines
content = re.sub(r'\s*<Format>text</Format>\s*\n', '', content)

with open('solution/Other/Customizations.xml', 'w') as f:
    f.write(content)
```

**Result**: Package created: `PerformanceManagement_v2.0.0.1.zip`

**Next Error**:
```
The format DateAndTime is not valid for the datetime type column pm_startdate
of table pm_StaffMember.
```

**Fix**: Iteration 2

---

### Iteration 2: Remove DateTime Format (Version 2.0.0.2)

**Root Cause**:
Similar to Iteration 1 - datetime fields had `<Format>DateAndTime</Format>` elements that Teams Dataverse rejects.

**Changes Applied**:
- Created `remove_datetime_format.py` script
- Identified 9 datetime fields across entities:
  - pm_staffmember: pm_startdate, pm_enddate
  - pm_weeklyevaluation: pm_weekending
  - pm_selfevaluation: pm_submitteddate
  - pm_meetingnote: pm_meetingdate
  - pm_goal: pm_startdate, pm_targetdate, pm_completeddate
  - pm_recognition: pm_date
- Removed `<Format>` elements from all datetime fields

**Script Pattern**:
```python
import re

content = re.sub(
    r'(<attribute PhysicalName="[^"]*">.*?<Type>datetime</Type>.*?)\s*<Format>[^<]*</Format>\s*\n',
    r'\1\n',
    content,
    flags=re.DOTALL
)
```

**Result**: Package created: `PerformanceManagement_v2.0.0.2.zip`

**Lesson Learned**: Teams Dataverse has no support for `<Format>` elements on any field type. Always remove them.

**Next Error**:
```
Import failed: Unable to find attribute type by name memo
Parameter name: name
```

**Fix**: Iteration 3

---

### Iteration 3: Convert Memo to NText (Version 2.0.0.2 - repackaged)

**Root Cause**:
Desktop Dataverse uses "memo" as a data type for multi-line text fields. Teams Dataverse only recognizes "ntext" for this purpose.

**Fields Affected** (11 total):
- pm_weeklyevaluation: pm_comments
- pm_selfevaluation: pm_reflections, pm_achievements, pm_challenges
- pm_meetingnote: pm_notes, pm_actionitems, pm_followup
- pm_goal: pm_description
- pm_recognition: pm_description
- pm_actionitem: pm_description
- pm_idpentry: pm_goaldescription

**Changes Applied**:
- Created `convert_memo_to_ntext.py` script
- Simple find-and-replace: `<Type>memo</Type>` → `<Type>ntext</Type>`

**Script**:
```python
content = content.replace('<Type>memo</Type>', '<Type>ntext</Type>')
```

**Result**: Converted 11 memo fields to ntext, package created

**Version Note**: This was packaged as v2.0.0.2 (same version as Iteration 2, which was an oversight)

**Next Error**:
```
The following attributes pm_evaluator of entity pm_WeeklyEvaluation are missing
their associated relationship definition.
```

**Fix**: Iteration 4

---

### Iteration 4: Add Evaluator Relationship (Version 2.0.0.2 - fixed version)

**Root Cause**:
The `pm_evaluator` field was defined as a lookup field (Target = "systemuser"), but no corresponding EntityRelationship was defined. Dataverse requires explicit relationship definitions for all lookup fields.

**Analysis**:
In `pm_weeklyevaluation` entity:
```xml
<attribute PhysicalName="pm_evaluator">
  <Type>lookup</Type>
  <Name>pm_evaluator</Name>
  <LogicalName>pm_evaluator</LogicalName>
  <RequiredLevel>none</RequiredLevel>
  <DisplayMask>ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>
  <Target>systemuser</Target>  <!-- Lookup to User table -->
</attribute>
```

But no `<EntityRelationship>` existed for this field.

**Additional Issue Found**:
The Target was set to "systemuser" (built-in user table), but our data model design intended `pm_evaluator` to reference `pm_staffmember` (since supervisors are also staff members).

**Changes Applied**:
- Created `add_evaluator_relationship.py` script
- Added EntityRelationship definition for pm_evaluator
- **Fixed Target** from "systemuser" to "pm_staffmember"

**Relationship Added**:
```xml
<EntityRelationship Name="pm_staffmember_pm_evaluator_pm_weeklyevaluation">
  <EntityRelationshipType>OneToMany</EntityRelationshipType>
  <IsCustomizable>1</IsCustomizable>
  <IntroducedVersion>1.0</IntroducedVersion>
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
  <ReferencingAttributeName>pm_evaluator</ReferencingAttributeName>
  <RelationshipDescription>
    <Descriptions>
      <Description description="Relationship between Staff Member and Weekly Evaluation for evaluator" languagecode="1033" />
    </Descriptions>
  </RelationshipDescription>
  <EntityRelationshipRoles>
    <EntityRelationshipRole>
      <NavPaneDisplayOption>UseCollectionName</NavPaneDisplayOption>
      <NavPaneArea>Details</NavPaneArea>
      <NavPaneOrder>10000</NavPaneOrder>
      <NavigationPropertyName>pm_staffmember_pm_evaluator_pm_weeklyevaluation</NavigationPropertyName>
      <RelationshipRoleType>1</RelationshipRoleType>
    </EntityRelationshipRole>
  </EntityRelationshipRoles>
</EntityRelationship>
```

**Result**: Package created, now properly defining the evaluator relationship

**Lesson Learned**: Every lookup field requires a corresponding EntityRelationship definition. Dataverse doesn't auto-generate these.

**Next Error**:
```
The new pm_goaldescription attribute is set as the primary name attribute for the
pm_IDPEntry entity. The pm_IDPEntry entity already has the pm_name attribute set
as the primary name attribute.
```

**Fix**: Iteration 5

---

### Iteration 5: Fix Duplicate Primary Name (Version 2.0.0.3)

**Root Cause**:
Each Dataverse entity can have only ONE primary name field. The pm_IDPEntry entity had TWO fields marked as primary name:
- pm_name (correct)
- pm_goaldescription (incorrect)

**Analysis**:
In the pm_goaldescription field definition:
```xml
<DisplayMask>PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>
```

The `PrimaryName` flag should only exist on pm_name.

**Changes Applied**:
- Created `fix_duplicate_primary_name.py` script
- Found pm_goaldescription field in pm_IDPEntry entity
- Removed `PrimaryName` from DisplayMask

**Before**:
```xml
<DisplayMask>PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>
```

**After**:
```xml
<DisplayMask>ValidForAdvancedFind|ValidForForm|ValidForGrid</DisplayMask>
```

**Result**: Package created: `PerformanceManagement_v2.0.0.3.zip`

**Lesson Learned**: Only one field per entity can have `PrimaryName` in its DisplayMask. Typically, this is the pm_name field (or equivalent).

**Next Error**:
```
The following attributes pm_owner of entity pm_ActionItem are missing their
associated relationship definition.
```

**Fix**: Iteration 6

---

### Iteration 6: Add Owner Relationship (Version 2.0.0.4)

**Root Cause**:
Same issue as Iteration 4 - another lookup field without its EntityRelationship definition.

**Analysis**:
The pm_actionitem entity had a `pm_owner` lookup field (person responsible for the action item) pointing to pm_staffmember, but no relationship was defined.

**Changes Applied**:
- Created `add_owner_relationship.py` script
- Added EntityRelationship for pm_owner

**Relationship Added**:
```xml
<EntityRelationship Name="pm_staffmember_pm_owner_pm_actionitem">
  <EntityRelationshipType>OneToMany</EntityRelationshipType>
  <ReferencingEntityName>pm_ActionItem</ReferencingEntityName>
  <ReferencedEntityName>pm_StaffMember</ReferencedEntityName>
  <CascadeAssign>NoCascade</CascadeAssign>
  <CascadeDelete>RemoveLink</CascadeDelete>
  <ReferencingAttributeName>pm_owner</ReferencingAttributeName>
  <RelationshipDescription>
    <Descriptions>
      <Description description="Relationship between Staff Member and Action Item for owner" languagecode="1033" />
    </Descriptions>
  </RelationshipDescription>
</EntityRelationship>
```

**Result**: Package created: `PerformanceManagement_v2.0.0.4.zip`

**Lesson Learned**: Need to systematically check ALL lookup fields and ensure each has a corresponding relationship.

**Next Error**:
```
Error while importing workflow cda026dd-326a-ca25-a20a-f71f4c1269c4 type ModernFlow
name AdHocSelfEvalRequest: The import has failed because component
{cda026dd-326a-ca25-a20a-f71f4c1269c4} of type 29 is not declared in the solution
file as a root component.
```

**Fix**: Iteration 7

---

### Iteration 7: Remove Workflows Section (Version 2.0.0.5)

**Root Cause**:
Desktop Dataverse solutions can embed workflows (Power Automate flows) in the `<Workflows>` section of Customizations.xml. Teams Dataverse does NOT support embedded workflows - they must be created separately in Power Automate after solution import.

**Analysis**:
Our Customizations.xml contained:
```xml
<Workflows>
  <Workflow Name="AdHocSelfEvalRequest">...</Workflow>
  <Workflow Name="QuarterlySelfEvalReminder">...</Workflow>
  <Workflow Name="OneOnOneMeetingNotification">...</Workflow>
  <Workflow Name="WeeklyEvaluationReminder">...</Workflow>
</Workflows>
```

These 4 workflows were:
1. AdHocSelfEvalRequest - Trigger self-evaluation on demand
2. QuarterlySelfEvalReminder - Automated quarterly reminders
3. OneOnOneMeetingNotification - Meeting prep emails
4. WeeklyEvaluationReminder - Monday morning evaluation reminders

**Changes Applied**:
- Created `remove_workflows.py` script
- Removed entire `<Workflows>` section from Customizations.xml
- Kept workflow JSON files in `solution/Workflows/` for reference

**Script**:
```python
import re

content = re.sub(r'\s*<Workflows>.*?</Workflows>\s*', '\n', content, flags=re.DOTALL)
```

**Result**: Removed 4 workflows, package size reduced from ~17KB to ~10KB

**Deployment Note**: The 4 workflows now need to be manually created in Power Automate after importing the solution. JSON definitions are available in `solution/Workflows/` folder as templates.

**Lesson Learned**: Teams Dataverse requires workflows to be deployed separately from the solution. Keep workflow JSONs as reference but don't embed them in Customizations.xml.

**Next Error**:
```
CanvasApp import: FAILURE: The solution specified an expected assets file but that
file was missing or invalid.
```

**Fix**: Iteration 8

---

### Iteration 8: Remove Canvas App Root Component (Version 2.0.0.6)

**Root Cause**:
Solution.xml declared a canvas app as a root component, but the actual .msapp file was missing (or invalid - 0 bytes).

**Analysis**:
In `Other/Solution.xml`:
```xml
<RootComponents>
  <RootComponent type="1" schemaName="pm_staffmember" behavior="0" />
  ...
  <RootComponent type="300" schemaName="pm_performancemanagement_12345" behavior="0" />
  <!-- Type 300 = Canvas App -->
</RootComponents>
```

The canvas app component was declared but not built yet.

**Decision**:
Since we're building the Dataverse layer first and will create the canvas app separately later, we removed the canvas app from root components.

**Changes Applied**:
- Edited `solution/Other/Solution.xml`
- Removed canvas app RootComponent entry
- Kept only the 9 entity declarations

**Before**: 10 root components (9 entities + 1 canvas app)
**After**: 9 root components (9 entities only)

**Result**: Package created: `PerformanceManagement_v2.0.0.6.zip`

**Deployment Strategy**: Import Dataverse entities first, then build and add canvas app in Power Apps Studio later.

**Next Error**:
```
CanvasApp import: FAILURE: The import has failed because component
pm_performancemanagement_12345 of type 300 is not declared in the solution file
as a root component.
```

**Fix**: Iteration 9

---

### Iteration 9: Remove CanvasApps Section (Version 2.0.0.7)

**Root Cause**:
Even though we removed the canvas app from root components (Iteration 8), the `<CanvasApps>` section still existed in Customizations.xml, causing a mismatch.

**Analysis**:
Two locations referenced the canvas app:
1. ✅ `Other/Solution.xml` - RootComponents (removed in Iteration 8)
2. ❌ `Other/Customizations.xml` - CanvasApps section (still present)

The Customizations.xml contained:
```xml
<CanvasApps>
  <CanvasApp>
    <Name>pm_performancemanagement_12345</Name>
    ...
  </CanvasApp>
</CanvasApps>
```

**Changes Applied**:
- Created `remove_canvasapp.py` script
- Removed entire `<CanvasApps>` section from Customizations.xml

**Script**:
```python
import re

content = re.sub(r'\s*<CanvasApps>.*?</CanvasApps>\s*', '\n', content, flags=re.DOTALL)
```

**Result**: Package created: `PerformanceManagement_v2.0.0.7.zip`

**File Size**: 9.0 KB (smallest version - just entities, no workflows, no canvas app)

**Next Result**: SUCCESS!

---

### Iteration 10: SUCCESS! (Version 2.0.0.7)

**Import Result**:
```
✓ Customizations from file 'PerformanceManagement_v2.0.0.7.zip' imported successfully.
```

**What Was Imported**:
- 9 Dataverse entities with full schema
- All field definitions
- All relationships
- No workflows (to be created separately)
- No canvas app (to be built separately)

**Verification**:
- Opened Teams Power Apps
- Confirmed 9 tables visible
- All fields present and correct
- Relationships working
- Ready for canvas app development

**Final Package Details**:
- Size: 9.0 KB
- SHA256: c675a0a18c62bc0f8f64b5fe1377932babc413b5d34e57e400c91cf71ed53a79
- Location: `releases/PerformanceManagement_v2.0.0.7.zip`

---

## Summary of All Fixes

| Iteration | Version | Error | Fix | Files Changed |
|-----------|---------|-------|-----|---------------|
| 0 | 2.0.0.0 | Invalid string format Text | - | Initial attempt |
| 1 | 2.0.0.1 | Text format on pm_name | Remove `<Format>text</Format>` | remove_text_format.py |
| 2 | 2.0.0.2 | DateTime format invalid | Remove `<Format>DateAndTime</Format>` | remove_datetime_format.py |
| 3 | 2.0.0.2 | Memo type not found | Convert memo → ntext | convert_memo_to_ntext.py |
| 4 | 2.0.0.2 | Missing pm_evaluator relationship | Add EntityRelationship + fix Target | add_evaluator_relationship.py |
| 5 | 2.0.0.3 | Duplicate primary name | Remove PrimaryName from pm_goaldescription | fix_duplicate_primary_name.py |
| 6 | 2.0.0.4 | Missing pm_owner relationship | Add EntityRelationship | add_owner_relationship.py |
| 7 | 2.0.0.5 | Workflow not in root components | Remove `<Workflows>` section | remove_workflows.py |
| 8 | 2.0.0.6 | Canvas app file missing | Remove canvas app from RootComponents | Manual edit Solution.xml |
| 9 | 2.0.0.7 | Canvas app section mismatch | Remove `<CanvasApps>` section | remove_canvasapp.py |
| 10 | 2.0.0.7 | ✓ SUCCESS | Imports successfully | - |

## Key Lessons Learned

### 1. Teams Dataverse is Stricter
- No `<Format>` elements on any field type
- "memo" must be "ntext"
- Workflows cannot be embedded
- Canvas apps must be built in Power Apps Studio

### 2. Every Lookup Needs a Relationship
- Lookup fields require explicit EntityRelationship definitions
- Dataverse doesn't auto-generate these
- Must specify cascade behaviors (assign, delete, share, etc.)

### 3. Primary Name Field Rules
- Only ONE field per entity can be marked PrimaryName
- Usually the pm_name field (or equivalent)
- Other fields should NOT have PrimaryName in DisplayMask

### 4. Solution Components
- Solution.xml and Customizations.xml must be in sync
- If a component is in RootComponents, it must have corresponding definition
- Missing components cause import failures

### 5. Systematic Approach Wins
- Each error revealed one specific issue
- Fix one thing at a time
- Test after each fix
- Document what changed and why
- Version numbering helps track progress

## Tools Created

All scripts created during this process:
- `remove_text_format.py` - Remove Format from nvarchar fields
- `remove_datetime_format.py` - Remove Format from datetime fields
- `convert_memo_to_ntext.py` - Convert memo type to ntext
- `add_evaluator_relationship.py` - Add missing pm_evaluator relationship
- `fix_duplicate_primary_name.py` - Remove duplicate PrimaryName
- `add_owner_relationship.py` - Add missing pm_owner relationship
- `remove_workflows.py` - Remove Workflows section
- `remove_canvasapp.py` - Remove CanvasApps section

These scripts are **one-time use** - they were needed to fix the initial solution structure. Once applied, they're not needed again.

## Reusable Checklist for Future Solutions

When migrating desktop Dataverse solutions to Teams Dataverse:

**Pre-Import Checklist**:
- [ ] Remove ALL `<Format>` elements (text, datetime, etc.)
- [ ] Convert all `memo` types to `ntext`
- [ ] Verify every lookup field has a corresponding EntityRelationship
- [ ] Ensure only ONE field per entity has PrimaryName in DisplayMask
- [ ] Remove `<Workflows>` section (deploy flows separately)
- [ ] Remove `<CanvasApps>` section (build app separately)
- [ ] Verify Solution.xml RootComponents match Customizations.xml contents
- [ ] Increment version number
- [ ] Package solution with correct ZIP structure
- [ ] Test import in dev environment

**Post-Import Tasks**:
- [ ] Create Power Automate flows using JSON templates from solution/Workflows/
- [ ] Build canvas app in Power Apps Studio
- [ ] Add canvas app to solution
- [ ] Export complete solution (entities + app + flows)
- [ ] Test in fresh environment

## Conclusion

What started as a series of import failures turned into a deep understanding of Teams Dataverse requirements and solution structure. The systematic approach of:
1. Attempt import
2. Read error message carefully
3. Identify root cause
4. Apply targeted fix
5. Document what changed
6. Test and repeat

...led to a successfully importing solution in 10 iterations.

This journey is valuable not just for this project, but as a learning resource for anyone building Power Platform solutions for Teams Dataverse. The lessons learned here are broadly applicable to any solution migration from desktop Dataverse to Teams.

**Final Status**: ✅ Performance Management solution Version 2.0.0.7 successfully imports to Microsoft Teams Dataverse.
