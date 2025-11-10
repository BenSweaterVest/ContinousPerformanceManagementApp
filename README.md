# Performance Management System

A Power Platform solution for continuous performance management that runs on Dataverse for Teams.

## What is this?

Built this to help supervisors do performance management without it feeling like a giant bureaucratic nightmare. Instead of one massive annual review that everyone dreads, this breaks it down into weekly check-ins. Supervisors answer 2 questions per week about each staff member using a rotating list of 12 standard performance questions. Over time, you get comprehensive coverage without the stress.

Also handles quarterly self-evals, one-on-one meeting notes, development plans, and all that good stuff.

## What it does

**Weekly Micro-Evaluations**
- Supervisors do 2 quick evaluations per week per person
- Questions rotate automatically through a list of 12
- Rate 1-5 or mark "Insufficient Data" if you haven't observed that area
- No more forgetting what someone did 11 months ago

**Quarterly Self-Assessments**
- Staff rate themselves on the same 12 questions each quarter
- Makes for great discussion points in reviews
- Automated reminders so nobody forgets

**One-on-One Meeting Notes**
- Actually document what you talked about
- Track action items
- Link to recent performance data so you're prepared

**Development Plans (IDP)**
- Staff own their development goals
- Track progress over time
- See what people are actually working on

**Recognition & Feedback**
- Log the good stuff when it happens
- Build up evidence for annual reviews
- Everyone likes positive feedback

**Goals & Action Items**
- Track performance objectives
- Follow up on commitments
- Nobody falls through the cracks

## What's in here

**9 Dataverse Tables:**
- Staff Member (employee records)
- Evaluation Question (the 12 standardized questions)
- Weekly Evaluation (supervisor ratings)
- Self Evaluation (quarterly self-assessments)
- IDP Entry (development plan goals)
- Meeting Note (one-on-one documentation)
- Goal (performance objectives)
- Recognition Entry (positive feedback)
- Action Item (follow-ups from meetings)

**Canvas App:**
- Built for tablets (1366x768) but works on desktop too
- 9 screens covering all the functionality
- Dashboard shows your week at a glance
- Rotation algorithm built right in

**4 Power Automate Flows:**
- Weekly reminder (Monday mornings - sends suggestions for the week)
- Quarterly self-eval reminder (beginning of each quarter)
- One-on-one meeting prep (15 mins before meetings)
- Ad-hoc self-eval request (when you need an off-cycle assessment)

## Getting Started

**What you need:**
- Microsoft 365 with Teams
- Dataverse for Teams environment (comes with Teams)
- Power Platform CLI
- Power Apps license (included with most M365 subscriptions)

**Installation:**

Two ways to install - UI method is easier:

**Option A: UI Import (Recommended)**
1. Pack the solution (creates a ZIP file):
   ```bash
   cd deployment
   ./pack-solution.ps1    # Windows
   ./pack-solution.sh     # Mac/Linux
   ```
2. Go to https://make.powerapps.com
3. Solutions → Import solution
4. Upload the `PerformanceManagement_1_0_0_0.zip` file
5. Follow the wizard

**Option B: CLI Import**
Same as Option A step 1, then:
   ```bash
   ./import-solution.ps1 -EnvironmentId "your-env-id"    # Windows
   ./import-solution.sh --environment-id "your-env-id"   # Mac/Linux
   ```

4. **Post-import setup:**
   - Configure connection references (Office 365, Dataverse)
   - Turn on the flows
   - Add the 12 evaluation questions (they're in the deployment guide)
   - Share the app with your supervisors

**Docs:**
- [Deployment Guide](docs/DEPLOYMENT-GUIDE.md) - step-by-step deployment
- [Data Model](docs/DATA-MODEL.md) - how everything connects
- [User Guide](docs/USER-GUIDE.md) - for supervisors and staff
- [Canvas App Specs](solution/CanvasApps/README.md) - if you want to build/customize the app

## How it works

**The Rotation Algorithm**

Instead of you deciding who to evaluate and what question to ask, there's a simple rotation:

```
Week Number = Days since Jan 1, 2025 ÷ 7
Question Index = (Week Number × 2) % Total Questions
Staff Index = (Week Number × 2) % Total Staff
```

This means:
- Everyone gets evaluated equally over time
- All 12 questions get covered systematically
- No favoritism or forgetting about people
- Predictable - you always know what's coming

Every Monday you get an email saying "This week, evaluate Person A on Question 1 and Person B on Question 2." Simple.

**Security**

- Supervisors only see their own staff's data
- No peeking at other supervisors' evaluations
- Row-level security built into Dataverse
- Standard Azure AD authentication

## Tech Stack

- Microsoft Power Platform
- Dataverse for Teams
- Power Apps (Canvas)
- Power Automate
- Version 1.0.0.0

**System Requirements:**
- Microsoft Teams + Dataverse for Teams
- Modern browser (Chrome, Edge, Firefox, Safari)
- Works best on tablet or desktop
- Internet connection (obviously)

## Folder Structure

```
ContinousPerformanceManagementApp/
├── solution/           # All the Power Platform components
│   ├── Tables/         # 9 Dataverse table definitions
│   ├── Workflows/      # 4 Power Automate flow JSONs
│   ├── CanvasApps/     # Canvas app specs (you'll build this)
│   └── Other/          # Solution manifest files
├── deployment/         # Scripts to pack and import
│   ├── pack-solution.ps1
│   ├── pack-solution.sh
│   ├── import-solution.ps1
│   └── import-solution.sh
└── docs/              # All the documentation
    ├── DEPLOYMENT-GUIDE.md
    ├── DATA-MODEL.md
    └── USER-GUIDE.md
```

## Notes

**Canvas App:** The app specs are in `solution/CanvasApps/README.md` but you'll need to build it in Power Apps Studio. It's designed to take a few hours if you follow the specs.

**The 12 Questions:** After importing, you'll need to manually add the 12 evaluation questions to the Evaluation Question table. They're listed in the deployment guide.

**Flows:** The flows will import but won't run until you configure the connection references (Office 365, Dataverse).

**Testing:** Test in a dev environment first. Once you're happy with it, deploy to production.

## Changelog

**v1.0.0.0** (Initial Release)
- 9 Dataverse tables
- Canvas app design (9 screens)
- 4 automated flows
- Rotation algorithm
- Documentation

---

Built with Power Platform • Runs on Dataverse for Teams
