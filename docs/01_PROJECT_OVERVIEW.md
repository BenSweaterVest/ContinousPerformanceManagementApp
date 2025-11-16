# Project Overview: Continuous Performance Management System

## The Problem with Traditional Performance Reviews

Annual performance reviews are broken:
- **Recency bias**: Managers can only remember the last few months
- **High stress**: One conversation determines raises and promotions
- **Infrequent feedback**: Staff wait months to know how they're doing
- **Time-consuming**: Managers spend weeks writing lengthy reviews
- **Limited data**: Reviews based on memory, not systematic observation

## The Solution: Continuous Micro-Evaluations

This system replaces annual reviews with a continuous feedback model:

### Weekly Micro-Evaluations (5 minutes each)
Instead of one massive annual review, managers complete **2 quick evaluations per week** per staff member:
- Rate on a 1-5 scale or mark "Insufficient Data"
- Questions rotate through 12 standardized criteria
- Takes 2-3 minutes per person
- Builds a comprehensive picture over time

**Example**: Week 1 might ask about "Communication Skills" and "Technical Ability", Week 2 asks about "Teamwork" and "Initiative", etc.

### The Rotation Algorithm

```
Week Number = Days since Jan 1, 2025 ÷ 7
Question Index = (Week Number × 2) % 12
```

This ensures:
- Every question gets covered systematically
- All staff evaluated equally over time
- No favoritism or forgotten employees
- Predictable and fair

### Quarterly Self-Assessments

Every quarter, staff complete self-evaluations:
- Same 12 questions as weekly evaluations
- Provides employee perspective
- Creates discussion points for reviews
- Automated reminders ensure completion

## Theory: Why This Works

### 1. **Reduced Cognitive Load**
- 2 questions vs. comprehensive review
- Fresh observations vs. year-old memories
- Quick ratings vs. lengthy narratives

### 2. **More Accurate Data**
- 52 touchpoints per year vs. 1 annual review
- Real-time observations vs. retrospective recall
- Quantitative ratings allow trend analysis

### 3. **Continuous Improvement**
- Immediate feedback possible
- Course corrections throughout the year
- No waiting 11 months to address issues

### 4. **Better Conversations**
- Data-driven discussions
- Specific examples from recent weeks
- Self-eval comparison shows self-awareness

### 5. **Reduced Bias**
- Systematic rotation prevents cherry-picking
- Long-term trends vs. single-moment judgments
- "Insufficient Data" option acknowledges limitations

## The 12 Evaluation Questions

The system uses 12 standardized performance criteria:

1. **Communication Skills** - Written, verbal, and presentation abilities
2. **Technical Ability** - Job-specific skills and knowledge
3. **Quality of Work** - Accuracy, attention to detail, thoroughness
4. **Productivity** - Efficiency and output
5. **Initiative** - Self-starting, proactive problem-solving
6. **Teamwork** - Collaboration and cooperation
7. **Dependability** - Reliability, attendance, follow-through
8. **Professionalism** - Conduct, ethics, workplace behavior
9. **Adaptability** - Flexibility, learning agility
10. **Leadership** - Influence, mentoring, decision-making
11. **Problem Solving** - Analytical thinking, troubleshooting
12. **Customer Focus** - Service quality, stakeholder relationships

Each question is rated 1-5 or marked "Insufficient Data" if the manager hasn't observed that area recently.

## System Features

### For Managers

**Weekly Workflow (5 minutes)**:
1. Open app on Monday morning
2. See automated suggestions: "This week, evaluate:"
   - Staff Member A on Question 1 (Communication)
   - Staff Member B on Question 3 (Quality of Work)
3. Rate 1-5 or mark "Insufficient Data"
4. Add optional notes
5. Done

**One-on-One Meetings**:
- Review recent evaluation trends
- Compare manager vs. self-assessment ratings
- Discuss gaps and action items
- Document meeting notes in the app

**Annual Reviews**:
- Auto-generated summary from 52 weeks of data
- Charts showing trends over time
- Self-eval comparison for each quarter
- All recognition and feedback logged

### For Staff

**Quarterly Self-Assessments (10 minutes)**:
- Receive automated reminder
- Rate yourself on the same 12 questions
- Reflect on growth areas
- Submit for manager review

**Individual Development Plans**:
- Set personal development goals
- Track progress on learning objectives
- Update quarterly during one-on-ones

**Recognition**:
- Receive positive feedback as it happens
- View your accomplishments log
- Export for resume/portfolio

## Data Model Overview

The system consists of 9 interconnected entities:

```
┌─────────────────┐
│  Staff Member   │─────┐
└─────────────────┘     │
         │              │
         │              │
         ├──────────────┼───────────────┬──────────────┬──────────────┐
         │              │               │              │              │
         ▼              ▼               ▼              ▼              ▼
┌──────────────┐  ┌──────────────┐  ┌─────────┐  ┌──────────┐  ┌────────────┐
│   Weekly     │  │     Self     │  │   IDP   │  │ Meeting  │  │    Goal    │
│ Evaluation   │  │ Evaluation   │  │  Entry  │  │   Note   │  │            │
└──────────────┘  └──────────────┘  └─────────┘  └──────────┘  └────────────┘
         │                                              │
         │                                              │
         ▼                                              ▼
┌──────────────┐                               ┌──────────────┐
│  Evaluation  │                               │ Action Item  │
│   Question   │                               │              │
└──────────────┘                               └──────────────┘
                                                       │
                                                       │
                                               ┌──────────────┐
                                               │ Recognition  │
                                               │              │
                                               └──────────────┘
```

