# Performance Management App - Rebuild Design Document

**Created:** 2025-11-16
**Purpose:** Complete rebuild of PerformanceManagement solution from scratch using Microsoft-accurate patterns
**Based on:** Analysis of 6 Microsoft official sample solutions + troubleshooting documentation

---

## Executive Summary

This rebuild will create a completely fresh PerformanceManagement solution that follows Microsoft's exact architectural patterns discovered through analysis of official Teams sample apps. The current solution has been through many fix iterations and needs a clean start to ensure import success.

**Key Changes from Current Solution:**
1. Complete recreation of all entity definitions with exact Microsoft metadata
2. Proper entity name casing (PascalCase in customizations.xml)
3. All system relationships properly defined
4. Workflows moved to separate JSON definitions (not embedded in solution)
5. Canvas app properly registered but not embedded
6. All attribute metadata matching Microsoft patterns exactly

---

## Solution Architecture

### Solution Metadata

| Property | Value |
|----------|-------|
| UniqueName | PerformanceManagement |
| Display Name | Performance Management System |
| Version | 2.0.0.0 (new major version for clean start) |
| Publisher | perfmgmt |
| Prefix | pm |
| Managed | 0 (Unmanaged) |
| Option Value Prefix | 10000 |

### Root Components (14 total)

**Entities (9):**
- pm_staffmember (Staff Member)
- pm_evaluationquestion (Evaluation Question)
- pm_weeklyevaluation (Weekly Evaluation)
- pm_selfevaluation (Self Evaluation)
- pm_idpentry (IDP Entry)
- pm_meetingnote (Meeting Note)
- pm_goal (Goal)
- pm_recognition (Recognition)
- pm_actionitem (Action Item)

**Canvas App (1):**
- pm_performancemanagement_12345

**Workflows (4):**
- WeeklyEvaluationReminder
- QuarterlySelfEvalReminder
- OneOnOneMeetingNotification
- AdHocSelfEvalRequest

---

## Entity Definitions

### 1. Staff Member (pm_StaffMember)

**Purpose:** Store employee records for performance tracking

**Schema Name:** pm_staffmember (lowercase)
**Entity Name:** pm_StaffMember (PascalCase)
**Display Name:** Staff Member
**Collection Name:** Staff Members
**Ownership:** UserOwned
**Entity Set Name:** pm_staffmembers

**Custom Fields:**
| Logical Name | Type | Display Name | Length | Required | Notes |
|--------------|------|--------------|--------|----------|-------|
| pm_name | nvarchar | Name | 100 | Yes | Primary name field |
| pm_employeeid | nvarchar | Employee ID | 50 | No | Unique identifier |
| pm_positiontitle | nvarchar | Position Title | 100 | No | Job title |
| pm_startdate | datetime | Start Date | - | No | Employment start date |
| pm_department | nvarchar | Department | 100 | No | Department/team |

**Relationships:**
- 6 system relationships (business_unit, lk_createdby, lk_modifiedby, owner, team, user)
- 1:N to pm_WeeklyEvaluation (supervisor evaluates many staff)
- 1:N to pm_SelfEvaluation (staff member has many self-evals)
- 1:N to pm_IDPEntry (staff member has many IDP entries)
- 1:N to pm_MeetingNote (staff member has many meeting notes)
- 1:N to pm_Goal (staff member has many goals)
- 1:N to pm_Recognition (staff member receives recognition)
- 1:N to pm_ActionItem (staff member has action items)

### 2. Evaluation Question (pm_EvaluationQuestion)

**Purpose:** Store the 12 standardized performance evaluation questions

**Schema Name:** pm_evaluationquestion
**Entity Name:** pm_EvaluationQuestion
**Display Name:** Evaluation Question
**Collection Name:** Evaluation Questions
**Ownership:** UserOwned
**Entity Set Name:** pm_evaluationquestions

