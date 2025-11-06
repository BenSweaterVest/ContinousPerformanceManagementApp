# Canvas App: Performance Management System

## Overview

The Canvas App must be created within Power Apps Studio and then exported/added to this solution. This document provides the complete specifications for building the app.

## App Configuration

- **Name**: Performance Management System
- **Form Factor**: Tablet (1366x768)
- **Data Sources**:
  - mnit_staffmember
  - mnit_evaluationquestion
  - mnit_weeklyevaluation
  - mnit_selfevaluation
  - mnit_idpentry
  - mnit_meetingnote
  - mnit_goal
  - mnit_recognition
  - mnit_actionitem
  - Office 365 Users
  - Office 365 Outlook (for flows)

## App.OnStart Formula

```powerappsfx
// Get current user
Set(varCurrentUser, User());

// Load staff members supervised by current user
ClearCollect(
    colMyStaff,
    Filter(
        'Staff Members',
        'Supervisor'.'Primary Email' = varCurrentUser.Email &&
        Status.Value = 1  // Active
    )
);

// Load all active questions
ClearCollect(
    colQuestions,
    SortByColumns(
        Filter('Evaluation Questions', Active = true),
        "Question Number",
        Ascending
    )
);

// Calculate rotation for this week
Set(varWeekNumber, RoundDown(DateDiff(Date(2025,1,1), Today(), Days) / 7, 0));
Set(varTotalQuestions, CountRows(colQuestions));
Set(varTotalStaff, CountRows(colMyStaff));

// Determine this week's suggested evaluations
Set(varQuestionIndex1, Mod(varWeekNumber * 2, varTotalQuestions));
Set(varQuestionIndex2, Mod(varWeekNumber * 2 + 1, varTotalQuestions));
Set(varStaffIndex1, Mod(varWeekNumber * 2, varTotalStaff));
Set(varStaffIndex2, Mod(varWeekNumber * 2 + 1, varTotalStaff));

// Get suggested items (handle empty collections)
Set(
    varSuggestedStaff1,
    If(varTotalStaff > 0, Index(colMyStaff, varStaffIndex1 + 1), Blank())
);
Set(
    varSuggestedStaff2,
    If(varTotalStaff > 1, Index(colMyStaff, varStaffIndex2 + 1), Blank())
);
Set(
    varSuggestedQuestion1,
    If(varTotalQuestions > 0, Index(colQuestions, varQuestionIndex1 + 1), Blank())
);
Set(
    varSuggestedQuestion2,
    If(varTotalQuestions > 1, Index(colQuestions, varQuestionIndex2 + 1), Blank())
);

// Calculate current fiscal quarter (July-June fiscal year)
Set(
    varCurrentQuarter,
    Switch(
        Month(Today()),
        1, 2, 3, "Q3",
        4, 5, 6, "Q4",
        7, 8, 9, "Q1",
        10, 11, 12, "Q2",
        "Q1"
    )
);

Set(
    varCurrentFiscalYear,
    If(Month(Today()) >= 7, Year(Today()) + 1, Year(Today()))
);

// Navigate to home screen
Navigate(HomeScreen, ScreenTransition.None);
```

## Screen Specifications

### 1. HomeScreen (Dashboard)

**Purpose**: Main landing page with overview and quick actions

**Components**:
- Header label: "Performance Management System"
- User greeting: "Welcome, " & varCurrentUser.FullName
- 4 Stat Cards:
  - Total Staff: CountRows(colMyStaff)
  - Evaluations This Month: CountRows(Filter('Weekly Evaluations', Month('Evaluation Date') = Month(Today())))
  - Upcoming 1-on-1s: CountRows(Filter('Meeting Notes', 'Meeting Date' >= Today() && 'Meeting Date' <= Today() + 7))
  - Pending Actions: CountRows(Filter('Action Items', Status.Value = 1))

- Alert Box: "This Week's Suggested Evaluations"
  - Staff 1 + Question 1
  - Staff 2 + Question 2

