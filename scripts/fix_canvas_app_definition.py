#!/usr/bin/env python3
"""
Fix Canvas App Definition to Match Microsoft's Structure

Based on analysis of Microsoft Boards solution, fixes the Canvas App
definition to match the correct structure and avoid import errors.
"""

import re
from pathlib import Path
import json

def create_proper_canvas_app_definition(app_name: str) -> str:
    """Create Canvas App definition matching Microsoft's structure"""

    # Connection references as JSON (matching Microsoft's format)
    connection_refs_json = json.dumps({
        "cr_commondataserviceforapps": {
            "id": "/providers/microsoft.powerapps/apis/shared_commondataserviceforapps",
            "displayName": "Microsoft Dataverse",
            "dataSources": ["pm_staffmembers", "pm_evaluationquestions", "pm_weeklyevaluations",
                          "pm_selfevaluations", "pm_idpentries", "pm_meetingnotes",
                          "pm_goals", "pm_recognitions", "pm_actionitems"],
            "apiTier": "Standard"
        },
        "cr_office365users": {
            "id": "/providers/microsoft.powerapps/apis/shared_office365users",
            "displayName": "Office 365 Users",
            "apiTier": "Standard"
        },
        "cr_office365": {
            "id": "/providers/microsoft.powerapps/apis/shared_office365",
            "displayName": "Office 365 Outlook",
            "apiTier": "Standard"
        }
    })

    # Database references as JSON (matching Microsoft's format)
    database_refs_json = json.dumps({
        "default.cds": {
            "databaseDetails": {
                "referenceType": "Environmental",
                "environmentName": "default.cds"
            },
            "dataSources": {
                "Staff Members": {"entitySetName": "pm_staffmembers", "logicalName": "pm_staffmember"},
                "Evaluation Questions": {"entitySetName": "pm_evaluationquestions", "logicalName": "pm_evaluationquestion"},
                "Weekly Evaluations": {"entitySetName": "pm_weeklyevaluations", "logicalName": "pm_weeklyevaluation"},
                "Self Evaluations": {"entitySetName": "pm_selfevaluations", "logicalName": "pm_selfevaluation"},
                "IDP Entries": {"entitySetName": "pm_idpentries", "logicalName": "pm_idpentry"},
                "Meeting Notes": {"entitySetName": "pm_meetingnotes", "logicalName": "pm_meetingnote"},
                "Goals": {"entitySetName": "pm_goals", "logicalName": "pm_goal"},
                "Recognitions": {"entitySetName": "pm_recognitions", "logicalName": "pm_recognition"},
                "Action Items": {"entitySetName": "pm_actionitems", "logicalName": "pm_actionitem"}
            }
        }
    })

    # Tags as JSON
    tags_json = json.dumps({
        "primaryDeviceWidth": "1366",
        "primaryDeviceHeight": "768",
        "supportsPortrait": "true",
        "supportsLandscape": "true",
        "primaryFormFactor": "Tablet",
        "hasComponent": "false",
        "isUnifiedRootApp": "false"
    })

    # Create CDS dependencies
    cds_deps = {
        "cdsdependencies": [
            {"logicalname": "pm_staffmember", "componenttype": 1},
            {"logicalname": "pm_evaluationquestion", "componenttype": 1},
            {"logicalname": "pm_weeklyevaluation", "componenttype": 1},
            {"logicalname": "pm_selfevaluation", "componenttype": 1},
            {"logicalname": "pm_idpentry", "componenttype": 1},
            {"logicalname": "pm_meetingnote", "componenttype": 1},
            {"logicalname": "pm_goal", "componenttype": 1},
            {"logicalname": "pm_recognition", "componenttype": 1},
            {"logicalname": "pm_actionitem", "componenttype": 1}
        ]
    }
    cds_deps_json = json.dumps(cds_deps)

    # Build Canvas App XML (matching Microsoft's structure exactly)
    canvas_app_xml = f"""  <CanvasApps>
    <CanvasApp>
      <Name>{app_name}</Name>
      <AppVersion>2025-11-15T00:00:00Z</AppVersion>
      <Status>Ready</Status>
      <CreatedByClientVersion>3.24</CreatedByClientVersion>
      <MinClientVersion>3.24</MinClientVersion>
      <Tags>{tags_json}</Tags>
      <IsCdsUpgraded>0</IsCdsUpgraded>
      <GalleryItemId xsi:nil="true"></GalleryItemId>
      <BackgroundColor>rgba(0, 120, 212, 1)</BackgroundColor>
      <DisplayName>Performance Management System</DisplayName>
      <Description>Continuous performance management with weekly evaluations and quarterly self-assessments</Description>
      <CommitMessage xsi:nil="true"></CommitMessage>
      <Publisher xsi:nil="true"></Publisher>
      <AuthorizationReferences>[]</AuthorizationReferences>
      <ConnectionReferences>{connection_refs_json}</ConnectionReferences>
      <DatabaseReferences>{database_refs_json}</DatabaseReferences>
      <AppComponents>[]</AppComponents>
      <AppComponentDependencies>[]</AppComponentDependencies>
      <CanConsumeAppPass>1</CanConsumeAppPass>
      <CanvasAppType>0</CanvasAppType>
      <BypassConsent>0</BypassConsent>
      <AdminControlBypassConsent>0</AdminControlBypassConsent>
      <EmbeddedApp xsi:nil="true"></EmbeddedApp>
      <IntroducedVersion>1.0</IntroducedVersion>
      <CdsDependencies>{cds_deps_json}</CdsDependencies>
      <IsCustomizable>1</IsCustomizable>
      <DocumentUri>/CanvasApps/{app_name}.msapp</DocumentUri>
    </CanvasApp>
  </CanvasApps>"""

    return canvas_app_xml

