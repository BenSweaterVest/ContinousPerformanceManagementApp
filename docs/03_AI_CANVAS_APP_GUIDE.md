# AI-Powered Canvas App Development Guide
**Building Power Apps with AI Assistance**

## Introduction

This guide documents our journey building Power Apps canvas apps using AI assistance. Through deep analysis of Microsoft Teams template apps and systematic experimentation, we've uncovered how .msapp files work internally and identified the most practical approaches for AI-assisted development.

**Key Takeaway**: While manually creating canvas apps is theoretically possible, **Power Apps Studio remains the recommended approach**. However, understanding the internal structure is invaluable for debugging, automation, and AI-assisted development.

## Executive Summary

Canvas apps (.msapp files) are ZIP archives containing JSON and asset files that define the app's structure, data connections, controls, and UI. After analyzing Microsoft's Boards and Area Inspection template apps, this document provides a comprehensive guide to understanding canvas app internals and leveraging AI for development.

## .MSAPP File Structure

```
msapp_file.msapp (ZIP archive)
├── Header.json              # Version metadata
├── Properties.json          # App-level metadata & connections
├── checksum.json            # File integrity
├── AppCheckerResult.sarif   # Validation results (optional)
├── Controls/                # Screen & control definitions
│   ├── 1.json              # App control (root with OnStart)
│   ├── 3.json              # Screen 1
│   ├── 16.json             # Screen 2
│   └── ...                 # More screens/controls
├── Components/              # Custom reusable components (optional)
│   ├── 3.json
│   └── ...
├── ComponentsMetadata.json  # Component definitions (if Components/ exists)
├── References/
│   ├── DataSources.json    # Connection metadata (Office365, Teams, Dataverse)
│   ├── Templates.json      # Control templates
│   └── Themes.json         # Color themes
├── Resources/
│   └── PublishInfo.json    # Publishing metadata
└── Assets/
    └── Images/             # Icons, images, etc.
```

## Analysis of Two Template Apps

### Boards App
- **Purpose**: Task/project board management (similar to Trello/Planner)
- **Dataverse Entities**: 6 entities (Boards, Board Items, Board Categories, etc.)
- **External Connections**: Office 365 Users, Microsoft Teams
- **Screens**: 12 screens
- **Total Controls**: 305+ controls
- **Components**: None (uses inline controls)

### Area Inspection App
- **Purpose**: Location inspection checklist and task management
- **Dataverse Entities**: 12 entities (Area Inspections, Checklists, Steps, etc.)
- **External Connections**: Office 365 Users, Microsoft Teams, Planner
- **Screens**: 7 screens
- **Total Controls**: 425+ controls
- **Components**: 5 custom reusable components

## Key Files Explained

### 1. Header.json
Contains version information for the canvas app package.

**Example:**
```json
{
  "DocVersion": "1.305",
  "MinVersionToLoad": "1.305",
  "MSAppStructureVersion": "2.0"
}
```

**Key Fields:**
- `DocVersion`: Version of Power Apps that created this app
- `MinVersionToLoad`: Minimum Power Apps version required to open this app
- `MSAppStructureVersion`: Canvas app file format version (usually "2.0")

### 2. Properties.json
**MOST IMPORTANT FILE** - Contains all app-level metadata, connections, and configuration.

**Critical Sections:**

#### a) LocalDatabaseReferences (Dataverse Connection)
Maps the canvas app to Dataverse entities. This is **the key to connecting your app to your imported tables**.

**Example from Boards App:**
```json
{
  "default.cds": {
    "state": "Configured",
    "instanceUrl": "https://org95504ca5.crm.dynamics.com/",
    "webApiVersion": "v9.0",
    "dataSources": {
      "Users": {
        "entitySetName": "systemusers",
        "logicalName": "systemuser"
      },
      "Boards": {
        "entitySetName": "msft_boards",
        "logicalName": "msft_board"
      },
      "Board Items": {
        "entitySetName": "msft_boarditems",
        "logicalName": "msft_boarditem"
      }
    }
  }
}
```

**For Performance Management App, this would be:**
```json
{
  "default.cds": {
    "state": "Configured",
    "instanceUrl": "<YOUR_DATAVERSE_URL>",
    "webApiVersion": "v9.0",
    "dataSources": {
      "Users": {
        "entitySetName": "systemusers",
        "logicalName": "systemuser"
      },
      "Staff Members": {
        "entitySetName": "pm_staffmembers",
        "logicalName": "pm_staffmember"
      },
      "Weekly Evaluations": {
        "entitySetName": "pm_weeklyevaluations",
        "logicalName": "pm_weeklyevaluation"
      },
      "Self Evaluations": {
        "entitySetName": "pm_selfevaluations",
        "logicalName": "pm_selfevaluation"
      },
      "Evaluation Questions": {
        "entitySetName": "pm_evaluationquestions",
        "logicalName": "pm_evaluationquestion"
      },
      "IDP Entries": {
        "entitySetName": "pm_idpentries",
        "logicalName": "pm_idpentry"
      },
      "Meeting Notes": {
        "entitySetName": "pm_meetingnotes",
        "logicalName": "pm_meetingnote"
      },
      "Goals": {
        "entitySetName": "pm_goals",
        "logicalName": "pm_goal"
      },
      "Recognitions": {
        "entitySetName": "pm_recognitions",
        "logicalName": "pm_recognition"
      },
      "Action Items": {
        "entitySetName": "pm_actionitems",
        "logicalName": "pm_actionitem"
      }
    }
  }
}
```

