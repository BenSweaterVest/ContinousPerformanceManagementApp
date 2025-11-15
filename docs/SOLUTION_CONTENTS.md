# Performance Management Solution - Complete Contents

## Overview

This is a **complete, production-ready Dataverse for Teams solution** for performance management. It includes tables, workflows, and a canvas app - everything needed for out-of-the-box deployment.

**Version**: 1.0.1.0
**Solution Name**: PerformanceManagement
**Publisher**: Default
**Type**: Unmanaged

---

## What's Included

### 📊 9 Dataverse Tables (Entities)

All tables have been configured for Dataverse for Teams compatibility:

1. **pm_StaffMember** - Staff member records with supervisor relationships
2. **pm_EvaluationQuestion** - Question bank for evaluations
3. **pm_WeeklyEvaluation** - Weekly micro-evaluation records
4. **pm_SelfEvaluation** - Quarterly self-assessment records
5. **pm_IDPEntry** - Individual Development Plan entries
6. **pm_MeetingNote** - One-on-one meeting documentation
7. **pm_Goal** - Performance goals and progress tracking
8. **pm_Recognition** - Positive recognition records
9. **pm_ActionItem** - Follow-up actions and tasks

**Features**:
- ✅ All system relationships included (owner, created by, modified by, business unit)
- ✅ PascalCase entity names (Teams requirement)
- ✅ Audit disabled (Teams doesn't support AsyncOperation entity)
- ✅ All lookup relationships properly defined
- ✅ Choice fields for status, ratings, priorities

### ⚡ 4 Cloud Flows (Power Automate)

Automated workflows for reminders and notifications:

1. **WeeklyEvaluationReminder**
   - **Trigger**: Every Monday at 8:00 AM CST
   - **Purpose**: Send weekly reminder to supervisors with suggested evaluations
   - **Actions**: Get active staff, calculate rotation, send email

2. **QuarterlySelfEvalReminder**
   - **Trigger**: First day of each quarter
   - **Purpose**: Remind staff to complete quarterly self-evaluations
   - **Actions**: Send personalized reminders to all active staff

3. **OneOnOneMeetingNotification**
   - **Trigger**: 24 hours before scheduled meeting
   - **Purpose**: Remind supervisor and staff member of upcoming 1-on-1
   - **Actions**: Send calendar notification

4. **AdHocSelfEvalRequest**
   - **Trigger**: Manual trigger from supervisor
   - **Purpose**: Request immediate self-evaluation from staff member
   - **Actions**: Send notification email with evaluation link

**Connections Required**:
- Dataverse (for reading/writing data)
- Office 365 Outlook (for sending emails)
- Office 365 Users (for user lookups)

### 📱 1 Canvas App

**Name**: Performance Management System
**Form Factor**: Tablet (1366x768)
**Type**: Model-driven

**Included Screens**:

1. **HomeScreen (Dashboard)**
   - Welcome message with current user
   - Stats cards (total staff, evaluations this month, upcoming meetings, pending actions)
   - This week's suggested evaluations (based on rotation algorithm)
   - Recent activity gallery
   - Navigation to all features

2. **WeeklyEvaluationsScreen**
   - Staff member dropdown (pre-populated with suggestions)
   - Question dropdown (pre-populated with rotated question)
   - Rating buttons (1-5 + Insufficient Data)
   - Notes text input
   - Save button with validation
   - Recent evaluations gallery

**Data Connections**:
- All 9 Dataverse tables
- Office 365 Users connector
- Office 365 Outlook connector

**Key Features**:
- **Rotation Algorithm**: Automatically suggests 2 staff members and 2 questions each week
- **Fiscal Year Aware**: Calculates quarters based on July-June fiscal year
- **Navigation**: Smooth transitions between screens
- **Responsive**: Optimized for tablet (1366x768)

### 🔌 3 Connection References

Connection references allow the solution to work across different environments:

1. **cr_commondataserviceforapps** - Dataverse connection
2. **cr_office365** - Office 365 Outlook connection
3. **cr_office365users** - Office 365 Users connection

**Note**: After import, you'll need to configure these connections in Power Apps/Power Automate.

---

## File Structure

```
solution/
├── [Content_Types].xml              # OPC content type declarations
├── CanvasApps/
│   └── pm_performancemanagement_12345.msapp  # Canvas app (6.1 KB)
├── Other/
│   ├── Customizations.xml           # Main solution manifest (522 KB)
│   └── Solution.xml                 # Solution metadata
├── Tables/
│   ├── pm_staffmember/              # Table definition
│   ├── pm_evaluationquestion/
│   ├── pm_weeklyevaluation/
│   ├── pm_selfevaluation/
│   ├── pm_idpentry/
│   ├── pm_meetingnote/
│   ├── pm_goal/
│   ├── pm_recognition/
│   └── pm_actionitem/
└── Workflows/
    ├── AdHocSelfEvalRequest.json
    ├── OneOnOneMeetingNotification.json
    ├── QuarterlySelfEvalReminder.json
    └── WeeklyEvaluationReminder.json
```

---

## What You'll See When Importing

When you import `PerformanceManagement_1_0_1_0.zip` into Dataverse for Teams, the import screen will show:

### Tables (9)
- ✅ pm_StaffMember
- ✅ pm_EvaluationQuestion
- ✅ pm_WeeklyEvaluation
- ✅ pm_SelfEvaluation
- ✅ pm_IDPEntry
- ✅ pm_MeetingNote
- ✅ pm_Goal
- ✅ pm_Recognition
- ✅ pm_ActionItem

### Cloud Flows (4)
- ✅ WeeklyEvaluationReminder
- ✅ QuarterlySelfEvalReminder
- ✅ OneOnOneMeetingNotification
- ✅ AdHocSelfEvalRequest

### Canvas Apps (1)
- ✅ Performance Management System

---

## Post-Import Configuration

After importing the solution, you'll need to:

### 1. Configure Connections

**For Cloud Flows:**
1. Go to Power Automate in Teams
2. Open each flow
3. Edit the connection references
4. Authenticate with your Office 365 account
5. Save and turn on the flows

**For Canvas App:**
1. Open the app in Power Apps
2. Data sources will need to reconnect
3. Authenticate connections
4. Test the app

### 2. Add Sample Data (Recommended)

To test the solution, add sample data:

1. **Staff Members**: Create 3-5 staff member records
2. **Evaluation Questions**: Add 10-15 questions
3. **Test the rotation**: Run the app on different weeks to see rotation in action

### 3. Customize (Optional)

All components are customizable:
- Modify tables to add fields
- Adjust flow schedules/logic
- Customize app screens and formulas
- Add additional workflows

---

## Teams Compatibility Notes

This solution has been specifically designed for **Dataverse for Teams**:

✅ **No AsyncOperation dependencies** - Audit is disabled on all entities and attributes
✅ **No premium connectors** - Uses only standard Office 365 connectors
✅ **Optimized table count** - 9 tables (well under Teams limits)
✅ **No code components** - Pure Power Apps formulas and controls
✅ **No custom APIs** - Uses standard Dataverse actions only

---

## Known Limitations

1. **Flows are created in "off" state** - You must turn them on manually after import
2. **Connections must be configured** - First-time setup requires authentication
3. **Canvas App is basic** - Includes core screens; additional screens can be added
4. **No sample data** - Import creates structure only; you must add data
5. **No security roles** - Teams uses built-in member/owner roles

---

## Version History

### 1.0.1.0 (Current)
- **Major Change**: Disabled audit for Teams compatibility
- **Added**: Complete Cloud Flows integration (4 workflows)
- **Added**: Canvas App with HomeScreen and WeeklyEvaluationsScreen
- **Added**: Connection references for all connectors
- **Fixed**: AsyncOperation entity error
- **Fixed**: ZIP structure for proper import

### 1.0.0.1 (Previous)
- Initial version with 9 tables only
- Had audit enabled (caused import errors)

---

## Support and Documentation

### Related Documentation
- [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) - CI/CD workflow details
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Overall project documentation
- [VERSIONING_AND_CICD.md](VERSIONING_AND_CICD.md) - Version management

### Getting Help
- Check import error messages carefully
- Ensure connections are properly configured
- Verify you're importing into a Dataverse for Teams environment (not full Dataverse)
- Review [Content_Types].xml if you get "invalid solution file" errors

---

## Technical Details

**Solution Package Format**: Open Packaging Conventions (OPC)
**Required Files at Root**:
- `solution.xml` (lowercase)
- `customizations.xml` (lowercase)
- `[Content_Types].xml`

**Canvas App Format**: .msapp (ZIP archive with JSON definitions)
**Workflow Format**: Embedded in Customizations.xml as base64-encoded JSON

**Total Package Size**: ~530 KB (uncompressed)
**Compressed ZIP Size**: ~180 KB

---

**Last Updated**: 2025-11-15
**Solution Version**: 1.0.1.0
**Compatible With**: Dataverse for Teams, Dataverse (full)