**Custom Fields:**
| Logical Name | Type | Display Name | Length | Required | Notes |
|--------------|------|--------------|--------|----------|-------|
| pm_questiontext | nvarchar | Question Text | 500 | Yes | Primary name - the actual question |
| pm_questionnumber | int | Question Number | - | Yes | 1-12, for rotation algorithm |
| pm_category | picklist | Category | - | No | Categories like "Quality", "Teamwork" |
| pm_isactive | bit | Is Active | - | No | Allow disabling questions |

**Picklist Values (pm_category):**
- 1: Quality of Work
- 2: Productivity
- 3: Communication
- 4: Teamwork
- 5: Leadership
- 6: Problem Solving
- 7: Initiative
- 8: Adaptability
- 9: Customer Service
- 10: Technical Skills
- 11: Professional Development
- 12: Accountability

**Relationships:**
- 6 system relationships
- 1:N to pm_WeeklyEvaluation (question used in evaluations)
- 1:N to pm_SelfEvaluation (question used in self-evals)

### 3. Weekly Evaluation (pm_WeeklyEvaluation)

**Purpose:** Store weekly supervisor evaluations (2 per week per staff member)

**Schema Name:** pm_weeklyevaluation
**Entity Name:** pm_WeeklyEvaluation
**Display Name:** Weekly Evaluation
**Collection Name:** Weekly Evaluations
**Ownership:** UserOwned
**Entity Set Name:** pm_weeklyevaluations

**Custom Fields:**
| Logical Name | Type | Display Name | Length | Required | Notes |
|--------------|------|--------------|--------|----------|-------|
| pm_name | nvarchar | Name | 200 | Yes | Primary name - auto-generated "StaffName - Week X" |
| pm_staffmemberid | lookup | Staff Member | - | Yes | → pm_StaffMember |
| pm_questionid | lookup | Question | - | Yes | → pm_EvaluationQuestion |
| pm_weeknumber | int | Week Number | - | Yes | Week number in year |
| pm_year | int | Year | - | Yes | Evaluation year |
| pm_rating | int | Rating | - | No | 1-5 scale |
| pm_insufficientdata | bit | Insufficient Data | - | No | Supervisor hasn't observed |
| pm_notes | memo | Notes | 4000 | No | Additional comments |
| pm_evaluationdate | datetime | Evaluation Date | - | No | When eval was completed |

**Relationships:**
- 6 system relationships
- N:1 to pm_StaffMember (pm_staffmemberid)
- N:1 to pm_EvaluationQuestion (pm_questionid)

### 4. Self Evaluation (pm_SelfEvaluation)

**Purpose:** Store quarterly self-assessments by staff members

**Schema Name:** pm_selfevaluation
**Entity Name:** pm_SelfEvaluation
**Display Name:** Self Evaluation
**Collection Name:** Self Evaluations
**Ownership:** UserOwned
**Entity Set Name:** pm_selfevaluations

**Custom Fields:**
| Logical Name | Type | Display Name | Length | Required | Notes |
|--------------|------|--------------|--------|----------|-------|
| pm_name | nvarchar | Name | 200 | Yes | Primary name - "Quarter X FY YYYY" |
| pm_staffmemberid | lookup | Staff Member | - | Yes | → pm_StaffMember |
| pm_questionid | lookup | Question | - | Yes | → pm_EvaluationQuestion |
| pm_quarter | int | Quarter | - | Yes | 1-4 |
| pm_fiscalyear | int | Fiscal Year | - | Yes | YYYY |
| pm_rating | int | Self Rating | - | No | 1-5 scale |
| pm_notes | memo | Comments | 4000 | No | Self-assessment notes |
| pm_completeddate | datetime | Completed Date | - | No | When self-eval completed |
| pm_status | picklist | Status | - | No | Pending/Complete |

**Picklist Values (pm_status):**
- 1: Pending
- 2: In Progress
- 3: Completed

**Relationships:**
- 6 system relationships
- N:1 to pm_StaffMember (pm_staffmemberid)
- N:1 to pm_EvaluationQuestion (pm_questionid)

