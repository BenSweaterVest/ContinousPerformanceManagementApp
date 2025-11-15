# Performance Management System - Deployment Guide

Step-by-step guide to get this thing running in your environment.

## What You'll Need

**Software:**
- .NET SDK 6.0 or higher (to create the solution ZIP file)
- Power Platform CLI (same - used to pack the solution)
- Git (optional, for cloning the repo)

**Note:** If you already have the ZIP file (`PerformanceManagement_1_0_0_0.zip`), you don't need any of the above - just use the UI import method in Step 5!

**Access:**
- Microsoft 365 account (E3, E5, or similar)
- Teams access
- Admin rights in your target environment (or Environment Maker role)

**Time:** Plan for about 2-3 hours total:
- Setup & packing: 30 minutes (or 0 if you have the ZIP already)
- Solution import: 15 minutes
- Configuration: 30 minutes
- Canvas app build: 1-2 hours
- Testing: 30 minutes

---

## Step 1: Get the Solution

**Option A: Download from Releases (Recommended)**

1. Go to the GitHub repository Releases page
2. Download the latest `PerformanceManagement_1_0_0_0.zip` file
3. Skip to Step 5 (Import the Solution) - you're done!

**Option B: Build from Source**

If you want to customize the solution before deploying:

1. Clone or download the repository
2. Extract somewhere you can find it
3. Open terminal/PowerShell in that folder
4. Continue to Step 2 to pack the solution

---

## Step 2: Install Prerequisites

You need two tools: .NET SDK (to install tools) and Power Platform CLI (to deploy the solution).

### Install .NET SDK

The Power Platform CLI is distributed as a .NET tool, so you need .NET SDK first.

**Check if you already have it:**
```bash
dotnet --version
```

**If you see version 6.0 or higher** → You're good, skip ahead to "Install Power Platform CLI"

**If you see "command not found"** → Continue below:

#### Windows

1. Go to https://dotnet.microsoft.com/download
2. Download ".NET 6.0 SDK" (or any version 6.0+)
3. Run the installer (follow the wizard)
4. **Close and reopen your terminal** (important!)
5. Verify it worked:
   ```bash
   dotnet --version
   ```
   Should show something like `6.0.XXX` or `7.0.XXX` or `8.0.XXX`

#### Mac

If you have Homebrew:
```bash
brew install dotnet-sdk
```

If you don't have Homebrew, download from https://dotnet.microsoft.com/download

**Verify:**
```bash
dotnet --version
```

#### Linux

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y dotnet-sdk-6.0
```

**Fedora:**
```bash
sudo dnf install dotnet-sdk-6.0
```

**Other distros:** Check https://learn.microsoft.com/en-us/dotnet/core/install/linux

**Verify:**
```bash
dotnet --version
```

---

### Install Power Platform CLI

Now install the Power Platform CLI using .NET:

```bash
dotnet tool install --global Microsoft.PowerApps.CLI.Tool
```

**You should see:**
```
You can invoke the tool using the following command: pac
Tool 'microsoft.powerapps.cli.tool' (version 'X.X.X') was successfully installed.
```

**Now verify it works:**
```bash
pac --version
```

**If you get "pac: command not found"** → Continue to PATH setup below.

**If you see version number** (like "Microsoft PowerApps CLI Version: 1.x.x") → You're done! Skip to Step 3.

---

### Fix PATH (if pac command not found)

The `pac` command is installed to your .NET tools folder, but your terminal might not know where to find it.

#### Windows PowerShell

**For current session only:**
```powershell
$env:PATH += ";$env:USERPROFILE\.dotnet\tools"
```

**To make it permanent:** (recommended)
1. Press Windows key, search "Environment Variables"
2. Click "Edit the system environment variables"
3. Click "Environment Variables" button
4. Under "User variables", select "Path", click "Edit"
5. Click "New"
6. Add: `%USERPROFILE%\.dotnet\tools`
7. Click OK on everything
8. Close and reopen PowerShell

**Verify:**
```powershell
pac --version
```

#### Mac/Linux

**For current session only:**
```bash
export PATH="$PATH:$HOME/.dotnet/tools"
```

**To make it permanent:** (recommended)

Add to your shell profile. Which file depends on your shell:

```bash
# If you use bash (most common on Linux):
echo 'export PATH="$PATH:$HOME/.dotnet/tools"' >> ~/.bashrc
source ~/.bashrc