#### b) LocalConnectionReferences (External Connectors)
Defines connections to external services like Office 365, Teams, etc.

**Example:**
```json
{
  "58615322-5ecf-41d7-8809-6230f0c07bce": {
    "id": "58615322-5ecf-41d7-8809-6230f0c07bce",
    "dataSources": ["Office365Users"],
    "connectionParameters": {
      "sku": "Enterprise"
    },
    "connectionRef": {
      "id": "/providers/microsoft.powerapps/apis/shared_office365users",
      "displayName": "Office 365 Users",
      "iconUri": "https://connectoricons-prod.azureedge.net/releases/.../office365users/icon.png",
      "apiTier": "Standard"
    }
  }
}
```

**Common Connectors for Teams Apps:**
- `shared_office365users` - Office 365 Users (for user profiles, photos)
- `shared_teams` - Microsoft Teams (for team/channel info)
- `shared_office365` - Office 365 (for email)
- `shared_planner` - Planner (for task integration)

#### c) AppPreviewFlagsMap (Feature Flags)
Controls which Power Apps features are enabled for this app.

**Key Flags:**
- `delayloadscreens: true` - Improves performance by loading screens on demand
- `enableonstart: true` - Enables OnStart event on App control
- `nativecdsexperimental: true` - Uses optimized Dataverse connector
- `useguiddatatypes: true` - Uses GUID data types for lookups
- `componentauthoring: true` - Allows custom components

#### d) Basic App Metadata
```json
{
  "Name": "Performance Management",
  "Author": "",
  "DocumentAppType": "DesktopOrTablet",
  "DocumentLayoutWidth": 1366,
  "DocumentLayoutHeight": 768,
  "DocumentLayoutOrientation": "landscape",
  "DocumentType": "App"
}
```

### 3. Controls/1.json (App Root Control)
The App control is always `1.json` and contains the `OnStart` formula that runs when the app launches.

**Key Elements:**
- **OnStart**: Power Fx formula that initializes global variables, loads data into collections
- **Template**: References `http://microsoft.com/appmagic/appinfo`
- **Rules**: Array of property rules (OnStart, MinScreenWidth, MinScreenHeight, etc.)

**Example OnStart Pattern:**
```javascript
// Set loading state
Set(gblAppLoaded, false);

// Detect user language
Set(gblUserLanguage, Left(Language(), 2));

// Load theme parameters
Set(gblThemeDark, Param("theme") = "dark");
Set(gblTeamsContext, !IsBlank(Param("groupId")));

// Load reference data
ClearCollect(colStaffMembers, 'Staff Members');
ClearCollect(colEvalQuestions, 'Evaluation Questions');

// Mark app as loaded
Set(gblAppLoaded, true);
```

### 4. Controls/[N].json (Screen Controls)
Each screen and control has its own JSON file with a numeric ID.

**Structure:**
- **Template**: Control type (e.g., `http://microsoft.com/appmagic/screen`)
- **Name**: Control name (e.g., "scrHome", "galEvaluations")
- **Parent**: Parent control ID
- **Rules**: Array of property rules (OnVisible, Items, Fill, etc.)
- **Children**: Array of child control IDs

**Control Types:**
- `screen` - App screen
- `gallery` - Repeating list/grid
- `button` - Button
- `label` - Text label
- `text` - Text input
- `combobox` - Dropdown/combobox
- `groupContainer` - Container for grouping controls
- `rectangle` - Shape/divider
- `image` - Image control

### 5. References/DataSources.json
Contains metadata about all data sources (Dataverse entities and external connections) with their schemas and capabilities.

**Contains:**
- WADL (Web Application Description Language) XML for each connector
- Entity schemas (fields, types, relationships)
- Connector capabilities (filtering, sorting, pagination)

### 6. checksum.json
Contains SHA256 checksums for all files in the package to ensure integrity.

**Structure:**
```json
{
  "ClientStampedChecksum": "C8_<hash>",
  "ServerStampedChecksum": "",
  "ServerPerFileChecksums": {
    "Controls\\1.json": "C8_<hash>",
    "Header.json": "C8_<hash>",
    "Properties.json": "C8_<hash>",
    ...
  }
}
```

## Creating a Canvas App Manually: Challenges

After analyzing these apps, here are the key challenges with manually creating a .msapp file:

### 1. **Complexity**:
- Boards app (simple): 305+ controls across 12 screens
- Area Inspection (moderate): 425+ controls across 7 screens with 5 components
- Each control requires detailed JSON configuration

