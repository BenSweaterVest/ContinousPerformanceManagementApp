# Performance Management System - Deployment Guide

Complete step-by-step instructions for deploying the Performance Management solution to Dataverse for Teams.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Solution Installation](#solution-installation)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Power Platform CLI**: Latest version
  - Windows: Install via `dotnet tool install --global Microsoft.PowerApps.CLI.Tool`
  - Mac/Linux: Same command

- **.NET SDK**: Version 6.0 or higher
  - Download from https://dotnet.microsoft.com/download

### Required Access

- **Microsoft 365 License**: E3, E5, or equivalent
- **Teams License**: Included with M365
- **Power Apps for Teams**: Included with Teams
- **System Administrator**: Or Environment Maker role in target environment

### Environment Requirements

- Dataverse for Teams environment (created automatically with Teams)
- Minimum 1GB available database capacity
- Network connectivity to Microsoft services

---

## Environment Setup

### Step 1: Create Dataverse for Teams Environment

1. **Open Microsoft Teams**
   - Launch Teams desktop or web app
   - Navigate to a team (or create one for testing)

2. **Add Power Apps to Teams**
   - Click the "+" tab in any channel
   - Search for "Power Apps"
   - Select "Power Apps" app
   - Click "Save"

3. **Create Dataverse for Teams Environment**
   - This happens automatically when you create your first app
   - Click "Create an app" in Power Apps
   - Environment is provisioned in the background (2-5 minutes)

4. **Get Environment Details**
   - Go to https://admin.powerplatform.microsoft.com
   - Click "Environments"
   - Find your Teams environment (named after your team)
   - Click the environment name
   - Copy the "Environment ID" (you'll need this later)

### Step 2: Install Power Platform CLI

**Windows (PowerShell as Administrator):**

```powershell
# Check if .NET SDK is installed
dotnet --version

# If not installed, download from https://dotnet.microsoft.com/download

# Install PAC CLI
dotnet tool install --global Microsoft.PowerApps.CLI.Tool

# Verify installation
pac --version
```

**Mac/Linux:**

```bash
# Check if .NET SDK is installed
dotnet --version

# If not installed, use package manager:
# macOS: brew install dotnet
# Ubuntu: apt install dotnet-sdk-6.0

# Install PAC CLI
dotnet tool install --global Microsoft.PowerApps.CLI.Tool

# Add to PATH (if needed)
export PATH="$PATH:$HOME/.dotnet/tools"

# Verify installation
pac --version
```

---

## Solution Installation

### Step 1: Obtain Solution Files

**Option A: Clone from Git**

```bash
git clone [repository-url]
cd ContinousPerformanceManagementApp
```

**Option B: Download ZIP**

1. Download solution ZIP from repository
2. Extract to local folder
3. Navigate to extracted folder

### Step 2: Pack the Solution

Navigate to the deployment folder and run the pack script:

**Windows:**

```powershell
cd deployment
.\pack-solution.ps1
```

**Mac/Linux:**

```bash
cd deployment
chmod +x *.sh  # Make scripts executable
./pack-solution.sh
```

**Expected Output:**

```
======================================
Performance Management Solution Pack
======================================

Checking for Power Platform CLI...
Found PAC CLI: Microsoft PowerApps CLI Version: 1.x.x

Project root: /path/to/ContinousPerformanceManagementApp

Packing solution...

======================================
SUCCESS: Solution packed!
======================================

Output file: PerformanceManagement_1_0_0_0.zip
Location: /path/to/project
File size: 0.25 MB
```

### Step 3: Authenticate to Environment

```bash
# Using Environment ID
pac auth create --environment YOUR-ENVIRONMENT-ID-HERE

# OR using Environment URL
pac auth create --url https://yourorg.crm.dynamics.com

# Verify authentication
pac auth list
```

**Authentication will open a browser window:**
1. Sign in with your M365 account
2. Consent to requested permissions
3. Return to terminal

### Step 4: Import Solution

**Windows:**

```powershell
.\import-solution.ps1 -EnvironmentId "YOUR-ENVIRONMENT-ID"
```

**Mac/Linux:**

```bash
./import-solution.sh --environment-id "YOUR-ENVIRONMENT-ID"
```

**Expected Output:**

```
========================================
Performance Management Solution Import
========================================

Checking for Power Platform CLI...
Found PAC CLI

Found solution package: PerformanceManagement_1_0_0_0.zip

Authenticated successfully

Starting solution import...
This may take several minutes...

========================================
SUCCESS: Import initiated!
========================================

The solution is being imported asynchronously.
```

### Step 5: Monitor Import Progress

1. Go to https://admin.powerplatform.microsoft.com
2. Select **Environments**
3. Click your environment
4. Go to **Solutions** (in left nav, under Resources)
5. Look for "Performance Management System"
6. Status will show:
   - **Importing** (yellow) - In progress
   - **Installed** (green) - Success
   - **Failed** (red) - Error (check logs)

**Import typically takes 5-15 minutes depending on:**
- Network speed
- Environment load
- Number of components

---

## Post-Deployment Configuration

### Step 1: Configure Connection References

Power Automate flows require connection references to be configured.

1. Go to https://make.powerapps.com
2. Select your environment (top right)
3. Click **Solutions** in left navigation
4. Click **Performance Management System**
5. Click **Connection References** (filter view)

Configure each connection:

**Office 365 Outlook:**
1. Click the connection reference
2. Click **+ New connection**
3. Sign in with your account
4. Click **Create**

**Office 365 Users:**
1. Repeat process above
2. Use same M365 account

**Dataverse (Microsoft Dataverse):**
- Usually auto-configured
- If not, click and select "Dataverse (current environment)"

### Step 2: Load Seed Data

The solution requires 12 evaluation questions to be manually added.

1. Go to https://make.powerapps.com
2. Select your environment
3. Click **Tables** in left nav
4. Search for "Evaluation Question"
5. Click the table
6. Click **+ New row** (12 times)

**Enter these 12 questions:**

1. Demonstrates quality and accuracy in work products
2. Completes assignments within agreed timeframes
3. Communicates effectively with team members and stakeholders
4. Takes initiative to identify and solve problems proactively
5. Demonstrates technical competency in required skills
6. Adapts effectively to changing priorities
7. Collaborates well with others
8. Follows established processes and procedures
9. Demonstrates customer service orientation
10. Pursues professional development and learning
11. Manages workload and priorities effectively
12. Demonstrates dependability and reliability

For each:
- **Question Text**: [Copy from above]
- **Question Number**: 1-12
- **Active**: Yes (checked)

### Step 3: Enable Power Automate Flows

1. Go to https://make.powerautomate.com
2. Select your environment
3. Click **Solutions** in left nav
4. Click **Performance Management System**
5. Click **Cloud flows** (filter)

Enable each flow:

1. **Weekly Evaluation Reminder**
   - Click the flow name
   - Click **Turn on** (top right)
   - Verify: "Your flow is on"

2. **Quarterly Self-Eval Reminder**
   - Repeat above steps

3. **One-on-One Meeting Notification**
   - Repeat above steps
   - Note: Requires Outlook calendar access

4. **Ad Hoc Self-Eval Request**
   - This is an HTTP-triggered flow
   - Leave off unless needed from app

### Step 4: Build/Import Canvas App

The Canvas App must be built in Power Apps Studio following the specifications.

**Option A: Build from Specifications**

1. Open https://make.powerapps.com
2. Click **+ Create** > **Blank app** > **Tablet**
3. Name: "Performance Management System"
4. Follow specifications in `solution/CanvasApps/README.md`
5. Add all data sources
6. Create all 9 screens
7. Implement formulas
8. Test thoroughly
9. Save and publish

**Option B: Import Pre-built .msapp File**

If a pre-built .msapp file is provided:

1. Go to https://make.powerapps.com
2. Click **Apps** in left nav
3. Click **Import canvas app**
4. Upload the .msapp file
5. Complete import wizard
6. Open app and verify data connections

### Step 5: Share the App

1. Go to https://make.powerapps.com
2. Select your environment
3. Click **Apps**
4. Find "Performance Management System"
5. Click **...** (more options)
6. Click **Share**
7. Add supervisors:
   - Enter email addresses
   - Select permission: **Can use**
   - Include security group if available
8. Click **Share**

Supervisors will receive an email with app link.

### Step 6: Add Staff Members

Supervisors should add their staff:

1. Open the app
2. Navigate to **Staff List** screen
3. Click **+ Add Staff**
4. Enter:
   - Name
   - Employee ID
   - Position Title
   - Start Date
   - Supervisor (auto-set to current user)
   - Status: Active
5. Click **Save**

---

## Testing

### Functional Test Checklist

Perform these tests to verify deployment:

#### ✅ Authentication & Access
- [ ] Can log into app
- [ ] Correct environment selected
- [ ] No permission errors

#### ✅ Data Operations
- [ ] Can create staff member
- [ ] Can view staff list
- [ ] Can edit staff member
- [ ] Can view evaluation questions

#### ✅ Weekly Evaluations
- [ ] Dashboard displays
- [ ] This week's suggestions shown
- [ ] Can select staff member
- [ ] Can select question
- [ ] Can rate (1-5 + Insufficient Data)
- [ ] Can save evaluation
- [ ] Recent evaluations display

#### ✅ Rotation Algorithm
- [ ] Suggestions change weekly
- [ ] Different staff/questions rotate
- [ ] No errors in calculations

#### ✅ Quarterly Self-Evaluations
- [ ] Can access self-eval screen
- [ ] All 12 questions display
- [ ] Can rate each question
- [ ] Can add notes
- [ ] Can save

#### ✅ One-on-Ones
- [ ] Can create meeting note
- [ ] Can select staff member
- [ ] Can enter agenda
- [ ] Can save notes
- [ ] Recent meetings display

#### ✅ Flows
- [ ] Weekly reminder sent (test on Monday)
- [ ] Quarterly reminder triggers (test date logic)
- [ ] Meeting notification works

---

## Troubleshooting

### Common Issues

#### Issue: "pac command not found"

**Solution:**

```bash
# Reinstall PAC CLI
dotnet tool uninstall --global Microsoft.PowerApps.CLI.Tool
dotnet tool install --global Microsoft.PowerApps.CLI.Tool

# Add to PATH (Mac/Linux)
export PATH="$PATH:$HOME/.dotnet/tools"

# Add to PATH (Windows - permanently)
$env:PATH += ";$env:USERPROFILE\.dotnet\tools"
```

#### Issue: Solution pack fails with XML errors

**Solution:**

1. Validate XML files:
```bash
xmllint solution/Other/Solution.xml
xmllint solution/Tables/*/Entity.xml
```

2. Check for:
   - Missing closing tags
   - Invalid characters
   - Incorrect schema

3. Review error messages for specific files

#### Issue: Import fails - "Missing dependencies"

**Solution:**

- Ensure target environment has required features enabled
- Check connection references are available
- Verify all table definitions are included

#### Issue: App won't open - "Permission denied"

**Solution:**

1. Verify app is shared with your user
2. Check security roles in Dataverse
3. Ensure environment access

#### Issue: Flows won't turn on

**Solution:**

1. Check connection references are configured
2. Verify all required connections exist
3. Check for flow checker errors
4. Review flow run history for details

#### Issue: Rotation algorithm not working

**Solution:**

1. Verify staff members exist
2. Ensure questions are marked "Active"
3. Check OnStart formula in app
4. Test with debug output

#### Issue: Data not showing in app

**Solution:**

1. Check data sources are connected
2. Verify delegation warnings
3. Check filters on galleries
4. Reload data connections

### Getting More Help

If issues persist:

1. **Check Power Platform Admin Center**
   - View operation logs
   - Check service health

2. **Review Flow Run History**
   - Identify failed steps
   - View error messages

3. **Use Monitor Tool in Power Apps**
   - Debug formulas
   - View API calls

4. **Microsoft Documentation**
   - https://docs.microsoft.com/power-platform/
   - https://docs.microsoft.com/powerapps/
   - https://docs.microsoft.com/power-automate/

5. **Community Forums**
   - https://powerusers.microsoft.com/
   - Post detailed error messages

---

## Rollback Procedure

If you need to remove the solution:

1. Go to https://admin.powerplatform.microsoft.com
2. Select your environment
3. Go to **Solutions**
4. Select **Performance Management System**
5. Click **Delete**
6. Confirm deletion

**Warning:** This removes all:
- Tables and data
- Canvas app
- Power Automate flows
- Cannot be undone (backup data first)

---

## Success Checklist

Before considering deployment complete:

- [x] Solution imported successfully
- [x] All connection references configured
- [x] 12 evaluation questions loaded
- [x] Power Automate flows enabled
- [x] Canvas app accessible
- [x] App shared with supervisors
- [x] At least one staff member created
- [x] Test evaluation completed
- [x] Dashboard displays correctly
- [x] Documentation reviewed

---

**Deployment complete! Users can now access the Performance Management System.**
