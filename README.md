# Continuous Performance Management App
**A Microsoft Teams Power Platform Solution**

## Overview

This project demonstrates how to build a complete Microsoft Teams performance management application using Dataverse for Teams and Power Apps canvas apps. The solution enables continuous performance feedback through weekly micro-evaluations and quarterly self-assessments, replacing traditional annual review cycles.

**Current Status**: ✅ Dataverse solution successfully importing (Version 2.0.0.7)

## What's in This Repository

This repository contains:
- ✅ A working Dataverse for Teams solution with 9 custom entities
- 📚 Comprehensive documentation on building Power Platform solutions with AI
- 🔧 Reference implementations from Microsoft template apps
- 📦 Release package ready for deployment

## Quick Start

1. **Deploy the Solution**:
   - Download [`releases/PerformanceManagement_v2.0.0.7.zip`](releases/PerformanceManagement_v2.0.0.7.zip)
   - Import into your Microsoft Teams Dataverse environment
   - See [Deployment Guide](docs/DEPLOYMENT-GUIDE.md) for details

2. **Build the Canvas App**:
   - Follow the guide in [docs/03_AI_CANVAS_APP_GUIDE.md](docs/03_AI_CANVAS_APP_GUIDE.md)
   - Or use Power Apps Studio to create your own interface

## Documentation

### For Understanding the Project
- 📖 [**Project Overview**](docs/01_PROJECT_OVERVIEW.md) - The concept, theory, and requirements behind continuous performance management
- 🎯 [**Data Model**](docs/DATA-MODEL.md) - Entity relationships and field definitions

### For Developers
- 🐙 [**GitHub Solution Packaging**](docs/02_GITHUB_SOLUTION_PACKAGING.md) - Using GitHub for Power Platform version control
- 🤖 [**AI Canvas App Development Guide**](docs/03_AI_CANVAS_APP_GUIDE.md) - Comprehensive guide on building canvas apps with AI assistance
- 🔄 [**Solution Fixes Journey**](docs/04_SOLUTION_FIXES_JOURNEY.md) - The 10 iterations of fixes we applied to get the solution working

### Reference Documentation
- 📋 [**Deployment Guide**](docs/DEPLOYMENT-GUIDE.md) - Step-by-step deployment instructions
- 📝 [**Release Notes**](docs/RELEASE_NOTES.md) - Version history and changes

## Project Structure

```
ContinousPerformanceManagementApp/
├── docs/                    # Comprehensive documentation
├── solution/                # Dataverse solution files
│   ├── Other/
│   │   ├── Customizations.xml  # Entity definitions
│   │   └── Solution.xml        # Solution manifest
│   └── Workflows/           # Power Automate flow templates (JSON)
├── ref/                     # Microsoft template apps for reference
├── releases/                # Packaged solution releases
│   └── PerformanceManagement_v2.0.0.7.zip
└── deployment/              # Deployment scripts
```

## The Performance Management System

### Core Concept

Traditional annual performance reviews are outdated. This system enables:
- **Weekly Micro-Evaluations** (5 minutes each) - Regular touchpoints for continuous feedback
- **Quarterly Self-Assessments** - Structured reflection on progress and goals
- **Individual Development Plans (IDP)** - Goal tracking and growth planning
- **Recognition & Kudos** - Celebrate wins as they happen
- **Action Items & Follow-ups** - Track commitments from 1:1 meetings

### Data Model

The solution includes 9 custom Dataverse entities:

1. **Staff Member** - Employee profiles
2. **Evaluation Question** - Configurable evaluation criteria
3. **Weekly Evaluation** - Quick manager check-ins
4. **Self Evaluation** - Quarterly employee self-assessments
5. **IDP Entry** - Individual development plan items
6. **Meeting Note** - 1:1 meeting documentation
7. **Goal** - Performance goals and objectives
8. **Recognition** - Kudos and achievements
9. **Action Item** - Follow-up tasks from meetings

See [docs/DATA-MODEL.md](docs/DATA-MODEL.md) for detailed entity relationships.

## Key Achievements

This project successfully demonstrates:

✅ **Building Dataverse solutions entirely through code and AI** - No Power Apps designer required for the data layer

✅ **10 iterations of systematic fixes** - Documented journey from initial failures to working import

✅ **Deep analysis of .msapp structure** - Understanding how canvas apps work internally

✅ **GitHub-based version control** - Managing Power Platform solutions like traditional code

✅ **Teams Dataverse compatibility** - Meeting all requirements for lightweight Teams environments

## What We Learned

Through this project, we discovered:

1. **Teams Dataverse has stricter requirements** than full Dataverse (no `<Format>` elements, memo→ntext, etc.)
2. **Every lookup field needs a relationship definition** - Not automatically inferred
3. **Canvas apps are ZIP archives** with complex JSON structures and checksums
4. **Power Apps Studio is the practical path** for building canvas apps (manual creation is possible but impractical)
5. **GitHub can effectively version control** Power Platform solutions

See [docs/04_SOLUTION_FIXES_JOURNEY.md](docs/04_SOLUTION_FIXES_JOURNEY.md) for the complete story.

## Contributing

This repository serves as both a working solution and a learning resource. Feel free to:
- Use this as a template for your own Teams apps
- Learn from the documented journey of fixes
- Contribute improvements or additional documentation

## Next Steps

1. **Build the Canvas App** - Create the user interface in Power Apps Studio
2. **Add Evaluation Questions** - Populate the pm_evaluationquestion table with your criteria
3. **Create Power Automate Flows** - Automate reminders and notifications
4. **Deploy to Production** - Roll out to your team

## License

This project is provided as-is for educational and reference purposes.

## Acknowledgments

Built with the assistance of Claude (Anthropic) and inspired by Microsoft's Teams template apps (Boards, Area Inspection, etc.).

---

**Version**: 2.0.0.7
**Last Updated**: November 2025
**Status**: Dataverse entities working, canvas app pending
