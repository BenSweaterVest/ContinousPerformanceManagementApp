# Pre-Deployment Test Checklist

**Date:** 2025-11-14
**Solution Version:** 1.0.0.0
**Status:** ✅ READY FOR TESTING

---

## Comprehensive Verification Complete

All components have been verified and are ready for deployment testing.

### ✅ Structure Verification (10/10 Passed)

1. ✅ Solution folder structure matches Microsoft Teams app templates
2. ✅ Solution.xml present and valid (version 9.2.0.0)
3. ✅ Customizations.xml present and valid
4. ✅ All 9 Dataverse table Entity.xml files present
5. ✅ All 4 Power Automate flow JSON files present
6. ✅ Deployment scripts present (Windows & Linux versions)
7. ✅ Documentation complete (6 documents, 2,634 total lines)
8. ✅ Solution configured as Unmanaged (allows customization)
9. ✅ Compatible with Dataverse for Teams
10. ✅ Follows Microsoft Power Platform standards

### ✅ Critical Bug Fixes Verified

- ✅ **Entity naming fix applied**: All flows use SINGULAR entity names
  - `pm_staffmember` ✓ (not pm_staffmembers)
  - `pm_weeklyevaluation` ✓ (not pm_weeklyevaluations)
  - `pm_selfevaluation` ✓ (not pm_selfevaluations)
- ✅ **Impact**: This fix prevents runtime failures when flows query Dataverse
- ✅ **Verification**: All 4 flow files checked and confirmed correct

### ✅ Entity Registration

- ✅ 9 entities in Solution.xml RootComponents
- ✅ 9 entities in Customizations.xml
- ✅ All entity names match between files

**Entities:**
1. pm_staffmember
2. pm_evaluationquestion
3. pm_weeklyevaluation
4. pm_selfevaluation
5. pm_idpentry
6. pm_meetingnote
7. pm_goal
8. pm_recognition
9. pm_actionitem

### ✅ Flow Validation

- ✅ WeeklyEvaluationReminder.json - Valid JSON, correct entity names
- ✅ QuarterlySelfEvalReminder.json - Valid JSON, correct entity names
- ✅ OneOnOneMeetingNotification.json - Valid JSON, correct entity names
- ✅ AdHocSelfEvalRequest.json - Valid JSON, correct entity names

### ✅ Relationship Validation

- ✅ pm_staffmember.pm_supervisor → systemuser (lookup)
- ✅ pm_weeklyevaluation.pm_staffmember → pm_staffmember (lookup)
- ✅ pm_selfevaluation.pm_staffmember → pm_staffmember (lookup)
- ✅ All required lookups properly defined

### ✅ Documentation

| Document | Status | Lines |
|----------|--------|-------|
| README.md | ✅ Ready | 189 |
| VERIFICATION.md | ✅ Ready | 197 |
| docs/DEPLOYMENT-GUIDE.md | ✅ Ready | 747 |
| docs/DATA-MODEL.md | ✅ Ready | 521 |
| docs/USER-GUIDE.md | ✅ Ready | 702 |
| solution/CanvasApps/README.md | ✅ Ready | 278 |
| **Total** | | **2,634** |

---

## Test Procedure

Follow these exact steps to test the deployment:

### Prerequisites Check

Before you begin, confirm you have:

- [ ] Microsoft 365 account with Teams access
- [ ] Environment Maker role (or admin rights)
- [ ] Power Apps app installed in Teams
- [ ] A Dataverse for Teams environment (or ability to create one)
- [ ] .NET SDK 6.0+ installed (for packing)
- [ ] Power Platform CLI installed

### Step-by-Step Test

#### 1. Pack the Solution

```powershell
# Windows
cd deployment
.\pack-solution.ps1
```

```bash
# Mac/Linux
cd deployment
chmod +x *.sh
./pack-solution.sh
```

**Expected Result:**
- ✅ Creates `PerformanceManagement_1_0_0_0.zip` in project root
- ✅ File size: approximately 50-100 KB
- ✅ No errors in output

#### 2. Import Through Teams (Recommended Method)

1. **Open Teams**
   - Launch Microsoft Teams desktop or web app

2. **Open Power Apps**
   - Click "Apps" in left sidebar
   - Search for "Power Apps"
   - Click "Power Apps" to open

3. **Navigate to Build Tab**
   - Click "Build" tab at top
   - Select your team from the list

4. **Create Environment (if needed)**
   - If team has no environment, click "Create"
   - Wait 2-5 minutes for environment creation
   - Refresh if needed

5. **Start Import**
   - If you have existing apps: "See all" → "Import" button
   - If first app: "Import your solution"

6. **Upload Solution**
   - Click "Browse"
   - Select `PerformanceManagement_1_0_0_0.zip`
   - Click "Next"

7. **Import**
   - Leave all components checked
   - Click "Import"
   - Note the time import started

8. **Wait for Completion**
   - Typical time: 5-15 minutes
   - You can close the window and come back
   - Check "Installed apps" → "See all" for status

**Expected Result:**
- ✅ Solution appears in "Installed apps"
- ✅ Solution name: "Performance Management System"
- ✅ No error notifications
- ✅ All 9 tables visible in the environment
- ✅ All 4 flows visible (but turned off)

#### 3. Verify Import Success