def add_xsi_namespace(content: str) -> str:
    """Add xsi namespace to ImportExportXml root if not present"""
    if 'xmlns:xsi=' not in content:
        content = content.replace(
            '<ImportExportXml',
            '<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
            1
        )
    return content

def main():
    print("🔧 Fixing Canvas App definition to match Microsoft's structure...\n")

    project_root = Path(__file__).parent.parent
    customizations_file = project_root / "solution" / "Other" / "Customizations.xml"
    canvas_apps_dir = project_root / "solution" / "CanvasApps"

    # Find the .msapp file
    msapp_files = list(canvas_apps_dir.glob("*.msapp"))
    if not msapp_files:
        print("❌ ERROR: No .msapp file found in CanvasApps directory")
        return 1

    app_name = msapp_files[0].stem
    print(f"📱 Canvas App: {app_name}")

    # Read Customizations.xml
    with open(customizations_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add xsi namespace if needed
    content = add_xsi_namespace(content)

    # Create new Canvas App definition
    new_canvas_app = create_proper_canvas_app_definition(app_name)

    # Replace existing CanvasApps section
    if '<CanvasApps>' in content:
        print("   ✓ Replacing existing Canvas Apps section")
        content = re.sub(
            r'<CanvasApps>.*?</CanvasApps>',
            new_canvas_app.strip(),
            content,
            flags=re.DOTALL
        )
    else:
        print("   ✓ Adding Canvas Apps section")
        # Add before closing tag
        content = content.replace('</ImportExportXml>', f'{new_canvas_app}\n</ImportExportXml>')

    # Write updated file
    with open(customizations_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Canvas App definition fixed!")
    print("\nKey changes:")
    print("   ✓ Name as child element (not attribute)")
    print("   ✓ Status: 'Ready' (not 'Published')")
    print("   ✓ BypassConsent: 0 (not 'false')")
    print("   ✓ IntroducedVersion: '1.0' (not '1.0.1.0')")
    print("   ✓ Added xsi:nil for null fields")
    print("   ✓ ConnectionReferences as JSON")
    print("   ✓ DatabaseReferences as JSON")
    print("   ✓ Added DocumentUri pointing to .msapp")
    print("   ✓ Added all Microsoft-standard fields")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