### 2. **Power Fx Formulas**:
- All logic is written in Power Fx (Excel-like formulas)
- Complex navigation, filtering, data manipulation
- Example: `Filter('Weekly Evaluations', pm_staffmember = gblCurrentUser && Year(pm_weekending) = gblCurrentYear)`

### 3. **Control Relationships**:
- Parent-child hierarchy must be maintained
- Control IDs must be unique and properly referenced
- Template IDs must match Power Apps control catalog

### 4. **Checksums**:
- All files must have valid SHA256 checksums
- Checksums must be updated whenever files change
- Format: `C8_<base64_encoded_hash>`

### 5. **DataSources.json**:
- Contains complex WADL XML for each connector
- Includes full entity schemas from Dataverse
- Generated automatically by Power Apps based on environment

### 6. **Unknown/Undocumented Fields**:
- Many fields in the JSON structure are not publicly documented
- Template IDs, control UUIDs, metadata keys
- Connector instance IDs, library dependencies

## Recommended Approach

### Option 1: Build in Power Apps Studio (RECOMMENDED)
1. Open Power Apps (https://make.powerapps.com)
2. Create new canvas app for Teams
3. Add Dataverse connection to your imported Performance Management tables
4. Design screens using visual designer
5. Write Power Fx formulas for business logic
6. Add app to PerformanceManagement solution
7. Export solution - this creates proper .msapp file

**Advantages:**
- Generates all complex JSON automatically
- Validates formulas and relationships
- Creates proper checksums
- Handles all undocumented fields correctly
- Visual drag-and-drop design
- IntelliSense for Power Fx formulas

### Option 2: Modify an Existing Template
1. Extract a similar Microsoft template (e.g., Boards or Area Inspection)
2. Modify Properties.json LocalDatabaseReferences to point to your entities
3. Update Controls to reference your entity fields instead of template fields
4. Update DataSources.json with your entity schemas
5. Recalculate all checksums
6. Test import

**Advantages:**
- Starts with working structure
- Faster than building from scratch
- Can reuse UI patterns

**Disadvantages:**
- Still very complex
- High risk of breaking something
- Checksum recalculation is tricky
- May have hidden dependencies on old entities

### Option 3: Minimal Starter App (EXPERIMENTAL)
Create a minimal canvas app with just a home screen that connects to your tables, then enhance in Power Apps Studio.

**Minimum Required Files:**
1. Header.json (version info)
2. Properties.json (with your LocalDatabaseReferences)
3. Controls/1.json (App control with basic OnStart)
4. Controls/3.json (Single home screen)
5. References/DataSources.json (generated from Dataverse)
6. Resources/PublishInfo.json
7. checksum.json (checksums for all above)

This would give you a working but basic app that you can then enhance visually.

## Next Steps for Performance Management App

**Recommended Path:**
1. ✅ **COMPLETED**: Import Dataverse tables (9 entities) - Version 2.0.0.7
2. **TODO**: Build canvas app in Power Apps Studio
   - Create screens: Home, Staff List, Evaluations, Self-Assessments, IDP, Goals, etc.
   - Connect to imported tables
   - Add business logic (filtering, calculations, navigation)
   - Design UI with Teams Fluent design principles
3. **TODO**: Add canvas app to solution in Power Apps
4. **TODO**: Export complete solution with tables + app
5. **TODO**: Test import in another Teams environment

**Alternative Experimental Path:**
1. ✅ **COMPLETED**: Import Dataverse tables
2. **EXPERIMENT**: Create minimal starter .msapp manually
3. Import minimal app to solution
4. Enhance in Power Apps Studio
5. Export and test

## Reference: Entity Schema Mapping

For reference, here's how to find the entitySetName and logicalName for your entities:

| Display Name | logicalName | entitySetName |
|--------------|-------------|---------------|
| Users (system) | systemuser | systemusers |
| Staff Member | pm_staffmember | pm_staffmembers |
| Weekly Evaluation | pm_weeklyevaluation | pm_weeklyevaluations |
| Self Evaluation | pm_selfevaluation | pm_selfevaluations |
| Evaluation Question | pm_evaluationquestion | pm_evaluationquestions |
| IDP Entry | pm_idpentry | pm_idpentries |
| Meeting Note | pm_meetingnote | pm_meetingnotes |
| Goal | pm_goal | pm_goals |
| Recognition | pm_recognition | pm_recognitions |
| Action Item | pm_actionitem | pm_actionitems |

**Note**: entitySetName is typically the logicalName + "s" (pluralized).

## Conclusion

While it is **theoretically possible** to create a canvas app .msapp file manually, it is **highly impractical** due to:
- Extreme complexity (hundreds of controls, each with dozens of properties)
- Undocumented internal structures
- Power Fx formula requirements
- Checksum validation
- Missing tooling for schema generation

**The Power Apps Studio approach is strongly recommended** as it handles all this complexity automatically while providing a visual designer and formula IntelliSense.

However, understanding the .msapp structure is valuable for:
- Debugging import issues
- Understanding how canvas apps work internally
- Potentially scripting bulk modifications to existing apps
- Creating custom tooling for app generation