# If you use zsh (default on macOS):
echo 'export PATH="$PATH:$HOME/.dotnet/tools"' >> ~/.zshrc
source ~/.zshrc
```

**Verify:**
```bash
pac --version
```

Should show: "Microsoft PowerApps CLI Version: 1.x.x"

---

### Still not working?

**Try these:**

1. **Verify .NET tools location exists:**
   ```bash
   # Windows:
   dir $env:USERPROFILE\.dotnet\tools

   # Mac/Linux:
   ls ~/.dotnet/tools
   ```
   You should see a `pac` file (or `pac.exe` on Windows)

2. **Reinstall PAC CLI:**
   ```bash
   dotnet tool uninstall --global Microsoft.PowerApps.CLI.Tool
   dotnet tool install --global Microsoft.PowerApps.CLI.Tool
   ```

3. **Try the full path:**
   ```bash
   # Windows:
   $env:USERPROFILE\.dotnet\tools\pac.exe --version

   # Mac/Linux:
   ~/.dotnet/tools/pac --version
   ```
   If this works, it's definitely a PATH issue.

If you're still stuck, check the troubleshooting section at the bottom of this guide

---

## Step 3: Set Up Your Dataverse for Teams Environment

You need a Dataverse environment to deploy to. The easiest way is to let Teams create one for you.

### Create Environment Using Power Apps in Teams

**If you already have a Dataverse for Teams environment**, skip to Step 4.

**To create a new environment:**

1. **Open Microsoft Teams**
2. **Install the Power Apps app:**
   - Click "Apps" in the left sidebar
   - Search for "Power Apps"
   - Click "Add" to install it
3. **Create your environment:**
   - Open the Power Apps app
   - Click the "Build" tab
   - Select a team from the list (or create a new team first)
   - Click "Create" when prompted
   - Teams will create a Dataverse environment for that team (takes 2-5 minutes)

That's it! Your environment is ready. You don't need the Environment ID unless you're using the CLI import method.

### Get Environment Details (Optional - Only for CLI Import)

Skip this if you're using Option A in Step 5 (Teams import).

**To get Environment ID:**
1. Go to https://admin.powerplatform.microsoft.com
2. Click "Environments" in left nav
3. Find your environment (named after your Team)
4. Copy the "Environment ID" (GUID format)

---

## Step 4: Pack the Solution

From the project root folder:

**Windows:**
```powershell
cd deployment
.\pack-solution.ps1
```

**Mac/Linux:**
```bash
cd deployment
chmod +x *.sh  # Make scripts executable (first time only)
./pack-solution.sh
```

**What you should see:**
```
======================================
Performance Management Solution Pack
======================================

Checking for Power Platform CLI...
Found PAC CLI: Microsoft PowerApps CLI Version: 1.x.x

Packing solution...

======================================
SUCCESS: Solution packed!
======================================