### 5. IDP Entry (pm_IDPEntry)

**Purpose:** Individual Development Plan entries for staff growth tracking

**Schema Name:** pm_idpentry
**Entity Name:** pm_IDPEntry
**Display Name:** IDP Entry
**Collection Name:** IDP Entries
**Ownership:** UserOwned
**Entity Set Name:** pm_idpentries

**Custom Fields:**
| Logical Name | Type | Display Name | Length | Required | Notes |
|--------------|------|--------------|--------|----------|-------|
| pm_title | nvarchar | Title | 200 | Yes | Primary name - development goal title |
| pm_staffmemberid | lookup | Staff Member | - | Yes | → pm_StaffMember |
| pm_description | memo | Description | 4000 | No | Goal details |
| pm_targetdate | datetime | Target Date | - | No | When to achieve |
| pm_status | picklist | Status | - | No | Not Started/In Progress/Complete |
| pm_progress | int | Progress % | - | No | 0-100 |
| pm_notes | memo | Notes | 4000 | No | Progress updates |

**Picklist Values (pm_status):**
- 1: Not Started
- 2: In Progress
- 3: Completed
- 4: Cancelled

**Relationships:**
- 6 system relationships
- N:1 to pm_StaffMember (pm_staffmemberid)

### 6. Meeting Note (pm_MeetingNote)

**Purpose:** Document one-on-one meeting discussions and outcomes

**Schema Name:** pm_meetingnote
**Entity Name:** pm_MeetingNote
**Display Name:** Meeting Note
**Collection Name:** Meeting Notes
**Ownership:** UserOwned
**Entity Set Name:** pm_meetingnotes

**Custom Fields:**
| Logical Name | Type | Display Name | Length | Required | Notes |
|--------------|------|--------------|--------|----------|-------|
| pm_name | nvarchar | Name | 200 | Yes | Primary name - "Meeting with [Staff] - [Date]" |
| pm_staffmemberid | lookup | Staff Member | - | Yes | → pm_StaffMember |
| pm_meetingdate | datetime | Meeting Date | - | Yes | When meeting occurred |
| pm_discussiontopics | memo | Discussion Topics | 4000 | No | What was discussed |
| pm_actionitems | memo | Action Items | 4000 | No | Follow-up items |
| pm_nextmeetingdate | datetime | Next Meeting Date | - | No | Scheduled next meeting |
| pm_notes | memo | Additional Notes | 4000 | No | Other comments |

**Relationships:**
- 6 system relationships
- N:1 to pm_StaffMember (pm_staffmemberid)
- 1:N to pm_ActionItem (meeting has action items)

### 7. Goal (pm_Goal)

**Purpose:** Track performance objectives and goals

**Schema Name:** pm_goal
**Entity Name:** pm_Goal
**Display Name:** Goal
**Collection Name:** Goals
**Ownership:** UserOwned
**Entity Set Name:** pm_goals

**Custom Fields:**
| Logical Name | Type | Display Name | Length | Required | Notes |
|--------------|------|--------------|--------|----------|-------|
| pm_title | nvarchar | Title | 200 | Yes | Primary name - goal title |
| pm_staffmemberid | lookup | Staff Member | - | Yes | → pm_StaffMember |
| pm_description | memo | Description | 4000 | No | Goal details |
| pm_startdate | datetime | Start Date | - | No | Goal start |
| pm_targetdate | datetime | Target Date | - | No | Goal deadline |
| pm_status | picklist | Status | - | No | Not Started/In Progress/Complete |
| pm_priority | picklist | Priority | - | No | High/Medium/Low |
| pm_progress | int | Progress % | - | No | 0-100 |
| pm_notes | memo | Notes | 4000 | No | Progress updates |

**Picklist Values (pm_status):**
- 1: Not Started
- 2: In Progress
- 3: Completed
- 4: Cancelled

**Picklist Values (pm_priority):**
- 1: Low
- 2: Medium
- 3: High