- Recent Activity Gallery (last 10 evaluations)
- Navigation buttons to all screens

### 2. WeeklyEvaluationsScreen

**Purpose**: Complete weekly micro-evaluations

**Components**:
- Alert: This week's suggestions (varSuggestedStaff1, varSuggestedQuestion1, etc.)
- Form controls:
  - Dropdown: Staff Member (Items: colMyStaff, Default: varSuggestedStaff1)
  - Dropdown: Question (Items: colQuestions, Default: varSuggestedQuestion1)
  - Button group: Rating (1-5 + Insufficient Data)
  - Text input: Notes (multiline)
  - Button: Save
  - Button: Skip (move to next suggestion)
- Recent evaluations gallery

**Save Button OnSelect**:
```powerappsfx
Patch(
    'Weekly Evaluations',
    Defaults('Weekly Evaluations'),
    {
        'Staff Member': drpStaffMember.Selected,
        Evaluator: LookUp(Users, 'Primary Email' = varCurrentUser.Email),
        Question: drpQuestion.Selected,
        Rating: {Value: varSelectedRating},
        Notes: txtNotes.Text,
        'Evaluation Date': Today(),
        'Evaluation Type': {Value: 1} // Weekly Suggested
    }
);
Notify("Evaluation saved successfully!", NotificationType.Success);
Reset(frm Evaluation);
```

### 3. StaffListScreen

**Purpose**: View and manage staff members

**Components**:
- Gallery: All active staff (colMyStaff)
- Search box
- Add staff button
- Edit/View buttons per item

### 4. StaffDetailScreen

**Purpose**: Detailed view of a staff member with all related data

**Components**:
- Staff member info card
- Tabs:
  - Overview (recent evaluations, goals, meetings)
  - Performance History (charts/graphs)
  - Development Plan (IDP entries)
  - Recognition
- Navigation back to list

### 5. OneOnOneScreen

**Purpose**: Document one-on-one meetings

**Components**:
- Form:
  - Staff member dropdown
  - Meeting date picker
  - Agenda (multiline text)
  - Discussion notes (multiline text)
  - Action items (multiline text)
  - Save button
- Recent meetings gallery

### 6. GoalsScreen

**Purpose**: Track performance goals

**Components**:
- Gallery: All goals for supervised staff
- Filter: By staff member, by status
- Add goal button
- Edit form with progress slider

### 7. RecognitionScreen

**Purpose**: Log positive recognition

**Components**:
- Form:
  - Staff member dropdown
  - Recognition date (default: Today)
  - Description (multiline)
  - Save button
- Recent recognition gallery

### 8. ActionItemsScreen

**Purpose**: Track follow-up actions

**Components**:
- Gallery: Pending action items
- Filters: My items, All items, Overdue
- Mark complete checkbox
- Add action item form

### 9. ReportsScreen

**Purpose**: View analytics and export data

**Components**:
- Charts:
  - Average ratings by staff member
  - Evaluation completion rate
  - Goals completion status
- Export buttons (to Excel via Power Automate)
- Date range selector

## Theme and Styling

- Primary Color: #0078D4 (Microsoft Blue)
- Secondary Color: #106EBE
- Success: #107C10
- Warning: #FFB900
- Error: #D83B01
- Font: Segoe UI

## Navigation Menu (Component)

Create a reusable navigation component with buttons:
- Home
- Weekly Evaluations
- Staff
- One-on-Ones
- Goals
- Recognition
- Action Items
- Reports

OnSelect formula for each: `Navigate(TargetScreen, ScreenTransition.Fade)`

## Building the App

1. Open Power Apps Studio
2. Create new Tablet app
3. Add data sources (all tables listed above)
4. Create each screen following specifications
5. Add formulas and controls
6. Test thoroughly
7. Save and publish
8. Add to this solution via Power Apps Studio or pac CLI

## Notes

- Use delegation-compatible formulas where possible
- Implement loading spinners for long operations
- Add error handling for all Patch operations
- Test on actual tablet devices
- Ensure mobile-responsive where appropriate