Output file: PerformanceManagement_1_0_0_0.zip
```

If you get errors about PAC not found, go back and check the PATH setup.

The ZIP file is created in the project root folder.

---

## Step 5: Import the Solution

Three ways to import - choose what works best for you. The Teams app method is easiest for Dataverse for Teams environments.

### Option A: Import Through Teams Power Apps App (Recommended)

This is the native way to import into Dataverse for Teams - no browser needed!

1. **Open the Power Apps app in Teams**
   - Open Microsoft Teams
   - Click "Apps" in the left sidebar
   - Search for "Power Apps"
   - Click "Power Apps" and then "Add" (if not already installed)
   - Once installed, click "Power Apps" to open it

2. **Navigate to your environment**
   - Click the "Build" tab at the top
   - Select your team from the list (the one where you want the app)
   - If you don't see your team, it doesn't have a Dataverse environment yet:
     - Click "Create"
     - Follow the prompts to create a Teams environment
     - This takes 2-5 minutes

3. **Start the import**
   - If you already have apps: Click "See all" → Click "Import" button
   - If this is your first app: Click "Import your solution"

4. **Upload the solution file**
   - Click "Browse"
   - Navigate to your project folder
   - Select `PerformanceManagement_1_0_0_0.zip` (created in Step 4)
   - Click "Next"

5. **Complete the import**
   - You'll see a list of components to import
   - Leave everything checked (import all components)
   - Click "Import"

6. **Wait for completion**
   - Import runs in the background
   - Takes 5-15 minutes usually
   - You'll see a notification when done
   - Go to "Installed apps" → "See all" to view your imported solution

**If it fails:** Check for:
- Missing permissions (need Environment Maker role)
- Wrong team selected
- ZIP file corrupted (try re-packing in Step 4)

---

### Option B: Import Through Web Portal (Alternative)

Use this if you prefer working in a browser:

1. Go to https://make.powerapps.com
2. Select your environment (top right dropdown)
3. Click "Solutions" in left navigation
4. Click "Import solution" button
5. Browse and select `PerformanceManagement_1_0_0_0.zip`
6. Click "Next" → "Import"
7. Wait 5-15 minutes for completion

**Note:** Make sure you select a **Dataverse for Teams** environment, not a regular Dataverse environment.

---

### Option C: Import Using CLI (For Automation)

Only use this if you prefer command line or need scriptable deployment.

**Authenticate to Your Environment:**

```bash
# Use Environment ID
pac auth create --environment YOUR-ENVIRONMENT-ID-HERE

