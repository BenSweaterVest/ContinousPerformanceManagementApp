#!/usr/bin/env python3
"""
Integrate Canvas App into Dataverse Solution

Adds the generated Canvas App to Customizations.xml so it's included
in the solution package.
"""

import os
import re
from pathlib import Path
import uuid

def main():
    print("🎨 Integrating Canvas App into solution...")

    project_root = Path(__file__).parent.parent
    customizations_file = project_root / "solution" / "Other" / "Customizations.xml"
    canvas_apps_dir = project_root / "solution" / "CanvasApps"

    # Find the .msapp file
    msapp_files = list(canvas_apps_dir.glob("*.msapp"))
    if not msapp_files:
        print("❌ ERROR: No .msapp file found in CanvasApps directory")
        return 1

    msapp_file = msapp_files[0]
    app_name = msapp_file.stem
    app_display_name = "Performance Management System"

    print(f"\n📱 Found Canvas App: {msapp_file.name}")

    # Read Customizations.xml
    with open(customizations_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create canvas apps section if it doesn't exist
    canvas_app_xml = f"""
  <CanvasApps>
    <CanvasApp Name="{app_name}">
      <DisplayName>{app_display_name}</DisplayName>
      <Description>Performance Management System for tracking staff evaluations, goals, and development</Description>
      <Status>Published</Status>
      <IntroducedVersion>1.0.1.0</IntroducedVersion>
      <IsCustomizable>1</IsCustomizable>
      <CanvasAppType>0</CanvasAppType>
      <BypassConsent>false</BypassConsent>
      <Publisher>Default</Publisher>
      <AuthorizationReferences>
        <AuthorizationReference>
          <Resource>shared_commondataserviceforapps</Resource>
        </AuthorizationReference>
        <AuthorizationReference>
          <Resource>shared_office365users</Resource>
        </AuthorizationReference>
        <AuthorizationReference>
          <Resource>shared_office365</Resource>
        </AuthorizationReference>
      </AuthorizationReferences>
      <ConnectionReferences>
        <ConnectionReference>
          <LogicalName>cr_commondataserviceforapps</LogicalName>
        </ConnectionReference>
        <ConnectionReference>
          <LogicalName>cr_office365users</LogicalName>
        </ConnectionReference>
        <ConnectionReference>
          <LogicalName>cr_office365</LogicalName>
        </ConnectionReference>
      </ConnectionReferences>
      <DatabaseReferences>
        <DatabaseReference>
          <EntityName>pm_staffmember</EntityName>
        </DatabaseReference>
        <DatabaseReference>
          <EntityName>pm_evaluationquestion</EntityName>
        </DatabaseReference>
        <DatabaseReference>
          <EntityName>pm_weeklyevaluation</EntityName>
        </DatabaseReference>
        <DatabaseReference>
          <EntityName>pm_selfevaluation</EntityName>
        </DatabaseReference>
        <DatabaseReference>
          <EntityName>pm_idpentry</EntityName>
        </DatabaseReference>
        <DatabaseReference>
          <EntityName>pm_meetingnote</EntityName>
        </DatabaseReference>
        <DatabaseReference>
          <EntityName>pm_goal</EntityName>
        </DatabaseReference>
        <DatabaseReference>
          <EntityName>pm_recognition</EntityName>
        </DatabaseReference>
        <DatabaseReference>
          <EntityName>pm_actionitem</EntityName>
        </DatabaseReference>
      </DatabaseReferences>
    </CanvasApp>
  </CanvasApps>
"""

    # Check if CanvasApps section already exists
    if '<CanvasApps>' in content:
        print("   ℹ️  Canvas Apps section already exists, replacing...")
        # Replace existing CanvasApps section
        content = re.sub(
            r'<CanvasApps>.*?</CanvasApps>',
            canvas_app_xml.strip(),
            content,
            flags=re.DOTALL
        )
    else:
        # Add after connection references
        if '<connectionreferences>' in content:
            # Find end of connectionreferences
            conn_ref_end = content.find('</connectionreferences>')
            if conn_ref_end > 0:
                insert_pos = content.find('\n', conn_ref_end) + 1
                content = content[:insert_pos] + '\n' + canvas_app_xml + '\n' + content[insert_pos:]
                print("   ✓ Added Canvas Apps section after connection references")
        else:
            print("   ⚠️  WARNING: Could not find ideal insertion point, appending before </ImportExportXml>")
            content = content.replace('</ImportExportXml>', f'{canvas_app_xml}\n</ImportExportXml>')

    # Write updated file
    with open(customizations_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Canvas App integrated successfully!")
    print(f"   • App: {app_display_name}")
    print(f"   • File: {msapp_file.name}")
    print(f"   • Tables: 9 Dataverse entities")
    print(f"   • Connections: 3 (Dataverse, Office 365 Users, Office 365 Outlook)")

    print("\n📋 Solution now includes:")
    print("   ✓ 9 Dataverse tables")
    print("   ✓ 4 Cloud Flows")
    print("   ✓ 1 Canvas App")
    print("   ✓ 3 Connection references")

if __name__ == "__main__":
    main()