**Relationships:**
- 6 system relationships
- N:1 to pm_StaffMember (pm_staffmemberid)

### 8. Recognition (pm_Recognition)

**Purpose:** Log positive feedback and recognition

**Schema Name:** pm_recognition
**Entity Name:** pm_Recognition
**Display Name:** Recognition
**Collection Name:** Recognition Entries
**Ownership:** UserOwned
**Entity Set Name:** pm_recognitions

**Custom Fields:**
| Logical Name | Type | Display Name | Length | Required | Notes |
|--------------|------|--------------|--------|----------|-------|
| pm_recognitiontext | nvarchar | Recognition | 500 | Yes | Primary name - what they did well |
| pm_staffmemberid | lookup | Staff Member | - | Yes | → pm_StaffMember |
| pm_recognitiondate | datetime | Recognition Date | - | Yes | When it happened |
| pm_category | picklist | Category | - | No | Type of recognition |
| pm_details | memo | Details | 4000 | No | Additional context |

**Picklist Values (pm_category):**
- 1: Excellence
- 2: Teamwork
- 3: Innovation
- 4: Customer Service
- 5: Leadership
- 6: Going Above and Beyond

**Relationships:**
- 6 system relationships
- N:1 to pm_StaffMember (pm_staffmemberid)

### 9. Action Item (pm_ActionItem)

**Purpose:** Track follow-up actions from meetings and evaluations

**Schema Name:** pm_actionitem
**Entity Name:** pm_ActionItem
**Display Name:** Action Item
**Collection Name:** Action Items
**Ownership:** UserOwned
**Entity Set Name:** pm_actionitems

**Custom Fields:**
| Logical Name | Type | Display Name | Length | Required | Notes |
|--------------|------|--------------|--------|----------|-------|
| pm_title | nvarchar | Title | 200 | Yes | Primary name - action item description |
| pm_staffmemberid | lookup | Staff Member | - | Yes | → pm_StaffMember |
| pm_meetingnoteid | lookup | Meeting Note | - | No | → pm_MeetingNote (optional) |
| pm_description | memo | Description | 4000 | No | Action details |
| pm_duedate | datetime | Due Date | - | No | When due |
| pm_status | picklist | Status | - | No | Not Started/In Progress/Complete |
| pm_priority | picklist | Priority | - | No | High/Medium/Low |
| pm_completeddate | datetime | Completed Date | - | No | When completed |
| pm_notes | memo | Notes | 4000 | No | Updates/comments |

**Picklist Values (pm_status):**
- 1: Not Started
- 2: In Progress
- 3: Completed
- 4: Cancelled

**Picklist Values (pm_priority):**
- 1: Low
- 2: Medium
- 3: High

**Relationships:**
- 6 system relationships
- N:1 to pm_StaffMember (pm_staffmemberid)
- N:1 to pm_MeetingNote (pm_meetingnoteid)

---

## Relationship Summary

### System Relationships (6 per entity × 9 entities = 54 total)

Every entity has these 6 relationships:
1. business_unit_pm_entityname
2. lk_pm_entityname_createdby
3. lk_pm_entityname_modifiedby
4. owner_pm_entityname
5. team_pm_entityname
6. user_pm_entityname

### Custom Entity Relationships (13 total)

| Relationship Name | Type | From Entity | To Entity | Field | Cascade Delete |
|-------------------|------|-------------|-----------|-------|----------------|
| pm_staffmember_weeklyevaluation | 1:N | StaffMember | WeeklyEvaluation | pm_staffmemberid | RemoveLink |
| pm_evaluationquestion_weeklyevaluation | 1:N | EvaluationQuestion | WeeklyEvaluation | pm_questionid | RemoveLink |
| pm_staffmember_selfevaluation | 1:N | StaffMember | SelfEvaluation | pm_staffmemberid | RemoveLink |
| pm_evaluationquestion_selfevaluation | 1:N | EvaluationQuestion | SelfEvaluation | pm_questionid | RemoveLink |
| pm_staffmember_idpentry | 1:N | StaffMember | IDPEntry | pm_staffmemberid | RemoveLink |
| pm_staffmember_meetingnote | 1:N | StaffMember | MeetingNote | pm_staffmemberid | RemoveLink |
| pm_staffmember_goal | 1:N | StaffMember | Goal | pm_staffmemberid | RemoveLink |
| pm_staffmember_recognition | 1:N | StaffMember | Recognition | pm_staffmemberid | RemoveLink |
| pm_staffmember_actionitem | 1:N | StaffMember | ActionItem | pm_staffmemberid | RemoveLink |
| pm_meetingnote_actionitem | 1:N | MeetingNote | ActionItem | pm_meetingnoteid | RemoveLink |