# OR use Environment URL
pac auth create --url https://orgXXXXX.crm.dynamics.com
```

This opens a browser. Sign in with your M365 account and approve permissions.

**Verify you're authenticated:**
```bash
pac auth list
```

Should show your environment with an asterisk (*) next to it.

**Run the import script:**

Still in the `deployment` folder:

**Windows:**
```powershell
.\import-solution.ps1 -EnvironmentId "YOUR-ENVIRONMENT-ID"
```

**Mac/Linux:**
```bash
./import-solution.sh --environment-id "YOUR-ENVIRONMENT-ID"
```

The script imports the ZIP file. It returns quickly but the import continues in the background.

**Monitor the import:**

1. Go to https://make.powerapps.com or https://admin.powerplatform.microsoft.com
2. Select your environment
3. Solutions → look for "Performance Management System"
4. Wait for status to change from "Importing" to "Installed"

---

## Step 6: Configure Connections

The flows won't work until you set up connections.

### Option A: Configure in Solution

1. Go to https://make.powerapps.com
2. Select your environment (top right dropdown)
3. Click "Solutions" (left nav)
4. Click "Performance Management System"
5. In the solution, look for "Connection References"

**If you see connection references:**
- Click each one
- Click "+ New connection"
- Sign in with your M365 account
- Click "Create"

Do this for:
- Office 365 Outlook
- Office 365 Users
- Dataverse (might auto-configure)

### Option B: Configure When Turning On Flows

If you don't see connection references (this is normal in Dataverse for Teams):

1. Go to https://make.powerautomate.com
2. Select your environment
3. Solutions → Performance Management System
4. Click on a flow
5. When you try to turn it on, it'll prompt you to add connections
6. Click "Add connection" for each
7. Sign in and authorize

---

## Step 7: Add the 12 Evaluation Questions

These don't import automatically - you need to add them manually.

1. Go to https://make.powerapps.com
2. Select your environment
3. Click "Tables" (left nav)
4. Search for "Evaluation Question"
5. Click the table
6. Click "+ New row" (you'll do this 12 times)

**For each row, enter:**
- **Question Text**: [see list below]
- **Question Number**: 1, 2, 3... through 12
- **Active**: Yes (check the box)

**The 12 Questions:**

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

**Pro tip:** Copy/paste them. This takes about 10 minutes.

---

## Step 8: Turn On the Flows

1. Go to https://make.powerautomate.com
2. Select your environment
3. Solutions → Performance Management System
4. Filter to "Cloud flows"

You should see 4 flows. Turn on the ones you want:

**Weekly Evaluation Reminder**
- Click the flow name
- Click "Turn on" (top right)
- If prompted for connections, add them
- Verify it says "Your flow is on"

**Quarterly Self-Eval Reminder**
- Same process

**One-on-One Meeting Notification**
- Same process
- This one watches your Outlook calendar

**Ad Hoc Self-Eval Request**
- HTTP-triggered flow
- Leave it off for now (the Canvas app will call it when needed)

**Troubleshooting:** If a flow won't turn on, click into it and check the "Flow checker" in top right for errors. Usually it's missing connections.

---

## Step 9: Build the Canvas App

The app specs are in `solution/CanvasApps/README.md` but here's the quick version:

### Create the App

1. Go to https://make.powerapps.com
2. Click "+ Create" (left nav)
3. Select "Blank app"
4. Choose "Tablet" format
5. Name it "Performance Management System"
6. Format: 1366 x 768

### Add Data Sources

Click "Data" (left nav in Power Apps Studio) and add:
- All 9 tables (Staff Member, Evaluation Question, Weekly Evaluation, etc.)
- Office 365 Users (connector)
- Office 365 Outlook (connector)

### Build the Screens

You need to create 9 screens. The detailed specs are in `solution/CanvasApps/README.md`.

**Minimum viable product approach:**

Start with these 3 screens to test:

1. **HomeScreen** - Just put a label that says "Performance Management System"
2. **WeeklyEvaluationsScreen** - Form with dropdowns for staff and questions
3. **StaffListScreen** - Gallery showing staff members

**Full build:** Follow the complete specs in `solution/CanvasApps/README.md`. Budget 2-4 hours if you're new to Power Apps, 1-2 hours if you've done this before.

### Key Formulas

**App.OnStart** (this calculates the weekly rotation):
```powerappsfx
Set(varCurrentUser, User());

ClearCollect(
    colMyStaff,
    Filter('pm_staffmember', 'pm_supervisor'.'Primary Email' = varCurrentUser.Email && pm_status = 1)
);

ClearCollect(
    colQuestions,
    SortByColumns(Filter('pm_evaluationquestion', pm_active = true), "pm_questionnumber", Ascending)
);

Set(varWeekNumber, RoundDown(DateDiff(Date(2025,1,1), Today(), Days) / 7, 0));
Set(varTotalQuestions, CountRows(colQuestions));
Set(varTotalStaff, CountRows(colMyStaff));

Set(varQuestionIndex1, Mod(varWeekNumber * 2, varTotalQuestions));
Set(varQuestionIndex2, Mod(varWeekNumber * 2 + 1, varTotalQuestions));
Set(varStaffIndex1, Mod(varWeekNumber * 2, varTotalStaff));
Set(varStaffIndex2, Mod(varWeekNumber * 2 + 1, varTotalStaff));