### Core Entities

**Staff Member**: Employee profiles with basic info (name, email, hire date, supervisor)

**Evaluation Question**: The 12 standardized questions used for evaluations

**Weekly Evaluation**: Manager ratings (links to Staff Member, Evaluation Question, includes rating 1-5 and notes)

**Self Evaluation**: Quarterly self-assessments (links to Staff Member, includes fiscal year/quarter)

**IDP Entry**: Individual development goals (links to Staff Member, includes goal, status, dates)

**Meeting Note**: One-on-one meeting documentation (links to Staff Member, includes date, notes, attendees)

**Goal**: Performance objectives (links to Staff Member, includes description, target date, status)

**Recognition**: Positive feedback and kudos (links to Staff Member, includes description, date)

**Action Item**: Follow-up tasks from meetings (links to Staff Member and Meeting Note, includes owner, due date, status)

See [DATA-MODEL.md](DATA-MODEL.md) for detailed field definitions.

## Proposed User Interface

### Screen Layout (9 Screens)

1. **Home Dashboard**
   - This week's evaluation assignments
   - Quick stats (completion rate, pending self-evals)
   - Upcoming meetings
   - Recent recognition

2. **Staff List**
   - All staff members (filtered by supervisor)
   - Quick access to staff details
   - Add/edit staff profiles

3. **Weekly Evaluations**
   - Complete this week's evaluations
   - View past evaluations by staff member
   - Filter by date range
   - Trend charts

4. **Self-Assessments**
   - For staff: Complete quarterly self-eval
   - For managers: View staff self-assessments
   - Compare manager vs. self ratings

5. **One-on-One Meetings**
   - Schedule meetings
   - View recent evaluation data before meeting
   - Document meeting notes
   - Create action items

6. **Individual Development Plans**
   - View/edit IDP goals
   - Track progress
   - Update status

7. **Goals & Objectives**
   - Performance goals
   - Track completion
   - Link to evaluations

8. **Recognition & Feedback**
   - Log positive feedback
   - View recognition history
   - Export for reviews

9. **Reports & Analytics**
   - Evaluation completion rates
   - Trend analysis over time
   - Manager vs. self-assessment gaps
   - Export data for annual reviews

## Automation (Power Automate Flows)

### 1. Weekly Evaluation Reminder
**Trigger**: Every Monday at 8:00 AM

**Actions**:
- Calculate current week number
- Determine which questions and staff to evaluate
- Send email to each supervisor with their assignments
- Format: "This week, evaluate Person A on Communication and Person B on Quality of Work"

### 2. Quarterly Self-Assessment Reminder
**Trigger**: First business day of each quarter (Jan 1, Apr 1, Jul 1, Oct 1)

**Actions**:
- Identify all staff due for self-assessment
- Create pending self-evaluation records
- Send email reminder to each staff member
- Include link to self-assessment form

### 3. One-on-One Meeting Notification
**Trigger**: 15 minutes before scheduled meeting

**Actions**:
- Retrieve recent evaluation data for staff member
- Get action items from last meeting
- Send meeting prep email to manager
- Include summary of recent ratings and trends

### 4. Ad-Hoc Self-Evaluation Request
**Trigger**: Manual trigger (button in canvas app)

**Actions**:
- Create new self-evaluation record
- Send email to staff member requesting off-cycle self-assessment
- Log request in system

## Technical Requirements

### Microsoft 365 Environment
- Microsoft Teams (with Dataverse for Teams license)
- Power Apps license (included in most M365 subscriptions)
- Power Automate license (for flows)
- Modern web browser

### Dataverse for Teams
- Lightweight Dataverse environment within Teams
- 1M row capacity (sufficient for years of data)
- No additional licensing cost
- Deployed per Team

### User Roles & Security

**Supervisor Role**:
- Create/edit evaluations for their staff
- View self-assessments
- Manage meetings and action items
- Full access to their staff's data
- No access to other supervisors' data

**Staff Role**:
- Complete self-assessments
- View own evaluation history
- Manage own IDP
- View own recognition
- No access to others' evaluations

**Security Model**: Row-level security based on Staff Member → Supervisor relationship

## Success Metrics

After deployment, measure:

1. **Completion Rate**: % of weekly evaluations completed on time
2. **Coverage**: % of staff evaluated each week
3. **Time Savings**: Compare time spent on annual reviews before/after
4. **Manager Satisfaction**: Survey on ease of use and value
5. **Staff Satisfaction**: Survey on feedback frequency and quality
6. **Data Quality**: % of "Insufficient Data" responses (should decrease over time)

## Next Steps

1. ✅ Deploy Dataverse entities (Version 2.0.0.7 - COMPLETED)
2. **Add the 12 evaluation questions** to pm_evaluationquestion table
3. **Build canvas app** in Power Apps Studio (9 screens)
4. **Create Power Automate flows** (4 flows for automation)
5. **Add initial staff records** to pm_staffmember table
6. **Pilot with one team** before full rollout
7. **Train managers** on weekly evaluation workflow
8. **Launch** and monitor adoption

## Conclusion

This continuous performance management system transforms performance reviews from a dreaded annual event into a lightweight, data-driven, continuous process. By breaking evaluations into 2-minute weekly touchpoints, managers build comprehensive performance data without the burden of traditional review cycles.

The system is built entirely on Microsoft Power Platform, making it easy to deploy, customize, and integrate with existing Microsoft 365 workflows.