**Total Relationships: 67**
- 54 system relationships
- 13 custom relationships

---

## Workflows (Power Automate Flows)

### 1. Weekly Evaluation Reminder

**File:** Workflows/WeeklyEvaluationReminder.json
**Trigger:** Recurrence - Every Monday at 8:00 AM CST
**Purpose:** Email supervisors with weekly evaluation suggestions

**Logic:**
1. Get current week number
2. Calculate rotation (week × 2) % 12 for questions
3. List active staff members
4. Calculate which 2 staff to evaluate
5. Retrieve the 2 questions for this week
6. Send email to each supervisor with their assignments

**Connections:**
- Dataverse for Teams
- Office 365 Outlook

### 2. Quarterly Self Evaluation Reminder

**File:** Workflows/QuarterlySelfEvalReminder.json
**Trigger:** Recurrence - 1st of month (Jan, Apr, Jul, Oct) at 9:00 AM
**Purpose:** Remind staff to complete quarterly self-evaluations

**Logic:**
1. Determine current quarter and fiscal year
2. List all active staff members
3. For each staff member:
   - Check if self-evals for this quarter exist
   - If not, send reminder email
   - Include link to self-eval form

**Connections:**
- Dataverse for Teams
- Office 365 Outlook
- Office 365 Users (for user profile data)

### 3. One-on-One Meeting Notification

**File:** Workflows/OneOnOneMeetingNotification.json
**Trigger:** When calendar event created/modified (one-on-one meetings)
**Purpose:** Send meeting prep notification 15 minutes before

**Logic:**
1. Check if calendar event is one-on-one (1 attendee)
2. Lookup staff member by email
3. Fetch recent performance data:
   - Last 4 weeks of evaluations
   - Recent meeting notes
   - Open action items
4. Send summary email 15 mins before meeting

**Connections:**
- Office 365 Calendar
- Dataverse for Teams
- Office 365 Outlook

### 4. Ad Hoc Self Evaluation Request

**File:** Workflows/AdHocSelfEvalRequest.json
**Trigger:** Manual HTTP request
**Purpose:** Allow supervisors to request off-cycle self-evaluation

**Logic:**
1. Receive HTTP request with staff member name
2. Lookup staff member record
3. Create pending self-evaluation records (all 12 questions)
4. Send email to staff member requesting completion
5. Return HTTP 200 success or 500 error

**Connections:**
- HTTP Request (trigger)
- Dataverse for Teams
- Office 365 Outlook

---

## Canvas App Specification

**App Name:** pm_performancemanagement_12345
**Form Factor:** Tablet (1366x768)
**Target:** Desktop and tablet users
**Status:** Design specification (manual rebuild required)

**Note:** Canvas apps cannot be included in Dataverse for Teams solution packages. The app must be manually recreated in Power Apps Studio following the specs in `solution/CanvasApps/README.md`.

**9 Screens:**
1. Dashboard - Week at a glance, quick stats
2. Weekly Evaluations - Complete supervisor ratings
3. Quarterly Self-Eval - Staff self-assessment
4. Meeting Notes - One-on-one documentation
5. IDP Tracking - Development plans
6. Goals - Performance objectives
7. Action Items - Follow-ups
8. Recognition - Positive feedback log
9. Admin - Manage evaluation questions