Set(varSuggestedStaff1, If(varTotalStaff > 0, Index(colMyStaff, varStaffIndex1 + 1), Blank()));
Set(varSuggestedStaff2, If(varTotalStaff > 1, Index(colMyStaff, varStaffIndex2 + 1), Blank()));
Set(varSuggestedQuestion1, If(varTotalQuestions > 0, Index(colQuestions, varQuestionIndex1 + 1), Blank()));
Set(varSuggestedQuestion2, If(varTotalQuestions > 1, Index(colQuestions, varQuestionIndex2 + 1), Blank()));
```

This is the core rotation logic. Copy/paste it into App → OnStart.

### Save and Publish

1. Click "Save" (top right)
2. Click "Publish"
3. Click "Publish this version"

---

## Step 10: Share the App

1. Back at https://make.powerapps.com
2. Click "Apps" (left nav)
3. Find "Performance Management System"
4. Click the three dots (...)
5. Click "Share"
6. Add users:
   - Type their email addresses
   - Select "Can use" (not "Can edit")
   - Click "Share"

They'll get an email with a link to open the app.

---

## Step 11: Test It

### Basic Smoke Test

1. **Open the app** (from the email link or make.powerapps.com)
2. **Add a test staff member:**
   - Navigate to Staff List
   - Click "+ Add Staff"
   - Fill in the fields
   - Save
3. **Do a test evaluation:**
   - Go to Weekly Evaluations screen
   - Select the staff member you just created
   - Select any question
   - Give a rating
   - Save
4. **Check the data:**
   - Go back to make.powerapps.com
   - Tables → Weekly Evaluation
   - You should see your test record

### Flow Testing

**Weekly Reminder (optional):**
- The flow runs Monday mornings at 8 AM Central
- To test without waiting: Click the flow → "Run" → "Run flow"
- Check your email for the reminder

**Quarterly Reminder:**
- Only runs on 1st of Jan/Apr/Jul/Oct
- Test same way (click "Run" manually)

---

## Troubleshooting

### "pac command not found"

**Fix:**
```bash
# Check .NET SDK is installed
dotnet --version

# Reinstall PAC CLI
dotnet tool uninstall --global Microsoft.PowerApps.CLI.Tool
dotnet tool install --global Microsoft.PowerApps.CLI.Tool

# Add to PATH
# Windows: $env:PATH += ";$env:USERPROFILE\.dotnet\tools"
# Mac/Linux: export PATH="$PATH:$HOME/.dotnet/tools"
```

### Solution Import Fails

**Check:**
1. Do you have the right permissions in the environment?
2. Is the environment a Dataverse for Teams environment?
3. Check error logs in admin.powerplatform.microsoft.com

**Common issues:**
- Missing dependencies: Make sure all files are in the ZIP
- Environment too old: Dataverse for Teams requires recent version

### Flows Won't Turn On

**Usually connection issues:**
1. Click into the flow
2. Click "Edit"
3. Check any action with a warning icon
4. Click "Add new connection"
5. Sign in
6. Save the flow
7. Try turning it on again

### Canvas App Data Not Loading

**Check data connections:**
1. In Power Apps Studio, click "Data"
2. Refresh each data source
3. Make sure the table names match (should start with pm_)
4. Check you have permissions to the tables

### Rotation Algorithm Not Working

**Debug:**
1. In App.OnStart, add a Label to your screen
2. Set its Text property to: `varSuggestedStaff1.pm_name`
3. If blank, check:
   - Are there staff members in the table?
   - Are they marked as Active?
   - Are there questions in the Evaluation Question table?

---

## What's Next

**Production deployment:**
1. Test in dev environment first (you did this)
2. Export as managed solution if going to production
3. Import to production environment
4. Repeat configuration steps
5. Share with actual users

**First supervisor setup:**
1. Have them add their staff members
2. Do a few test evaluations
3. Check the weekly email reminder works
4. Adjust anything that feels off

**Ongoing:**
- Flows run automatically once configured
- Supervisors get reminders every Monday
- Staff get quarterly reminders
- Just use the app

---

## Quick Reference

**Key URLs:**
- Admin portal: https://admin.powerplatform.microsoft.com
- Power Apps maker: https://make.powerapps.com
- Power Automate: https://make.powerautomate.com

**Important Files:**
- Solution ZIP: `PerformanceManagement_1_0_0_0.zip`
- Canvas app specs: `solution/CanvasApps/README.md`
- This guide: You're reading it

**Support:**
- Check VERIFICATION.md for validation details
- Check USER-GUIDE.md for end-user questions
- Check repository Issues for known problems

---

That's it. If you followed all this, you should have a working performance management system. Test it thoroughly before rolling out to everyone.