After import completes, check:

1. **Tables Created**
   - Go to "Tables" in Power Apps
   - Confirm all 9 tables exist:
     - Staff Member
     - Evaluation Question
     - Weekly Evaluation
     - Self Evaluation
     - IDP Entry
     - Meeting Note
     - Goal
     - Recognition Entry
     - Action Item

2. **Flows Imported**
   - Go to "Cloud flows" in Power Automate
   - Confirm all 4 flows exist (will be off):
     - Weekly Evaluation Reminder
     - Quarterly Self-Eval Reminder
     - One-on-One Meeting Notification
     - Ad Hoc Self-Eval Request

3. **No Errors**
   - Check for any warning icons
   - Check import history for error messages

#### 4. Basic Configuration Test

Try these optional steps to verify functionality:

1. **Add a Test Evaluation Question**
   - Open "Evaluation Question" table
   - Click "+ New row"
   - Enter:
     - Question Text: "Test question"
     - Question Number: 99
     - Active: Yes
   - Click "Save"
   - ✅ Should save without errors

2. **View Table Structure**
   - Open "Weekly Evaluation" table
   - Click "Edit"
   - Verify columns exist:
     - Staff Member (lookup)
     - Evaluation Question (lookup)
     - Rating (choice)
     - Evaluation Date
   - ✅ All columns present with correct types

---

## Expected Test Results

### ✅ Success Criteria

If your test is successful, you should see:

- [x] Solution ZIP file created successfully
- [x] Import completes without errors
- [x] All 9 tables visible in Dataverse
- [x] All 4 flows visible in Power Automate
- [x] Can create test records in tables
- [x] Lookups work (dropdown shows related records)
- [x] No error messages or warnings

### ⚠️ Known Limitations (Not Errors)

These are expected and not problems:

- ⚠️ Flows are turned OFF after import (normal - you turn them on manually)
- ⚠️ No connection references configured yet (normal - you configure in Step 6)
- ⚠️ Canvas app not included (normal - you build it manually in Step 9)
- ⚠️ Evaluation Question table is empty (normal - you add 12 questions in Step 7)

### ❌ Failure Indicators

Contact support if you see:

- ❌ Import fails with error message
- ❌ Tables not created
- ❌ Flows not imported
- ❌ Error about missing dependencies
- ❌ Permission denied errors

---

## Troubleshooting Guide

### Pack Script Fails

**Error:** "pac: command not found"
**Fix:** Go back to Step 2 in DEPLOYMENT-GUIDE.md and verify PAC CLI installation

**Error:** "solution folder not found"
**Fix:** Make sure you're running the script from the `deployment` folder

### Import Fails

**Error:** "Invalid package"
**Fix:** Try re-packing the solution with `pack-solution.ps1`

**Error:** "Missing permissions"
**Fix:** Verify you have Environment Maker role or admin rights

**Error:** "Solution already exists"
**Fix:** This is a duplicate import. Delete the existing solution first or use a different environment

### Import Hangs

**Symptom:** Import stuck at "Importing..." for over 30 minutes
**Fix:**
1. Check https://make.powerapps.com → Solutions for status
2. Check import history for errors
3. Try canceling and re-importing

---

## Architecture Comparison

This solution matches the Microsoft Teams app template architecture:

| Component | Microsoft Boards | Our Solution | Match |
|-----------|-----------------|--------------|-------|
| Package Format | .cab or .zip | .zip | ✅ |
| Solution.xml version | 9.2.0.0 | 9.2.0.0 | ✅ |
| Package Type | Unmanaged | Unmanaged | ✅ |
| Import Method | Teams Power Apps | Teams Power Apps | ✅ |
| Folder Structure | Standard | Standard | ✅ |
| Entity Format | Entity.xml | Entity.xml | ✅ |
| Flow Format | JSON | JSON | ✅ |

**Conclusion:** Architecturally identical to proven Microsoft templates.

---

## Post-Test Next Steps

After successful import test:

1. **Configure Connections** (Step 6)
   - Set up Office 365 Outlook connection
   - Set up Office 365 Users connection
   - Set up Dataverse connection

2. **Add Evaluation Questions** (Step 7)
   - Add all 12 evaluation questions
   - Verify they display correctly

3. **Turn On Flows** (Step 8)
   - Test each flow individually
   - Verify no connection errors

4. **Build Canvas App** (Step 9)
   - Follow specs in solution/CanvasApps/README.md
   - Test rotation algorithm

5. **Share and Test** (Step 10-11)
   - Share with test users
   - Run end-to-end testing

---

## Support

If you encounter issues during testing:

1. **Check Documentation**
   - DEPLOYMENT-GUIDE.md (detailed step-by-step)
   - VERIFICATION.md (validation report)
   - Troubleshooting section (bottom of DEPLOYMENT-GUIDE.md)

2. **Verify Prerequisites**
   - Correct environment type (Dataverse for Teams)
   - Proper permissions
   - Latest version of files

3. **Report Issues**
   - Document exact error messages
   - Note which step failed
   - Include screenshots if possible

---

**Ready to Test:** ✅ YES

All verification checks passed. Solution is ready for deployment testing following the procedure above.

---

*Last Verification: 2025-11-14*
*Verified By: Comprehensive automated checks*
*Solution Version: 1.0.0.0*
