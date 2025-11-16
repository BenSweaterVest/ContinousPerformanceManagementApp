# Performance Management System - Data Model

Complete documentation of the Dataverse data model including tables, relationships, and business rules.

## Table of Contents

1. [Overview](#overview)
2. [Entity Relationship Diagram](#entity-relationship-diagram)
3. [Table Specifications](#table-specifications)
4. [Relationships](#relationships)
5. [Business Rules](#business-rules)
6. [Sample Data](#sample-data)

---

## Overview

The Performance Management System uses 9 custom Dataverse tables with the `pm_` prefix. All tables follow standard Dataverse patterns with system fields (Created On, Modified On, Owner, etc.).

### Table Summary

| Table | Logical Name | Primary Purpose | Key Relationships |
|-------|-------------|-----------------|-------------------|
| Staff Member | pm_staffmember | Employee records | → systemuser (Supervisor) |
| Evaluation Question | pm_evaluationquestion | Standard questions | ← Weekly Evaluation, Self Evaluation |
| Weekly Evaluation | pm_weeklyevaluation | Supervisor evaluations | → Staff Member, → Question, → systemuser |
| Self Evaluation | pm_selfevaluation | Employee self-assessments | → Staff Member, → Question |
| IDP Entry | pm_idpentry | Development plans | → Staff Member |
| Meeting Note | pm_meetingnote | 1-on-1 documentation | → Staff Member, → systemuser |
| Goal | pm_goal | Performance objectives | → Staff Member |
| Recognition Entry | pm_recognition | Positive feedback | → Staff Member, → systemuser |
| Action Item | pm_actionitem | Follow-up tasks | → systemuser, → Staff Member (optional) |

---

## Entity Relationship Diagram

```
┌─────────────────┐
│   systemuser    │
│  (Built-in)     │
└────────┬────────┘
         │
         │ Supervisor
         ↓
┌─────────────────────┐          ┌──────────────────────┐
│   Staff Member      │          │ Evaluation Question   │
│   pm_staffmember  │          │ pm_evaluationquestion│
│                     │          │                       │
│ - Name              │          │ - Question Text       │
│ - Employee ID       │          │ - Question Number     │
│ - Position Title    │          │ - Active              │
│ - Start Date        │          └──────────┬────────────┘
│ - Status            │                     │
└──────┬──────────────┘                     │
       │                                    │
       │                                    │
       ├────────────────────────────────────┴──────┐
       │                                            │
       │                                            │
       ↓                                            ↓
┌─────────────────────┐                   ┌────────────────────┐
│  Weekly Evaluation  │                   │  Self Evaluation   │
│ pm_weeklyevaluation│                  │ pm_selfevaluation│
│                      │                  │                    │
│ - Staff Member   ────┘                  │ - Staff Member ────┘
│ - Question       ────────────────────── │ - Question ────────┘
│ - Evaluator                             │ - Rating           │
│ - Rating                                │ - Quarter          │
│ - Notes                                 │ - Fiscal Year      │
│ - Evaluation Date                       │ - Notes            │
└──────────────────────┘                  └────────────────────┘

       │
       │ Staff Member
       │
       ├────────────────┬──────────────────┬──────────────────┐
       ↓                ↓                  ↓                  ↓
┌────────────┐   ┌─────────────┐   ┌──────────┐   ┌─────────────────┐
│ IDP Entry  │   │ Meeting Note│   │   Goal   │   │   Recognition   │
│            │   │             │   │          │   │                 │
│ - Goal Desc│   │ - Supervisor│   │ - Desc   │   │ - Date          │
│ - Target   │   │ - Date      │   │ - Status │   │ - Description   │
│ - Status   │   │ - Agenda    │   │ - %      │   │ - Supervisor    │
│ - Notes    │   │ - Notes     │   │ - Due    │   └─────────────────┘
└────────────┘   └─────────────┘   └──────────┘

                 ┌─────────────────┐
                 │   Action Item   │
                 │                 │
                 │ - Description   │
                 │ - Owner         │
                 │ - Staff (opt)   │
                 │ - Due Date      │
                 │ - Status        │
                 └─────────────────┘
```

---

## Table Specifications

### 1. Staff Member (pm_staffmember)

**Purpose**: Store employee information for staff being evaluated.

**Primary Key**: pm_staffmemberid (GUID)
**Primary Name**: pm_name (Text, 100)

#### Columns

| Column | Type | Length | Required | Description |
|--------|------|--------|----------|-------------|
| pm_name | Text | 100 | Yes | Full name of staff member |
| pm_employeeid | Text | 50 | No | Unique employee identifier |
| pm_positiontitle | Text | 200 | No | Job title |
| pm_supervisor | Lookup | - | No | Lookup to systemuser |
| pm_startdate | Date | - | No | Position start date |
| pm_status | Choice | - | No | 1=Active, 2=Inactive |

#### Views

- **Active Staff Members**: Filters by status = Active, sorted by name

#### Business Rules

- Employee ID should be unique (not enforced at DB level)
- Only active staff appear in app dropdowns
- Supervisor lookup enables row-level security

---

### 2. Evaluation Question (pm_evaluationquestion)

**Purpose**: Store the 12 standardized performance evaluation questions.

**Primary Key**: pm_evaluationquestionid (GUID)
**Primary Name**: pm_questiontext (Multiline Text)

#### Columns

| Column | Type | Length | Required | Description |
|--------|------|--------|----------|-------------|
| pm_questiontext | Multiline Text | 2000 | Yes | The question text |
| pm_questionnumber | Whole Number | - | No | Sequential number (1-12) |
| pm_active | Yes/No | - | No | Is question active? (default: Yes) |

#### Seed Data Required

See DEPLOYMENT-GUIDE.md for the 12 standard questions that must be loaded manually.

#### Business Rules

- Only active questions appear in app dropdowns
- Question numbers should be 1-12
- Rotation algorithm depends on question order

---

### 3. Weekly Evaluation (pm_weeklyevaluation)

**Purpose**: Store supervisor's weekly micro-evaluations of staff performance.

**Primary Key**: pm_weeklyevaluationid (GUID)
**Primary Name**: pm_name (Auto-number: EVAL-{SEQNUM:5})

#### Columns

| Column | Type | Length | Required | Description |
|--------|------|--------|----------|-------------|
| pm_name | Text | 100 | No | Auto-generated ID |
| pm_staffmember | Lookup | - | Yes | → pm_staffmember |
| pm_evaluator | Lookup | - | Yes | → systemuser |
| pm_question | Lookup | - | Yes | → pm_evaluationquestion |
| pm_rating | Choice | - | Yes | 1-5 scale + "Insufficient Data" |
| pm_notes | Multiline Text | 5000 | No | Optional observations |
| pm_evaluationdate | Date | - | Yes | Date of evaluation |
| pm_evaluationtype | Choice | - | No | 1=Weekly Suggested, 2=Ad Hoc |

#### Rating Scale

| Value | Label |
|-------|-------|
| 1 | 1 - Not Satisfactory |
| 2 | 2 - Below Standard |
| 3 | 3 - Meets Standard |
| 4 | 4 - Exceeds Standard |
| 5 | 5 - Exceptional |
| 6 | Insufficient Data |

#### Views

- **Recent Evaluations**: All evaluations, sorted by date descending

#### Business Rules

- Evaluation date defaults to today
- Evaluator defaults to current user
- Rating is required
- One evaluation per staff/question/date (not enforced)

---

### 4. Self Evaluation (pm_selfevaluation)

**Purpose**: Store employee quarterly self-assessments.

**Primary Key**: pm_selfevaluationid (GUID)
**Primary Name**: pm_name (Auto-number: SELF-{SEQNUM:5})

#### Columns

| Column | Type | Length | Required | Description |
|--------|------|--------|----------|-------------|
| pm_name | Text | 100 | No | Auto-generated ID |
| pm_staffmember | Lookup | - | Yes | → pm_staffmember |
| pm_question | Lookup | - | Yes | → pm_evaluationquestion |
| pm_rating | Choice | - | No | 1-5 scale |
| pm_notes | Multiline Text | 5000 | No | Self-reflection notes |
| pm_quarter | Choice | - | Yes | Q1-Q4 (fiscal year) |
| pm_fiscalyear | Whole Number | - | Yes | 4-digit year |
| pm_evaluationtype | Choice | - | No | 1=Quarterly, 2=Ad Hoc |
| pm_completeddate | Date | - | No | When completed |

#### Quarter Options

| Value | Label | Months |
|-------|-------|--------|
| 1 | Q1 (Jul-Sep) | July-September |
| 2 | Q2 (Oct-Dec) | October-December |
| 3 | Q3 (Jan-Mar) | January-March |
| 4 | Q4 (Apr-Jun) | April-June |

#### Business Rules

- Staff should complete all 12 questions each quarter
- Fiscal year runs July-June
- Quarter determined by current month

---

### 5. IDP Entry (pm_idpentry)

**Purpose**: Individual Development Plan goals (employee-owned).

**Primary Key**: pm_idpentryid (GUID)
**Primary Name**: pm_goaldescription (Multiline Text, 500)

#### Columns

| Column | Type | Length | Required | Description |
|--------|------|--------|----------|-------------|
| pm_goaldescription | Multiline Text | 500 | Yes | Development goal |
| pm_staffmember | Lookup | - | Yes | → pm_staffmember |
| pm_targetdate | Date | - | No | Target completion date |
| pm_status | Choice | - | No | Progress status |
| pm_progressnotes | Multiline Text | 5000 | No | Progress updates |

#### Status Options

| Value | Label |
|-------|-------|
| 1 | Not Started |
| 2 | In Progress |
| 3 | Completed |
| 4 | On Hold |

---

### 6. Meeting Note (pm_meetingnote)

**Purpose**: Document one-on-one meeting discussions and outcomes.

**Primary Key**: pm_meetingnoteid (GUID)
**Primary Name**: pm_name (Auto-number: MTG-{SEQNUM:5})

#### Columns

| Column | Type | Length | Required | Description |
|--------|------|--------|----------|-------------|
| pm_name | Text | 100 | No | Auto-generated ID |
| pm_staffmember | Lookup | - | Yes | → pm_staffmember |
| pm_supervisor | Lookup | - | Yes | → systemuser |
| pm_meetingdate | Date | - | Yes | Meeting date |
| pm_agenda | Multiline Text | 5000 | No | Meeting agenda |
| pm_discussionnotes | Multiline Text | 10000 | No | Discussion summary |
| pm_actionitems | Multiline Text | 5000 | No | Follow-up actions |

#### Business Rules

- Meeting date required
- Action items should be copied to Action Item table for tracking
- Link to staff performance history

---

### 7. Goal (pm_goal)

**Purpose**: Track performance and development goals.

**Primary Key**: pm_goalid (GUID)
**Primary Name**: pm_goaldescription (Multiline Text, 500)

#### Columns

| Column | Type | Length | Required | Description |
|--------|------|--------|----------|-------------|
| pm_goaldescription | Multiline Text | 500 | Yes | Goal description |
| pm_staffmember | Lookup | - | Yes | → pm_staffmember |
| pm_status | Choice | - | No | Goal status |
| pm_completionpercentage | Whole Number | - | No | 0-100% |
| pm_duedate | Date | - | No | Target date |

#### Status Options

| Value | Label |
|-------|-------|
| 1 | Not Started |
| 2 | In Progress |
| 3 | Completed |
| 4 | Blocked |

---

### 8. Recognition Entry (pm_recognition)

**Purpose**: Log positive recognition and achievements.

**Primary Key**: pm_recognitionid (GUID)
**Primary Name**: pm_name (Auto-number: REC-{SEQNUM:5})

#### Columns

| Column | Type | Length | Required | Description |
|--------|------|--------|----------|-------------|
| pm_name | Text | 100 | No | Auto-generated ID |
| pm_staffmember | Lookup | - | Yes | → pm_staffmember |
| pm_supervisor | Lookup | - | Yes | → systemuser |
| pm_recognitiondate | Date | - | Yes | Recognition date |
| pm_description | Multiline Text | 5000 | No | What was recognized |

---

### 9. Action Item (pm_actionitem)

**Purpose**: Track follow-up actions from meetings and evaluations.

**Primary Key**: pm_actionitemid (GUID)
**Primary Name**: pm_name (Auto-number: ACT-{SEQNUM:5})

#### Columns

| Column | Type | Length | Required | Description |
|--------|------|--------|----------|-------------|
| pm_name | Text | 100 | No | Auto-generated ID |
| pm_description | Multiline Text | 2000 | Yes | Action description |
| pm_owner | Lookup | - | Yes | → systemuser |
| pm_relatedstaffmember | Lookup | - | No | → pm_staffmember |
| pm_duedate | Date | - | Yes | Due date |
| pm_status | Choice | - | No | Action status |
| pm_completeddate | Date | - | No | When completed |

#### Status Options

| Value | Label |
|-------|-------|
| 1 | Pending |
| 2 | In Progress |
| 3 | Completed |

---

## Relationships

### N:1 Relationships

| From Table | To Table | Relationship Name | Cascade Delete |
|------------|----------|-------------------|----------------|
| pm_staffmember | systemuser | pm_supervisor | Restrict |
| pm_weeklyevaluation | pm_staffmember | pm_staffmember_evaluations | Restrict |
| pm_weeklyevaluation | systemuser | pm_evaluator | Restrict |
| pm_weeklyevaluation | pm_evaluationquestion | pm_question | Restrict |
| pm_selfevaluation | pm_staffmember | pm_staffmember_selfevals | Restrict |
| pm_selfevaluation | pm_evaluationquestion | pm_question | Restrict |
| pm_idpentry | pm_staffmember | pm_staffmember_idp | Restrict |
| pm_meetingnote | pm_staffmember | pm_staffmember_meetings | Restrict |
| pm_meetingnote | systemuser | pm_supervisor | Restrict |
| pm_goal | pm_staffmember | pm_staffmember_goals | Restrict |
| pm_recognition | pm_staffmember | pm_staffmember_recognition | Restrict |
| pm_recognition | systemuser | pm_supervisor | Restrict |
| pm_actionitem | systemuser | pm_owner | Restrict |
| pm_actionitem | pm_staffmember | pm_relatedstaff | Restrict |

### Cascade Behavior

All relationships use **Restrict** cascade delete to prevent accidental data loss. If a staff member needs to be deleted, related records must be handled explicitly.

---

## Business Rules

### Data Integrity

1. **Staff Member Uniqueness**
   - Employee IDs should be unique
   - Consider adding duplicate detection rules

2. **Evaluation Constraints**
   - One weekly evaluation per staff/question/week (recommended)
   - Self-evaluations: 12 questions per quarter (enforced in app)

3. **Date Validations**
   - Start dates cannot be in the future
   - Due dates should be after creation date
   - Meeting dates typically not in future (1-on-1s)

### Security

1. **Row-Level Security**
   - Supervisors see only their supervised staff
   - Staff see only their own records
   - Admins see all records

2. **Field-Level Security**
   - Consider securing sensitive evaluation notes
   - Supervisor notes might be confidential

### Automation

1. **Auto-numbering**
   - Evaluation IDs, Meeting IDs, etc. auto-generate
   - Format: PREFIX-#####

2. **Default Values**
   - Evaluation date: Today
   - Evaluator: Current user
   - Recognition date: Today

---

## Sample Data

### Sample Staff Member

```
Name: John Smith
Employee ID: EMP12345
Position Title: IT Specialist II
Supervisor: Current User
Start Date: 2023-01-15
Status: Active
```

### Sample Weekly Evaluation

```
Evaluation ID: EVAL-00001
Staff Member: John Smith
Evaluator: Jane Manager
Question: Demonstrates quality and accuracy in work products
Rating: 4 - Exceeds Standard
Notes: Consistently delivers high-quality code with minimal defects
Evaluation Date: 2025-01-06
Type: Weekly Suggested
```

### Sample Self Evaluation

```
Self Evaluation ID: SELF-00001
Staff Member: John Smith
Question: Demonstrates quality and accuracy in work products
Rating: 3
Notes: I focus on code quality but sometimes rush under deadlines
Quarter: Q3 (Jan-Mar)
Fiscal Year: 2025
Type: Quarterly
Completed Date: 2025-01-15
```

---

## Data Model Evolution

### Version 2.0.0.7 (Current)

Initial schema with 9 tables and standard relationships.

### Future Considerations

Potential additions:
- **Peer Feedback** table for 360-degree reviews
- **Calibration Session** table for supervisor alignment
- **Performance Rating** calculated table for annual reviews
- **Training Record** table for professional development
- **Attachment** support for evidence files

---

## Database Sizing Estimates

Assuming 20 staff members, 1 supervisor:

| Table | Records/Year | Storage (approx) |
|-------|--------------|------------------|
| Staff Member | 20 | 20 KB |
| Evaluation Question | 12 | 5 KB |
| Weekly Evaluation | 2,080 | 500 KB |
| Self Evaluation | 960 | 200 KB |
| Meeting Notes | 240 | 100 KB |
| Goals | 40 | 20 KB |
| IDP Entries | 40 | 20 KB |
| Recognition | 100 | 50 KB |
| Action Items | 200 | 100 KB |
| **Total** | **~3,700** | **~1 MB** |

Dataverse for Teams provides 2GB, sufficient for 2,000+ years of data!

---

**Data model designed for scalability, security, and performance.**