---

## File Structure

```
solution/
├── [Content_Types].xml
├── Other/
│   ├── Solution.xml
│   └── Customizations.xml (8,000-12,000 lines expected)
├── CanvasApps/
│   ├── pm_performancemanagement_12345_DocumentUri.msapp
│   └── pm_performancemanagement_12345_BackgroundImageUri
└── Workflows/
    ├── WeeklyEvaluationReminder.json
    ├── QuarterlySelfEvalReminder.json
    ├── OneOnOneMeetingNotification.json
    └── AdHocSelfEvalRequest.json
```

---

## Implementation Approach

### Phase 1: Core Structure (Priority 1)
1. Create new solution.xml with correct metadata
2. Create new [Content_Types].xml
3. Build customizations.xml shell structure

### Phase 2: Entity Definitions (Priority 1)
For each of 9 entities:
1. Create entity with all 30+ metadata attributes
2. Add primary key field (with MaxLength=100)
3. Add primary name field (with all required metadata)
4. Add all 17 system fields
5. Add custom business fields
6. Add 6 system relationships
7. Add custom relationships (if any)

Use template-based approach with exact Microsoft patterns.

### Phase 3: Relationships (Priority 1)
1. Verify all 54 system relationships created
2. Create 13 custom entity relationships
3. Validate relationship names and cascade behavior

### Phase 4: Canvas App Registration (Priority 2)
1. Register app in RootComponents
2. Create app placeholder files
3. Document manual rebuild requirements

### Phase 5: Workflows (Priority 2)
1. Copy existing workflow JSON files
2. Validate JSON structure
3. Register in RootComponents
4. Document connection reference requirements

### Phase 6: Validation (Priority 1)
1. XML syntax validation (xmllint)
2. Entity count verification
3. Relationship count verification
4. RootComponents count verification
5. Compare against Microsoft samples

### Phase 7: Testing (Priority 1)
1. Pack solution using build script
2. Import to dev Teams environment
3. Fix any import errors
4. Validate entity creation
5. Validate workflows import

---

## Success Criteria

**Solution Package:**
- [ ] Packs without errors
- [ ] All 9 entities present
- [ ] All 67 relationships defined
- [ ] All 4 workflows registered
- [ ] Canvas app registered
- [ ] XML validates against schema

**Import to Teams:**
- [ ] Import completes without errors
- [ ] All 9 tables created in Dataverse
- [ ] All system fields present
- [ ] All custom fields present
- [ ] All relationships created
- [ ] Workflows import successfully
- [ ] Connection references created

**Post-Import:**
- [ ] Can create staff member records
- [ ] Can create evaluation questions
- [ ] Can create weekly evaluations
- [ ] Lookup fields work correctly
- [ ] Workflows can be configured
- [ ] Canvas app can be manually rebuilt

---

## Migration from v1.0.1.0

**Not a Migration - Clean Rebuild:**

This is NOT an upgrade path from v1.0.1.0. This is a complete rebuild as v2.0.0.0. Existing data will NOT migrate automatically.

**If you have existing data:**
1. Export data from v1.0.1.0 manually
2. Import v2.0.0.0 solution
3. Import data back manually
4. Rebuild canvas app

**Recommended:** Start fresh in new Teams environment.

---

## Known Limitations

1. **Canvas App Not Included:** Must be manually rebuilt in Power Apps Studio
2. **No Data Migration:** Existing data does not automatically transfer
3. **Workflows Require Configuration:** Connection references must be set up post-import
4. **Manual Question Entry:** 12 evaluation questions must be manually added
5. **Teams Environment Only:** Designed specifically for Dataverse for Teams

---

## References

- POWER_PLATFORM_SOLUTION_ARCHITECTURE_SPECIFICATION.md (this repository)
- IMPORT-TROUBLESHOOTING-GUIDE.md (ref folder)
- Microsoft sample solutions in ref/ folder
- Original app documentation in docs/ folder

---

**End of Rebuild Design**
