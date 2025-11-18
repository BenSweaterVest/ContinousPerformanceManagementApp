# PowerApps for Teams - Manual Build Guide
**Step-by-Step Instructions for Building the Continuous Performance Management App**

This guide provides detailed, click-by-click instructions for building the entire Performance Management app manually in PowerApps for Teams with Dataverse, without using the import solution function.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Part 1: Set Up Teams Environment](#part-1-set-up-teams-environment)
3. [Part 2: Create Dataverse Tables](#part-2-create-dataverse-tables)
4. [Part 3: Build the Canvas App](#part-3-build-the-canvas-app)
5. [Part 4: Create Power Automate Flows](#part-4-create-power-automate-flows)
6. [Part 5: Configure Security](#part-5-configure-security)
7. [Part 6: Testing & Deployment](#part-6-testing--deployment)

**Estimated Total Time**: 4-6 hours

---

## Prerequisites

### Required Access
- Microsoft 365 account (E3, E5, or Business Premium)
- Microsoft Teams access
- Permissions to create apps in Teams

### Knowledge Level
- Basic familiarity with Microsoft Teams
- No coding experience required
- This guide assumes you're brand new to PowerApps

### What You'll Build
- 9 custom Dataverse tables
- 1 canvas app with 9 screens
- 4 automated Power Automate flows
- Complete performance management system

---

## Part 1: Set Up Teams Environment

### Step 1.1: Install Power Apps in Microsoft Teams

1. **Open Microsoft Teams**
   - Launch the Teams desktop app or go to https://teams.microsoft.com

2. **Access the Apps Store**
   - Click **"Apps"** in the left sidebar (icon looks like four squares)

3. **Search for Power Apps**
   - In the search box at the top, type **"Power Apps"**
   - Click on **"Power Apps"** in the search results (published by Microsoft Corporation)

4. **Install Power Apps**
   - Click the **"Add"** button
   - Wait for installation to complete (5-10 seconds)

5. **Pin Power Apps (Optional but Recommended)**
   - Right-click on **"Power Apps"** in the left sidebar
   - Select **"Pin"**
   - This keeps Power Apps easily accessible

### Step 1.2: Create a Dataverse for Teams Environment

1. **Open the Power Apps App**
   - Click **"Power Apps"** in the Teams left sidebar

2. **Navigate to the Build Tab**
   - At the top of Power Apps, click the **"Build"** tab

3. **Select or Create a Team**
   - **Option A - Use Existing Team:**
     - Find the team where you want to build this app
     - Click on the team name

   - **Option B - Create New Team:**
     - Click **"Create a team"** at the bottom
     - Choose **"From scratch"**
     - Choose **"Private"** (recommended for HR data)
     - Team name: **"Performance Management"**
     - Description: **"Continuous performance management system"**
     - Click **"Create"**

4. **Create the Dataverse Environment**
   - After selecting your team, you'll see a message about creating a Dataverse database
   - Click **"Create"** or **"Create new environment"**
   - Wait 2-5 minutes for environment creation
   - You'll see a success message when ready

**✓ Checkpoint**: You should now see "Installed apps" and be able to create a new app

---

## Part 2: Create Dataverse Tables

In this section, you'll create all 9 custom tables. We'll go through the first table in complete detail, then provide streamlined instructions for the remaining tables.

### Step 2.1: Create Table #1 - Staff Member

1. **Access the Power Apps Maker Portal**
   - Open a new browser tab
   - Go to: https://make.powerapps.com
   - Sign in with your Microsoft 365 account

2. **Select Your Environment**
   - At the top right, click the **Environment** dropdown
   - Select your team's environment (it will be named after your team)
   - Example: "Performance Management" or similar

3. **Navigate to Tables**
   - In the left navigation pane, click **"Tables"**
   - You'll see a list of standard Dataverse tables

4. **Create New Table**
   - Click **"+ New table"** at the top
   - Select **"Create new table"** (NOT import or add existing)

5. **Configure Table Properties**
   - **Display name**: `Staff Member`
   - **Plural name**: `Staff Members` (auto-fills)
   - **Description**: `Employee profiles for performance management`
   - Click **"Advanced settings"** (dropdown arrow)
   - **Name** (logical name): `pm_staffmember` (auto-generated, starts with prefix)
   - Leave other settings as default
   - Click **"Save"**

6. **Wait for Table Creation**
   - The table is being created (10-15 seconds)
   - You'll see a success notification

7. **Add Custom Columns**

   The table already has a default "Name" column. Now add these additional columns:

   **Column 1: Employee ID**
   - Click **"+ New"** → **"Column"**
   - **Display name**: `Employee ID`
   - **Data type**: **Text** → **Single line of text**
   - **Max length**: `50`
   - **Required**: Leave unchecked (optional field)
   - Click **"Save"**

   **Column 2: Position Title**
   - Click **"+ New"** → **"Column"**
   - **Display name**: `Position Title`
   - **Data type**: **Text** → **Single line of text**
   - **Max length**: `200`
   - **Required**: Leave unchecked
   - Click **"Save"**

   **Column 3: Supervisor**
   - Click **"+ New"** → **"Column"**
   - **Display name**: `Supervisor`
   - **Data type**: **Lookup** → **Lookup**
   - **Related table**: Search for and select **"User"** (systemuser)
   - **Required**: Leave unchecked
   - Click **"Advanced options"**
   - **Relationship name**: `pm_staffmember_supervisor`
   - Click **"Save"**

   **Column 4: Start Date**
   - Click **"+ New"** → **"Column"**
   - **Display name**: `Start Date`
   - **Data type**: **Date and time** → **Date only**
   - **Required**: Leave unchecked
   - Click **"Save"**

   **Column 5: Status**
   - Click **"+ New"** → **"Column"**
   - **Display name**: `Status`
   - **Data type**: **Choice** → **Choice**
   - Click **"+ New choice"**
   - **Choice name**: `Staff Status`
   - Add options:
     - **Label**: `Active`, **Value**: `1`
     - Click **"+ New choice"**
     - **Label**: `Inactive`, **Value**: `2`
   - Click **"Save"** (on the choice)
   - **Default choice**: Select **Active**
   - Click **"Save"** (on the column)

8. **Verify Staff Member Table**
   - Click on **"Tables"** in the left nav
   - Find **"Staff Member"** in the list
   - Click on it to verify all columns are present:
     - ✓ Name (auto-created)
     - ✓ Employee ID
     - ✓ Position Title
     - ✓ Supervisor
     - ✓ Start Date
     - ✓ Status

**✓ Checkpoint**: Staff Member table created with 6 columns

---

### Step 2.2: Create Table #2 - Evaluation Question

1. **Create New Table**
   - Click **"Tables"** in left nav
   - Click **"+ New table"** → **"Create new table"**

2. **Table Properties**
   - **Display name**: `Evaluation Question`
   - **Plural name**: `Evaluation Questions`
   - **Description**: `Standard performance evaluation questions`
   - Click **"Save"**

3. **Modify the Name Column**
   - Find the **"Name"** column in the column list
   - Click on **"Name"** to edit it
   - Change **Data type** from "Single line of text" to **"Multiple lines of text"**
   - **Max length**: `2000`
   - Click **"Save"**
   - This will be used for the question text

4. **Add Column: Question Number**
   - Click **"+ New"** → **"Column"**
   - **Display name**: `Question Number`
   - **Data type**: **Number** → **Whole number**
   - **Required**: Leave unchecked
   - Click **"Save"**

5. **Add Column: Active**
   - Click **"+ New"** → **"Column"**
   - **Display name**: `Active`
   - **Data type**: **Choice** → **Yes/No**
   - **Default value**: **Yes**
   - Click **"Save"**

**✓ Checkpoint**: Evaluation Question table created with 3 columns

---

### Step 2.3: Create Table #3 - Weekly Evaluation

1. **Create New Table**
   - Click **"Tables"** → **"+ New table"** → **"Create new table"**

2. **Table Properties**
   - **Display name**: `Weekly Evaluation`
   - **Plural name**: `Weekly Evaluations`
   - **Description**: `Manager weekly micro-evaluations`
   - Click **"Save"**

3. **Configure Auto-Numbering for Name Column**
   - Click on the **"Name"** column
   - Change **Data type** to **"Autonumber"**
   - **Autonumber type**: **String prefixed number**
   - **Prefix**: `EVAL-`
   - **Minimum number of digits**: `5`
   - Click **"Save"**

4. **Add Column: Staff Member** (Lookup)
   - Click **"+ New"** → **"Column"**
   - **Display name**: `Staff Member`
   - **Data type**: **Lookup**
   - **Related table**: Search and select **"Staff Member"** (pm_staffmember)
   - **Required**: **Check this box** (required field)
   - **Relationship name**: `pm_staffmember_weeklyevaluations`
   - Click **"Save"**

5. **Add Column: Evaluator** (Lookup)
   - Click **"+ New"** → **"Column"**
   - **Display name**: `Evaluator`
   - **Data type**: **Lookup**
   - **Related table**: **"User"** (systemuser)
   - **Required**: **Check this box**
   - **Relationship name**: `pm_weeklyevaluation_evaluator`
   - Click **"Save"**

6. **Add Column: Question** (Lookup)
   - Click **"+ New"** → **"Column"**
   - **Display name**: `Question`
   - **Data type**: **Lookup**
   - **Related table**: **"Evaluation Question"** (pm_evaluationquestion)
   - **Required**: **Check this box**
   - **Relationship name**: `pm_evaluationquestion_weeklyevals`
   - Click **"Save"**

7. **Add Column: Rating** (Choice)
   - Click **"+ New"** → **"Column"**
   - **Display name**: `Rating`
   - **Data type**: **Choice**
   - Click **"+ New choice"**
   - **Choice name**: `Evaluation Rating`
   - Add these options:
     - **Label**: `1 - Not Satisfactory`, **Value**: `1`
     - **Label**: `2 - Below Standard`, **Value**: `2`
     - **Label**: `3 - Meets Standard`, **Value**: `3`
     - **Label**: `4 - Exceeds Standard`, **Value**: `4`
     - **Label**: `5 - Exceptional`, **Value**: `5`
     - **Label**: `Insufficient Data`, **Value**: `6`
   - Click **"Save"** (on the choice)
   - **Required**: **Check this box**
   - Click **"Save"** (on the column)

8. **Add Column: Notes**
   - Click **"+ New"** → **"Column"**
   - **Display name**: `Notes`
   - **Data type**: **Text** → **Multiple lines of text**
   - **Max length**: `5000`
   - **Required**: Leave unchecked
   - Click **"Save"**

9. **Add Column: Evaluation Date**
   - Click **"+ New"** → **"Column"**
   - **Display name**: `Evaluation Date`
   - **Data type**: **Date and time** → **Date only**
   - **Required**: **Check this box**
   - Click **"Advanced options"**
   - **Default value**: **Today's date**
   - Click **"Save"**

10. **Add Column: Evaluation Type**
    - Click **"+ New"** → **"Column"**
    - **Display name**: `Evaluation Type`
    - **Data type**: **Choice**
    - Click **"+ New choice"**
    - **Choice name**: `Evaluation Type`
    - Add options:
      - **Label**: `Weekly Suggested`, **Value**: `1`
      - **Label**: `Ad Hoc`, **Value**: `2`
    - Click **"Save"** (choice)
    - **Default**: **Weekly Suggested**
    - Click **"Save"** (column)

**✓ Checkpoint**: Weekly Evaluation table created with 7 columns

---

### Step 2.4: Create Table #4 - Self Evaluation

1. **Create New Table**
   - **Display name**: `Self Evaluation`
   - **Plural name**: `Self Evaluations`
   - **Description**: `Employee quarterly self-assessments`
   - Click **"Save"**

2. **Configure Name Column**
   - Click **"Name"** column
   - **Data type**: **Autonumber**
   - **Prefix**: `SELF-`
   - **Minimum digits**: `5`
   - Click **"Save"**

3. **Add Columns:**

   **Staff Member** (Lookup, Required)
   - **Related table**: Staff Member
   - **Relationship name**: `pm_staffmember_selfevaluations`

   **Question** (Lookup, Required)
   - **Related table**: Evaluation Question
   - **Relationship name**: `pm_evaluationquestion_selfevals`

   **Rating** (Choice, Optional)
   - Use existing choice: **Evaluation Rating** (created earlier)
   - Or create same 1-5 + Insufficient Data options

   **Notes** (Multiple lines of text, 5000 chars, Optional)

   **Quarter** (Choice, Required)
   - Create new choice: **Fiscal Quarter**
   - Options:
     - `Q1 (Jul-Sep)` = `1`
     - `Q2 (Oct-Dec)` = `2`
     - `Q3 (Jan-Mar)` = `3`
     - `Q4 (Apr-Jun)` = `4`

   **Fiscal Year** (Whole number, Required)

   **Evaluation Type** (Choice, Optional)
   - Create new choice: **Self Evaluation Type**
   - Options:
     - `Quarterly` = `1`
     - `Ad Hoc` = `2`

   **Completed Date** (Date only, Optional)

**✓ Checkpoint**: Self Evaluation table created with 8 columns

---

### Step 2.5: Create Table #5 - IDP Entry

1. **Create New Table**
   - **Display name**: `IDP Entry`
   - **Plural name**: `IDP Entries`
   - **Description**: `Individual Development Plan goals`
   - Click **"Save"**

2. **Modify Name Column**
   - Click **"Name"** column
   - **Data type**: **Multiple lines of text**
   - **Max length**: `500`
   - This will store the goal description
   - Click **"Save"**

3. **Add Columns:**

   **Staff Member** (Lookup, Required)
   - **Related table**: Staff Member
   - **Relationship name**: `pm_staffmember_idp`

   **Target Date** (Date only, Optional)

   **Status** (Choice, Optional)
   - Create choice: **IDP Status**
   - Options:
     - `Not Started` = `1`
     - `In Progress` = `2`
     - `Completed` = `3`
     - `On Hold` = `4`

   **Progress Notes** (Multiple lines of text, 5000 chars, Optional)

**✓ Checkpoint**: IDP Entry table created with 4 columns

---

### Step 2.6: Create Table #6 - Meeting Note

1. **Create New Table**
   - **Display name**: `Meeting Note`
   - **Plural name**: `Meeting Notes`
   - **Description**: `One-on-one meeting documentation`
   - Click **"Save"**

2. **Configure Name Column**
   - **Data type**: **Autonumber**
   - **Prefix**: `MTG-`
   - **Minimum digits**: `5`
   - Click **"Save"**

3. **Add Columns:**

   **Staff Member** (Lookup, Required)
   - **Related table**: Staff Member
   - **Relationship name**: `pm_staffmember_meetings`

   **Supervisor** (Lookup, Required)
   - **Related table**: User
   - **Relationship name**: `pm_meetingnote_supervisor`

   **Meeting Date** (Date only, Required)

   **Agenda** (Multiple lines of text, 5000 chars, Optional)

   **Discussion Notes** (Multiple lines of text, 10000 chars, Optional)

   **Action Items** (Multiple lines of text, 5000 chars, Optional)

**✓ Checkpoint**: Meeting Note table created with 6 columns

---

### Step 2.7: Create Table #7 - Goal

1. **Create New Table**
   - **Display name**: `Goal`
   - **Plural name**: `Goals`
   - **Description**: `Performance and development goals`
   - Click **"Save"**

2. **Modify Name Column**
   - **Data type**: **Multiple lines of text**
   - **Max length**: `500`
   - Click **"Save"**

3. **Add Columns:**

   **Staff Member** (Lookup, Required)
   - **Related table**: Staff Member
   - **Relationship name**: `pm_staffmember_goals`

   **Status** (Choice, Optional)
   - Create choice: **Goal Status**
   - Options:
     - `Not Started` = `1`
     - `In Progress` = `2`
     - `Completed` = `3`
     - `Blocked` = `4`

   **Completion Percentage** (Whole number, Optional)
   - Click **"Advanced options"**
   - **Minimum value**: `0`
   - **Maximum value**: `100`

   **Due Date** (Date only, Optional)

**✓ Checkpoint**: Goal table created with 4 columns

---

### Step 2.8: Create Table #8 - Recognition

1. **Create New Table**
   - **Display name**: `Recognition`
   - **Plural name**: `Recognitions`
   - **Description**: `Positive feedback and achievements`
   - Click **"Save"**

2. **Configure Name Column**
   - **Data type**: **Autonumber**
   - **Prefix**: `REC-`
   - **Minimum digits**: `5`
   - Click **"Save"**

3. **Add Columns:**

   **Staff Member** (Lookup, Required)
   - **Related table**: Staff Member
   - **Relationship name**: `pm_staffmember_recognition`

   **Supervisor** (Lookup, Required)
   - **Related table**: User
   - **Relationship name**: `pm_recognition_supervisor`

   **Recognition Date** (Date only, Required)
   - **Default**: Today's date

   **Description** (Multiple lines of text, 5000 chars, Optional)

**✓ Checkpoint**: Recognition table created with 4 columns

---

### Step 2.9: Create Table #9 - Action Item

1. **Create New Table**
   - **Display name**: `Action Item`
   - **Plural name**: `Action Items`
   - **Description**: `Follow-up tasks from meetings`
   - Click **"Save"**

2. **Configure Name Column**
   - **Data type**: **Autonumber**
   - **Prefix**: `ACT-`
   - **Minimum digits**: `5`
   - Click **"Save"**

3. **Add Columns:**

   **Description** (Multiple lines of text, 2000 chars, Required)

   **Owner** (Lookup, Required)
   - **Related table**: User
   - **Relationship name**: `pm_actionitem_owner`

   **Related Staff Member** (Lookup, Optional)
   - **Related table**: Staff Member
   - **Relationship name**: `pm_staffmember_actionitems`

   **Due Date** (Date only, Required)

   **Status** (Choice, Optional)
   - Create choice: **Action Item Status**
   - Options:
     - `Pending` = `1`
     - `In Progress` = `2`
     - `Completed` = `3`
   - **Default**: Pending

   **Completed Date** (Date only, Optional)

**✓ Checkpoint**: Action Item table created with 6 columns

---

### Step 2.10: Add the 12 Evaluation Questions

Now populate the Evaluation Question table with the standard questions.

1. **Navigate to Evaluation Questions Table**
   - Go to **Tables** → **Evaluation Question**
   - Click **"Edit"** or **"Edit data"**

2. **Add Each Question** (Repeat 12 times)

   Click **"+ New row"** and enter:

   **Question 1:**
   - **Name**: `Demonstrates quality and accuracy in work products`
   - **Question Number**: `1`
   - **Active**: `Yes`
   - Click **"Save"**

   **Question 2:**
   - **Name**: `Completes assignments within agreed timeframes`
   - **Question Number**: `2`
   - **Active**: `Yes`
   - Click **"Save"**

   **Question 3:**
   - **Name**: `Communicates effectively with team members and stakeholders`
   - **Question Number**: `3`
   - **Active**: `Yes`
   - Click **"Save"**

   **Question 4:**
   - **Name**: `Takes initiative to identify and solve problems proactively`
   - **Question Number**: `4`
   - **Active**: `Yes`
   - Click **"Save"**

   **Question 5:**
   - **Name**: `Demonstrates technical competency in required skills`
   - **Question Number**: `5`
   - **Active**: `Yes`
   - Click **"Save"**

   **Question 6:**
   - **Name**: `Adapts effectively to changing priorities`
   - **Question Number**: `6`
   - **Active**: `Yes`
   - Click **"Save"**

   **Question 7:**
   - **Name**: `Collaborates well with others`
   - **Question Number**: `7`
   - **Active**: `Yes`
   - Click **"Save"**

   **Question 8:**
   - **Name**: `Follows established processes and procedures`
   - **Question Number**: `8`
   - **Active**: `Yes`
   - Click **"Save"**

   **Question 9:**
   - **Name**: `Demonstrates customer service orientation`
   - **Question Number**: `9`
   - **Active**: `Yes`
   - Click **"Save"**

   **Question 10:**
   - **Name**: `Pursues professional development and learning`
   - **Question Number**: `10`
   - **Active**: `Yes`
   - Click **"Save"**

   **Question 11:**
   - **Name**: `Manages workload and priorities effectively`
   - **Question Number**: `11`
   - **Active**: `Yes`
   - Click **"Save"**

   **Question 12:**
   - **Name**: `Demonstrates dependability and reliability`
   - **Question Number**: `12`
   - **Active**: `Yes`
   - Click **"Save"**

**✓ Checkpoint**: All 9 tables created, 12 questions added

---

## Part 3: Build the Canvas App

Now you'll build the user interface in Power Apps Studio.

### Step 3.1: Create a New Canvas App

1. **Return to Teams Power Apps**
   - Go back to Microsoft Teams
   - Click **Power Apps** in the left sidebar
   - Click the **"Build"** tab

2. **Start New App**
   - Select your team (Performance Management)
   - Click **"Create an app"**
   - Or click **"New"** → **"App"**

3. **Choose App Type**
   - Select **"Tablet"** layout (1366 x 768)
   - Or select **"Blank app"** then choose Tablet
   - **App name**: `Performance Management`
   - Click **"Create"**

4. **Wait for Studio to Load**
   - Power Apps Studio will open (15-30 seconds)
   - You'll see a blank canvas

**✓ Checkpoint**: Power Apps Studio is open with a blank tablet app

---

### Step 3.2: Add Data Sources

Before building screens, connect to your tables.

1. **Open Data Panel**
   - In Power Apps Studio, click **"Data"** in the left sidebar (cylinder icon)

2. **Add Dataverse Tables**
   - Click **"+ Add data"**
   - Search for: `Staff Member`
   - Click **"Staff Member"** (with your prefix, e.g., pm_staffmember)
   - Click **"Connect"**

3. **Repeat for All Tables**
   Add these tables one by one:
   - ✓ Staff Member
   - ✓ Evaluation Question
   - ✓ Weekly Evaluation
   - ✓ Self Evaluation
   - ✓ IDP Entry
   - ✓ Meeting Note
   - ✓ Goal
   - ✓ Recognition
   - ✓ Action Item

4. **Add Office 365 Connectors**
   - Click **"+ Add data"**
   - Search for: `Office 365 Users`
   - Click **"Office 365 Users"**
   - Sign in if prompted
   - Click **"Connect"**

   - Repeat for: `Office 365 Outlook` (optional, for sending emails)

**✓ Checkpoint**: All data sources connected

---

### Step 3.3: Configure App OnStart

The OnStart formula initializes the app and calculates weekly rotation.

1. **Select the App Object**
   - In the left tree view, click **"App"** (at the very top)

2. **Find OnStart Property**
   - In the property dropdown (top left), select **"OnStart"**
   - Or find it in the formula bar

3. **Enter the OnStart Formula**

   Copy and paste this exact formula:

```powerappsfx
// Set current user
Set(varCurrentUser, User());

// Load staff supervised by current user
ClearCollect(
    colMyStaff,
    Filter(
        'Staff Members',
        'Supervisor'.'Primary Email' = varCurrentUser.Email &&
        Status.Value = 1
    )
);

// Load all active evaluation questions
ClearCollect(
    colQuestions,
    SortByColumns(
        Filter('Evaluation Questions', Active = true),
        "Question Number",
        Ascending
    )
);

// Calculate current week number (weeks since Jan 1, 2025)
Set(varWeekNumber, RoundDown(DateDiff(Date(2025,1,1), Today(), Days) / 7, 0));
Set(varTotalQuestions, CountRows(colQuestions));
Set(varTotalStaff, CountRows(colMyStaff));

// Calculate rotation indexes for 2 questions and 2 staff this week
Set(varQuestionIndex1, Mod(varWeekNumber * 2, varTotalQuestions));
Set(varQuestionIndex2, Mod(varWeekNumber * 2 + 1, varTotalQuestions));
Set(varStaffIndex1, Mod(varWeekNumber * 2, varTotalStaff));
Set(varStaffIndex2, Mod(varWeekNumber * 2 + 1, varTotalStaff));

// Get suggested staff and questions for this week
Set(varSuggestedStaff1, If(varTotalStaff > 0, Index(colMyStaff, varStaffIndex1 + 1), Blank()));
Set(varSuggestedStaff2, If(varTotalStaff > 1, Index(colMyStaff, varStaffIndex2 + 1), Blank()));
Set(varSuggestedQuestion1, If(varTotalQuestions > 0, Index(colQuestions, varQuestionIndex1 + 1), Blank()));
Set(varSuggestedQuestion2, If(varTotalQuestions > 1, Index(colQuestions, varQuestionIndex2 + 1), Blank()));

// Mark app as loaded
Set(varAppLoaded, true);
```

4. **Check for Errors**
   - Look for red underlines in the formula
   - If you see errors about table names, make sure they match exactly:
     - Use `'Staff Members'` (plural, in quotes)
     - Use `'Evaluation Questions'` (plural, in quotes)
   - Click the **"X"** icon to see error details

5. **Test the OnStart**
   - Click the **"..."** menu next to App
   - Select **"Run OnStart"**
   - Check that no errors appear

**✓ Checkpoint**: OnStart formula entered and runs without errors

---

### Step 3.4: Build Screen 1 - Home Dashboard

1. **Rename the Default Screen**
   - In the tree view, click **"Screen1"**
   - Press **F2** to rename
   - New name: `scrHome`
   - Press Enter

2. **Add a Header Label**
   - Click **"+ Insert"** in the toolbar
   - Select **"Label"**
   - A label appears on the canvas
   - **Properties:**
     - **Text**: `Performance Management`
     - **Font size**: `28`
     - **Font weight**: `Bold`
     - **Position**: X = `0`, Y = `0`
     - **Size**: Width = `1366`, Height = `80`
     - **Fill color**: Choose a dark blue (e.g., `RGBA(0, 51, 102, 1)`)
     - **Text color**: `White`
     - **Align**: `Center`

3. **Add Welcome Message**
   - Insert another **Label**
   - **Text**: `"Welcome, " & varCurrentUser.FullName`
   - **Font size**: `18`
   - **Position**: X = `40`, Y = `100`
   - **Size**: Width = `1200`, Height = `40`

4. **Add "This Week's Evaluations" Section**

   **Section Header:**
   - Insert **Label**
   - **Text**: `This Week's Suggested Evaluations`
   - **Font size**: `20`
   - **Font weight**: `Semibold`
   - **Position**: X = `40`, Y = `160`
   - **Size**: Width = `600`, Height = `40`

   **Evaluation 1 Container:**
   - Insert **Container** (or use Rectangle as background)
   - **Position**: X = `40`, Y = `220`
   - **Size**: Width = `600`, Height = `150`
   - **Fill**: Light gray `RGBA(240, 240, 240, 1)`
   - **Border**: 1px solid gray

   Inside the container, add:

   **Staff Label:**
   - Insert **Label**
   - **Text**: `"Staff: " & If(IsBlank(varSuggestedStaff1), "No staff assigned", varSuggestedStaff1.Name)`
   - **Position**: X = `60`, Y = `240`
   - **Size**: Width = `560`, Height = `30`
   - **Font size**: `16`

   **Question Label:**
   - Insert **Label**
   - **Text**: `"Question: " & If(IsBlank(varSuggestedQuestion1), "No questions available", varSuggestedQuestion1.Name)`
   - **Position**: X = `60`, Y = `280`
   - **Size**: Width = `560`, Height = `60`
   - **Font size**: `14`

   **Evaluation 2 Container:**
   - Duplicate the first container (Copy/Paste)
   - **Position**: X = `680`, Y = `220`
   - Update text formulas to use `varSuggestedStaff2` and `varSuggestedQuestion2`

5. **Add Navigation Buttons**

   Create buttons for each screen:

   **Button 1: Weekly Evaluations**
   - Insert **Button**
   - **Text**: `Weekly Evaluations`
   - **Position**: X = `40`, Y = `420`
   - **Size**: Width = `280`, Height = `60`
   - **OnSelect**: `Navigate(scrWeeklyEvals, ScreenTransition.Fade)`

   **Button 2: Self Assessments**
   - Insert **Button**
   - **Text**: `Self Assessments`
   - **Position**: X = `360`, Y = `420`
   - **Size**: Width = `280`, Height = `60`
   - **OnSelect**: `Navigate(scrSelfEvals, ScreenTransition.Fade)` (we'll create this screen next)

   **Button 3: Staff List**
   - Insert **Button**
   - **Text**: `Staff List`
   - **Position**: X = `680`, Y = `420`
   - **Size**: Width = `280`, Height = `60`
   - **OnSelect**: `Navigate(scrStaffList, ScreenTransition.Fade)`

   **Button 4: Meetings**
   - Insert **Button**
   - **Text**: `One-on-One Meetings`
   - **Position**: X = `1000`, Y = `420`
   - **Size**: Width = `280`, Height = `60`
   - **OnSelect**: `Navigate(scrMeetings, ScreenTransition.Fade)`

   Continue adding buttons for:
   - IDP (Individual Development Plans)
   - Goals
   - Recognition
   - Action Items

   Arrange in a grid layout below the first row

**✓ Checkpoint**: Home screen complete with welcome message and navigation

---

### Step 3.5: Build Screen 2 - Staff List

1. **Add New Screen**
   - Click **"+ New screen"** in the tree view toolbar
   - Select **"Blank"**
   - Rename to: `scrStaffList`

2. **Add Header**
   - Copy the header label from scrHome (Ctrl+C, Ctrl+V)
   - Change **Text** to: `Staff List`

3. **Add Back Button**
   - Insert **Icon** → **"Back arrow"**
   - **Position**: X = `20`, Y = `20`
   - **Size**: Width = `60`, Height = `60`
   - **OnSelect**: `Back()`
   - **Color**: White

4. **Add Staff Gallery**
   - Insert **Gallery** → **"Blank vertical"**
   - **Position**: X = `40`, Y = `120`
   - **Size**: Width = `1280`, Height = `580`
   - **Items**: `colMyStaff`

5. **Configure Gallery Template**

   Inside the gallery (galStaffList), add:

   **Name Label:**
   - Insert **Label** (inside gallery)
   - **Text**: `ThisItem.Name`
   - **Position**: X = `20`, Y = `10`
   - **Font size**: `18`
   - **Font weight**: `Semibold`

   **Position Label:**
   - Insert **Label**
   - **Text**: `ThisItem.'Position Title'`
   - **Position**: X = `20`, Y = `45`
   - **Font size**: `14`
   - **Color**: Gray

   **Employee ID Label:**
   - Insert **Label**
   - **Text**: `"ID: " & ThisItem.'Employee ID'`
   - **Position**: X = `20`, Y = `70`
   - **Font size**: `12`

   **Start Date Label:**
   - Insert **Label**
   - **Text**: `"Started: " & Text(ThisItem.'Start Date', "mm/dd/yyyy")`
   - **Position**: X = `400`, Y = `45`
   - **Font size**: `12`

   **Status Icon:**
   - Insert **Icon** → **"Check" or "Circle"**
   - **Color**: `If(ThisItem.Status.Value = 1, Green, Red)`
   - **Position**: Right side of gallery item

6. **Add "New Staff" Button**
   - Insert **Button** (outside gallery, above it)
   - **Text**: `+ Add Staff Member`
   - **Position**: X = `1050`, Y = `100`
   - **Size**: Width = `250`, Height = `50`
   - **OnSelect**:
```powerappsfx
NewForm(frmStaffEdit);
Navigate(scrStaffEdit, ScreenTransition.Fade)
```

7. **Add Gallery OnSelect**
   - Select the gallery (galStaffList)
   - Set **OnSelect** property:
```powerappsfx
Set(varSelectedStaff, ThisItem);
EditForm(frmStaffEdit);
Navigate(scrStaffEdit, ScreenTransition.Fade)
```

**✓ Checkpoint**: Staff list screen displays all staff members

---

### Step 3.6: Build Screen 3 - Staff Edit Form

1. **Add New Screen**
   - Click **"+ New screen"** → **"Blank"**
   - Rename to: `scrStaffEdit`

2. **Add Header and Back Button**
   - Copy header from previous screen
   - Change text to: `Staff Member Details`
   - Add back button with `Back()` action

3. **Add Edit Form**
   - Insert **"Edit form"**
   - Rename to: `frmStaffEdit`
   - **Position**: X = `40`, Y = `120`
   - **Size**: Width = `800`, Height = `600`
   - **Data source**: `'Staff Members'`
   - **Item**: `varSelectedStaff`

4. **Configure Form Fields**
   - Click **"Edit fields"** in the properties pane
   - Remove any default fields
   - Add these fields in order:
     - Name
     - Employee ID
     - Position Title
     - Supervisor
     - Start Date
     - Status

5. **Add Save Button**
   - Insert **Button**
   - **Text**: `Save`
   - **Position**: Below form, X = `40`, Y = `730`
   - **Size**: Width = `150`, Height = `50`
   - **OnSelect**:
```powerappsfx
SubmitForm(frmStaffEdit);
If(frmStaffEdit.Error = "", Back())
```

6. **Add Cancel Button**
   - Insert **Button**
   - **Text**: `Cancel`
   - **Position**: X = `210`, Y = `730`
   - **Size**: Width = `150`, Height = `50`
   - **OnSelect**: `ResetForm(frmStaffEdit); Back()`

**✓ Checkpoint**: Can add and edit staff members

---

### Step 3.7: Build Screen 4 - Weekly Evaluations

1. **Add New Screen**
   - Name: `scrWeeklyEvals`
   - Add header: `Weekly Evaluations`
   - Add back button

2. **Add "New Evaluation" Button**
   - **Text**: `+ New Evaluation`
   - **Position**: Top right
   - **OnSelect**:
```powerappsfx
Set(varNewEval, true);
Navigate(scrEvalForm, ScreenTransition.Fade)
```

3. **Add Evaluations Gallery**
   - Insert **Gallery** → **"Blank vertical"**
   - **Items**:
```powerappsfx
SortByColumns(
    Filter(
        'Weekly Evaluations',
        'Evaluator'.'Primary Email' = varCurrentUser.Email
    ),
    "Evaluation Date",
    Descending
)
```
   - **Position**: X = `40`, Y = `120`
   - **Size**: Width = `1280`, Height = `580`

4. **Configure Gallery Template**

   Add labels showing:
   - Staff Member name: `ThisItem.'Staff Member'.Name`
   - Question: `ThisItem.Question.Name`
   - Rating: `ThisItem.Rating.Value`
   - Date: `Text(ThisItem.'Evaluation Date', "mm/dd/yyyy")`
   - Notes preview: `Left(ThisItem.Notes, 100) & "..."`

5. **Add Filter Options** (Optional)
   - Add dropdown to filter by staff member
   - Add date range picker

**✓ Checkpoint**: Can view past evaluations

---

### Step 3.8: Build Screen 5 - Evaluation Form

1. **Add New Screen**
   - Name: `scrEvalForm`
   - Header: `Weekly Evaluation`

2. **Add Form**
   - Insert **Edit form**
   - Name: `frmEvaluation`
   - **Data source**: `'Weekly Evaluations'`
   - **Item**: `If(varNewEval, Defaults('Weekly Evaluations'), Gallery1.Selected)`

3. **Configure Form Fields**
   - Add fields:
     - Staff Member (Dropdown)
     - Question (Dropdown)
     - Rating (Dropdown)
     - Evaluation Date (Date picker)
     - Notes (Text input, multiline)

4. **Set Default Values**
   - Click on **Staff Member** card
   - **Default**: `varSuggestedStaff1` (for suggested evaluations)
   - Click on **Evaluator** card (if visible)
   - **Default**: `varCurrentUser`
   - Click on **Evaluation Date** card
   - **Default**: `Today()`

5. **Add Save Button**
   - **OnSelect**:
```powerappsfx
SubmitForm(frmEvaluation);
If(
    frmEvaluation.Error = "",
    Notify("Evaluation saved successfully", NotificationType.Success);
    Back()
)
```

6. **Add Cancel Button**
   - **OnSelect**: `ResetForm(frmEvaluation); Back()`

**✓ Checkpoint**: Can create new weekly evaluations

---

### Step 3.9: Build Remaining Screens

Following the same pattern as above, create:

**Screen 6: scrSelfEvals** (Self Assessments)
- Similar to Weekly Evaluations
- Filter by current user as staff member
- Form for completing self-assessments

**Screen 7: scrMeetings** (One-on-One Meetings)
- Gallery of past meetings
- Form to document new meetings

**Screen 8: scrIDP** (Individual Development Plans)
- Gallery of IDP goals
- Form to add/edit goals

**Screen 9: scrGoals** (Goals & Objectives)
- Gallery of goals
- Form to track progress

**Screen 10: scrRecognition** (Recognition)
- Gallery of recognition entries
- Form to log new recognition

**Screen 11: scrActionItems** (Action Items)
- Gallery of action items
- Form to create/complete actions

For each screen, follow the pattern:
1. Header with title
2. Back button
3. Gallery showing records
4. "New" button
5. Form screen for add/edit

**✓ Checkpoint**: All screens created

---

### Step 3.10: Save and Publish the App

1. **Save the App**
   - Click **"File"** in top left
   - Click **"Save"**
   - Or press **Ctrl+S**
   - App name: `Performance Management`
   - Click **"Save"**

2. **Publish the App**
   - Click **"Publish"**
   - Click **"Publish this version"**
   - Wait for confirmation

3. **Test the App**
   - Click **"Back"** (arrow in top left)
   - Click **Play** button (▶) to test
   - Navigate through screens
   - Test creating a staff member
   - Test creating an evaluation
   - Press **Esc** to exit preview

**✓ Checkpoint**: Canvas app is complete and published

---

## Part 4: Create Power Automate Flows

Now create the automated workflows.

### Step 4.1: Weekly Evaluation Reminder Flow

1. **Open Power Automate**
   - Go to https://make.powerautomate.com
   - Select your environment (top right)

2. **Create New Flow**
   - Click **"+ Create"** in left nav
   - Select **"Scheduled cloud flow"**

3. **Configure Trigger**
   - **Flow name**: `Weekly Evaluation Reminder`
   - **Starting**: Select a Monday in the future
   - **Repeat every**: `1` **Week**
   - **On these days**: Check **Monday**
   - **At these hours**: `8` (8 AM)
   - Click **"Create"**

4. **Add Action: Get Evaluation Questions**
   - Click **"+ New step"**
   - Search for: `Dataverse`
   - Select **"List rows"**
   - **Table name**: `Evaluation Questions`
   - **Filter rows**: `Active eq true`
   - **Sort by**: `Question Number`

5. **Add Action: Get Staff Members**
   - Click **"+ New step"**
   - Search: `Dataverse`
   - Select **"List rows"**
   - **Table name**: `Staff Members`
   - **Filter rows**: `Status eq 1`

6. **Add Action: Calculate Week Number**
   - Click **"+ New step"**
   - Search for: `Compose`
   - Select **"Compose"** action
   - **Inputs**:
```
div(sub(ticks(utcNow()), ticks('2025-01-01')), mul(7, 864000000000))
```
   This calculates weeks since Jan 1, 2025

7. **Add Action: Send Email to Each Supervisor**
   - Click **"+ New step"**
   - Search: `Office 365 Outlook`
   - Select **"Send an email (V2)"**
   - **To**: Enter a supervisor email (or make dynamic)
   - **Subject**: `Weekly Performance Evaluation Reminder`
   - **Body**:
```
Hi,

It's time for this week's micro-evaluations!

This week, please evaluate:
- [Staff Member A] on [Question X]
- [Staff Member B] on [Question Y]

Open the Performance Management app in Teams to complete your evaluations.

This takes just 2-3 minutes!

Thanks,
Performance Management System
```

8. **Save the Flow**
   - Click **"Save"** (top right)
   - Click **"Test"** to test manually
   - Or wait for Monday at 8 AM

**✓ Checkpoint**: Weekly reminder flow created

---

### Step 4.2: Quarterly Self-Evaluation Reminder Flow

1. **Create New Scheduled Flow**
   - **Flow name**: `Quarterly Self-Evaluation Reminder`
   - **Repeat every**: `3` **Months**
   - **Starting**: January 1 of current year
   - Click **"Create"**

2. **Add Action: Get All Staff**
   - **List rows** from `Staff Members`
   - **Filter**: `Status eq 1`

3. **Add Action: Send Email to Each Staff**
   - **Send an email (V2)**
   - **To**: Dynamic content: Staff Email
   - **Subject**: `Quarterly Self-Assessment Due`
   - **Body**:
```
Hi [Name],

It's time for your quarterly self-assessment!

Please complete your self-evaluation for all 12 performance criteria in the Performance Management app.

This should take about 15-20 minutes.

Deadline: [End of this month]

Thank you!
```

4. **Save and Test**

**✓ Checkpoint**: Quarterly reminder flow created

---

### Step 4.3: Meeting Notification Flow (Optional)

This flow sends a reminder before 1-on-1 meetings.

1. **Create New Flow**
   - Type: **Automated cloud flow**
   - **Trigger**: `When a new Meeting Note is created`

2. **Add Trigger**
   - Search: `Dataverse`
   - Select **"When a row is added, modified or deleted"**
   - **Change type**: `Added`
   - **Table name**: `Meeting Notes`

3. **Add Action: Get Staff Evaluation Summary**
   - **List rows** from `Weekly Evaluations`
   - **Filter**: Filter by staff member from trigger

4. **Add Action: Send Email**
   - **To**: Supervisor email
   - **Subject**: `Upcoming 1-on-1 with [Staff Name]`
   - **Body**: Include recent evaluation summary

5. **Save**

**✓ Checkpoint**: Meeting notification flow created

---

### Step 4.4: Ad-Hoc Self-Evaluation Request Flow (Optional)

This flow is triggered manually from the app.

1. **Create New Flow**
   - Type: **Instant cloud flow**
   - **Trigger**: `PowerApps`

2. **Add Trigger**
   - **PowerApps (V2)**

3. **Add Action: Get Staff Member**
   - Use PowerApps trigger inputs to get staff ID

4. **Add Action: Send Email**
   - **To**: Staff member email
   - **Subject**: `Self-Evaluation Request`

5. **Save**

6. **Connect to App**
   - Copy the flow URL
   - In Power Apps, add a button with:
   - **OnSelect**: `FlowName.Run(staffID)`

**✓ Checkpoint**: All 4 flows created

---

## Part 5: Configure Security

### Step 5.1: Create Security Roles (Optional)

For Teams environments, basic security is automatic, but you can configure advanced security.

1. **Navigate to Security Settings**
   - Go to https://admin.powerplatform.microsoft.com
   - Select your environment
   - Click **"Settings"**
   - Click **"Users + permissions"** → **"Security roles"**

2. **Create "Supervisor" Role**
   - Click **"+ New role"**
   - Name: `Performance Management Supervisor`
   - Grant permissions:
     - **Staff Members**: Read (All), Write (User's)
     - **Weekly Evaluations**: Full (User's)
     - **Self Evaluations**: Read (User's reports)
     - Others as needed

3. **Create "Employee" Role**
   - Click **"+ New role"**
   - Name: `Performance Management Employee`
   - Grant permissions:
     - **Staff Members**: Read (User record only)
     - **Self Evaluations**: Full (User record only)
     - **Weekly Evaluations**: Read (User record only)

4. **Assign Users to Roles**
   - Go to **"Users"**
   - Select a user
   - Click **"Manage roles"**
   - Assign appropriate role

**✓ Checkpoint**: Security configured

---

### Step 5.2: Share the App

1. **Go to Power Apps**
   - https://make.powerapps.com
   - Select your environment

2. **Find Your App**
   - Click **"Apps"** in left nav
   - Find **"Performance Management"**

3. **Share the App**
   - Click **"..."** (three dots)
   - Click **"Share"**
   - Add users:
     - Type email addresses
     - Or add security groups
   - Permissions: **"Can use"** (not "Can edit")
   - Click **"Share"**

4. **Share in Teams**
   - Open the app in Power Apps
   - Click **"File"** → **"Add to Teams"**
   - Select your team
   - Choose **"Add as tab"** or **"Add as app"**
   - Click **"Save"**

**✓ Checkpoint**: App shared with users

---

## Part 6: Testing & Deployment

### Step 6.1: Create Test Data

1. **Add Test Staff Members**
   - Open the app
   - Go to Staff List
   - Add 2-3 test staff members
   - Assign yourself as supervisor

2. **Complete Test Evaluations**
   - Go to Weekly Evaluations
   - Complete 2-3 evaluations for test staff
   - Try different ratings
   - Add notes

3. **Complete Test Self-Evaluation**
   - Log in as a test user (if possible)
   - Complete a self-assessment
   - Compare to manager evaluations

**✓ Checkpoint**: Test data created

---

### Step 6.2: Test All Functionality

Go through this checklist:

**Staff Management:**
- ✓ Add new staff member
- ✓ Edit existing staff
- ✓ View staff list
- ✓ Supervisor lookup works

**Weekly Evaluations:**
- ✓ Create new evaluation
- ✓ See suggested staff/questions on home screen
- ✓ View evaluation history
- ✓ Filter evaluations by staff
- ✓ Ratings save correctly

**Self Evaluations:**
- ✓ Complete self-assessment
- ✓ View past self-evals
- ✓ Compare to manager ratings

**Meetings:**
- ✓ Create meeting note
- ✓ View meeting history
- ✓ Add action items

**IDP & Goals:**
- ✓ Create development goals
- ✓ Update goal status
- ✓ Track completion

**Recognition:**
- ✓ Log recognition
- ✓ View recognition history

**Action Items:**
- ✓ Create action items
- ✓ Mark as complete
- ✓ Filter by status

**Flows:**
- ✓ Test weekly reminder (manually trigger)
- ✓ Test quarterly reminder (manually trigger)
- ✓ Verify emails are sent

**Navigation:**
- ✓ All buttons work
- ✓ Back button on each screen
- ✓ Smooth transitions

**✓ Checkpoint**: All features tested and working

---

### Step 6.3: Deploy to Production

1. **Export as Solution** (Optional)
   - Go to https://make.powerapps.com
   - Click **"Solutions"**
   - Click **"+ New solution"**
   - Name: `Performance Management v1.0`
   - Publisher: Select or create
   - Click **"Create"**

   - Click **"Add existing"** → **"App"** → **"Canvas app"**
   - Select your app
   - Click **"Add"**

   - Click **"Add existing"** → **"Table"**
   - Add all 9 custom tables
   - Click **"Add"**

   - Click **"Export"**
   - Export as **"Unmanaged"** for dev
   - Export as **"Managed"** for production

2. **Document for Users**
   - Create quick start guide
   - Record training video
   - Schedule training sessions

3. **Rollout Plan**
   - **Week 1**: Pilot with 1 team (5-10 people)
   - **Week 2-3**: Gather feedback, fix issues
   - **Week 4**: Deploy to next team
   - **Month 2**: Full organization rollout

4. **Monitor Adoption**
   - Check completion rates weekly
   - Follow up with non-users
   - Gather feedback
   - Iterate on improvements

**✓ Checkpoint**: Production deployment complete

---

## Troubleshooting

### App Won't Load
- Check browser console for errors
- Verify all data sources are connected
- Check OnStart formula for syntax errors
- Try clearing browser cache

### Data Not Saving
- Check form mode (New vs. Edit)
- Verify required fields are filled
- Check SubmitForm() formula
- Look for error messages in frmName.Error

### Flows Not Running
- Check flow run history
- Verify connections are active
- Check trigger conditions
- Test manually first

### Tables Not Appearing
- Verify you're in the correct environment
- Refresh data sources in Power Apps
- Check table permissions

### Rotation Algorithm Not Working
- Verify evaluation questions are numbered 1-12
- Check staff members exist
- Verify OnStart ran successfully
- Test varSuggestedStaff1 is not blank

---

## Next Steps

### Enhancements
1. **Add Analytics Dashboard**
   - Average ratings by staff
   - Trends over time
   - Completion rates

2. **Add Notifications**
   - In-app notifications for overdue evaluations
   - Push notifications in Teams

3. **Add Reporting**
   - Export to Excel
   - Annual review summaries
   - Manager vs. self-eval comparisons

4. **Integrate with HR Systems**
   - Auto-import staff from Active Directory
   - Sync with HRIS for position changes

### Training Materials
- Create video walkthroughs
- Build FAQ document
- Schedule lunch & learn sessions

### Ongoing Maintenance
- Review and update evaluation questions annually
- Archive old data (keep 2-3 years)
- Monitor for compliance
- Gather user feedback quarterly

---

## Summary

You've now built a complete Performance Management system in PowerApps for Teams!

**What You Created:**
- ✅ 9 custom Dataverse tables with relationships
- ✅ Canvas app with 11 screens
- ✅ 4 Power Automate flows for automation
- ✅ Security configuration
- ✅ Full continuous feedback system

**Time Investment:**
- Initial build: 4-6 hours
- Testing: 1-2 hours
- Training: 2-4 hours
- **Total**: ~10-12 hours

**Ongoing Time Savings:**
- Replaces 20+ hour annual review process
- Reduces to 5 minutes per week per manager
- Saves 15+ hours per year per manager
- Better data, less stress, happier teams

**Congratulations!** 🎉

You've transformed your performance management process from annual reviews to continuous feedback using nothing but Microsoft Teams and Power Platform.

---

**Document Version**: 1.0
**Last Updated**: November 2025
**Compatible With**: PowerApps for Teams, Dataverse for Teams
**Support**: See repository issues for questions
