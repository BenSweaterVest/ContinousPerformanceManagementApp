# Performance Management System

A comprehensive Power Platform solution for continuous performance management designed for Microsoft Dataverse for Teams.

## Overview

This solution enables supervisors to conduct weekly micro-evaluations of staff, track quarterly self-assessments, manage one-on-one meetings, and generate performance reports. Built specifically for public sector IT organizations with supervision responsibilities.

## Features

### ✅ Weekly Micro-Evaluations
- Supervisor completes 2 evaluations per week per staff member
- Rotating through 12 standardized questions
- 5-point rating scale plus "Insufficient Data" option
- Automatic rotation algorithm ensures comprehensive coverage

### ✅ Quarterly Self-Assessments
- Staff complete self-evaluations each quarter
- Same 12 questions as supervisor evaluations
- Enables comparison and discussion
- Automated reminders

### ✅ One-on-One Meeting Management
- Document meeting agendas and notes
- Track action items
- Link to staff performance data
- Meeting preparation notifications

### ✅ Individual Development Plans
- Employee-owned development goals
- Progress tracking
- Status management

### ✅ Recognition Tracking
- Log positive feedback and achievements
- Build performance documentation
- Support annual reviews

### ✅ Goals and Action Items
- Track performance goals
- Manage follow-up tasks
- Completion percentage tracking

## Solution Components

### Dataverse Tables (9)
1. **Staff Member** - Employee records
2. **Evaluation Question** - 12 standardized questions
3. **Weekly Evaluation** - Supervisor micro-evaluations
4. **Self Evaluation** - Employee self-assessments
5. **IDP Entry** - Development plan items
6. **Meeting Note** - One-on-one documentation
7. **Goal** - Performance objectives
8. **Recognition Entry** - Positive feedback log
9. **Action Item** - Follow-up tasks

### Canvas App
- Tablet-optimized interface (1366x768)
- 9 screens for complete functionality
- Dashboard with key metrics
- Rotation algorithm built-in

### Power Automate Flows (4)
1. **Weekly Evaluation Reminder** - Monday morning notifications
2. **Quarterly Self-Eval Reminder** - Quarterly notifications
3. **One-on-One Meeting Notification** - Pre-meeting prep
4. **Ad Hoc Self-Eval Request** - On-demand requests

## Quick Start

### Prerequisites

- Microsoft 365 subscription with Teams
- Dataverse for Teams environment
- Power Platform CLI installed
- Power Apps license

### Installation

#### 1. Install Power Platform CLI

**Windows:**
```powershell
dotnet tool install --global Microsoft.PowerApps.CLI.Tool
```

**Mac/Linux:**
```bash
dotnet tool install --global Microsoft.PowerApps.CLI.Tool
```

#### 2. Pack the Solution

**Windows:**
```powershell
cd deployment
.\pack-solution.ps1
```

**Mac/Linux:**
```bash
cd deployment
./pack-solution.sh
```

#### 3. Import to Environment

**Windows:**
```powershell
.\import-solution.ps1 -EnvironmentId "your-environment-id"
```

**Mac/Linux:**
```bash
./import-solution.sh --environment-id "your-environment-id"
```

#### 4. Post-Import Configuration

1. Configure connection references in Power Apps
2. Enable Power Automate flows
3. Load seed data (12 evaluation questions)
4. Share app with supervisors

## Detailed Documentation

- **[Deployment Guide](docs/DEPLOYMENT-GUIDE.md)** - Complete deployment instructions
- **[Data Model](docs/DATA-MODEL.md)** - Entity relationships and schemas
- **[User Guide](docs/USER-GUIDE.md)** - End-user instructions
- **[Canvas App Specs](solution/CanvasApps/README.md)** - App building instructions

## Architecture

### Rotation Algorithm

The solution uses a mathematical rotation algorithm to ensure comprehensive, equitable evaluations:

```
Week Number = Days since Jan 1, 2025 ÷ 7
Question Index = (Week Number × 2) % Total Questions
Staff Index = (Week Number × 2) % Total Staff
```

This ensures:
- All staff evaluated equally over time
- All questions covered systematically
- Predictable schedule for planning
- 2 evaluations per week per supervisor

### Security Model

- Row-level security: Supervisors see only their staff
- Role-based access control
- Dataverse security roles
- No cross-supervisor data visibility

## Technical Specifications

- **Platform**: Microsoft Power Platform
- **Target**: Dataverse for Teams
- **Solution Version**: 1.0.0.0
- **Publisher**: Minnesota IT Services (mnit)
- **Prefix**: mnit_

## System Requirements

- Microsoft Teams with Dataverse for Teams
- Modern web browser (Chrome, Edge, Firefox, Safari)
- Tablet or desktop for optimal Canvas App experience
- Stable internet connection

## Solution Structure

```
ContinousPerformanceManagementApp/
├── solution/
│   ├── Other/
│   │   ├── Solution.xml
│   │   └── Customizations.xml
│   ├── Tables/          # 9 Dataverse table definitions
│   ├── Workflows/       # 4 Power Automate flows
│   ├── CanvasApps/      # Canvas app specifications
│   └── WebResources/
├── deployment/
│   ├── pack-solution.ps1
│   ├── pack-solution.sh
│   ├── import-solution.ps1
│   └── import-solution.sh
└── docs/
    ├── DEPLOYMENT-GUIDE.md
    ├── DATA-MODEL.md
    └── USER-GUIDE.md
```

## Version History

### 1.0.0.0 (Current)
- Initial release
- 9 Dataverse tables
- Canvas app with 9 screens
- 4 Power Automate flows
- Weekly rotation algorithm
- Quarterly self-evaluations

---

**Built with Microsoft Power Platform**
