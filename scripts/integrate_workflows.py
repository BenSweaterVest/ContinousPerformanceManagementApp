#!/usr/bin/env python3
"""
Integrate Cloud Flows into Dataverse Solution

This script converts Power Automate Cloud Flow JSON files into proper
Dataverse workflow definitions and adds them to Customizations.xml.
"""

import json
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import base64

def generate_guid(name: str) -> str:
    """Generate a consistent GUID from a name (for demo purposes)"""
    import hashlib
    hash_obj = hashlib.md5(name.encode())
    hash_hex = hash_obj.hexdigest()
    return f"{hash_hex[:8]}-{hash_hex[8:12]}-{hash_hex[12:16]}-{hash_hex[16:20]}-{hash_hex[20:32]}"

def get_connection_references(workflows_dir: Path) -> dict:
    """Extract all unique connection references from workflow JSON files"""
    connections = {}

    for json_file in workflows_dir.glob("*.json"):
        with open(json_file, 'r') as f:
            flow_def = json.load(f)

        # Find all connectionName references
        flow_str = json.dumps(flow_def)
        conn_matches = re.findall(r'"connectionName":\s*"([^"]+)"', flow_str)

        for conn_name in set(conn_matches):
            if conn_name not in connections:
                # Map connection names to their APIs
                api_map = {
                    "shared_commondataserviceforapps": "/providers/Microsoft.PowerApps/apis/shared_commondataserviceforapps",
                    "shared_office365": "/providers/Microsoft.PowerApps/apis/shared_office365",
                    "shared_office365users": "/providers/Microsoft.PowerApps/apis/shared_office365users"
                }
                connections[conn_name] = {
                    "id": generate_guid(f"connref_{conn_name}"),
                    "name": conn_name.replace("shared_", ""),
                    "api": api_map.get(conn_name, f"/providers/Microsoft.PowerApps/apis/{conn_name}")
                }

    return connections

def create_connection_references_xml(connections: dict) -> str:
    """Generate XML for connection references"""
    xml_parts = []
    xml_parts.append('  <connectionreferences>')

    for conn_name, conn_info in connections.items():
        conn_id = conn_info['id']
        friendly_name = conn_info['name']
        api_id = conn_info['api']

        xml_parts.append(f'    <connectionreference connectionreferencelogicalname="cr_{friendly_name.lower()}">')
        xml_parts.append(f'      <connectionreferenceid>{conn_id}</connectionreferenceid>')
        xml_parts.append(f'      <connectionreferencedisplayname>{friendly_name} Connection</connectionreferencedisplayname>')
        xml_parts.append(f'      <connectorid>{api_id}</connectorid>')
        xml_parts.append(f'      <iscustomizable>1</iscustomizable>')
        xml_parts.append(f'      <statecode>0</statecode>')
        xml_parts.append(f'      <statuscode>1</statuscode>')
        xml_parts.append(f'    </connectionreference>')

    xml_parts.append('  </connectionreferences>')
    return '\n'.join(xml_parts)

def create_workflow_xml(flow_name: str, flow_json_path: Path, connections: dict) -> str:
    """Generate XML for a single workflow"""

    # Read flow definition
    with open(flow_json_path, 'r') as f:
        flow_def = json.load(f)

    # Generate workflow ID
    workflow_id = generate_guid(f"workflow_{flow_name}")

    # Replace connection names with connection references in the flow definition
    flow_str = json.dumps(flow_def, indent=2)
    for conn_name, conn_info in connections.items():
        ref_name = f"cr_{conn_info['name'].lower()}"
        # Replace connection references
        flow_str = flow_str.replace(
            f'"connectionName": "{conn_name}"',
            f'"connectionName": "@connectionReferences(\'{ref_name}\')"'
        )

    # Base64 encode the flow definition for embedding
    flow_encoded = base64.b64encode(flow_str.encode()).decode()

    # Determine trigger type
    trigger_type = "Recurrence"  # Default
    if "triggers" in flow_def:
        trigger_keys = list(flow_def["triggers"].keys())
        if trigger_keys:
            first_trigger = flow_def["triggers"][trigger_keys[0]]
            trigger_type = first_trigger.get("type", "Recurrence")

    # Create friendly name
    friendly_name = flow_name.replace("_", " ")

    xml_parts = []
    xml_parts.append(f'    <Workflow WorkflowId="{workflow_id}" Name="{flow_name}">')
    xml_parts.append(f'      <WorkflowIdUnique>{workflow_id}</WorkflowIdUnique>')
    xml_parts.append(f'      <Name>{friendly_name}</Name>')
    xml_parts.append(f'      <Type>1</Type>') # 1 = Definition (Cloud Flow)
    xml_parts.append(f'      <Category>5</Category>') # 5 = Modern Flow
    xml_parts.append(f'      <Mode>0</Mode>') # 0 = Background
    xml_parts.append(f'      <Scope>4</Scope>') # 4 = Organization
    xml_parts.append(f'      <OnDemand>0</OnDemand>')
    xml_parts.append(f'      <Subprocess>0</Subprocess>')
    xml_parts.append(f'      <StateCode>1</StateCode>') # 1 = Activated
    xml_parts.append(f'      <StatusCode>2</StatusCode>') # 2 = Activated
    xml_parts.append(f'      <IsTransacted>1</IsTransacted>')
    xml_parts.append(f'      <IntroducedVersion>1.0.0.0</IntroducedVersion>')
    xml_parts.append(f'      <IsCustomizable>1</IsCustomizable>')
    xml_parts.append(f'      <TriggerOnCreate>0</TriggerOnCreate>')
    xml_parts.append(f'      <TriggerOnDelete>0</TriggerOnDelete>')
    xml_parts.append(f'      <AsyncAutodelete>0</AsyncAutodelete>')
    xml_parts.append(f'      <SyncWorkflowLogOnFailure>0</SyncWorkflowLogOnFailure>')
    xml_parts.append(f'      <StateCode>1</StateCode>')
    xml_parts.append(f'      <StatusCode>2</StatusCode>')

    # Add the flow definition as ClientData (this is where Power Automate stores the JSON)
    xml_parts.append(f'      <ClientData>')
    xml_parts.append(f'        <FlowDefinition>{flow_encoded}</FlowDefinition>')
    xml_parts.append(f'        <FlowTriggerType>{trigger_type}</FlowTriggerType>')
    xml_parts.append(f'      </ClientData>')

    xml_parts.append(f'    </Workflow>')

    return '\n'.join(xml_parts)

def main():
    # Paths
    project_root = Path(__file__).parent.parent
    workflows_dir = project_root / "solution" / "Workflows"
    customizations_file = project_root / "solution" / "Other" / "Customizations.xml"

    print("🔄 Integrating Cloud Flows into Dataverse solution...")

    # Get all connection references
    print("\n📡 Extracting connection references...")
    connections = get_connection_references(workflows_dir)
    for conn_name, conn_info in connections.items():
        print(f"   ✓ {conn_name} → {conn_info['name']}")

    # Generate connection references XML
    conn_refs_xml = create_connection_references_xml(connections)

    # Generate workflow XML for each JSON file
    print("\n⚙️  Generating workflow definitions...")
    workflows_xml_parts = ['  <Workflows>']

    for json_file in sorted(workflows_dir.glob("*.json")):
        flow_name = json_file.stem
        print(f"   ✓ {flow_name}")
        workflow_xml = create_workflow_xml(flow_name, json_file, connections)
        workflows_xml_parts.append(workflow_xml)

    workflows_xml_parts.append('  </Workflows>')
    workflows_xml = '\n'.join(workflows_xml_parts)

    # Read current Customizations.xml
    print("\n📝 Updating Customizations.xml...")
    with open(customizations_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace <Workflows /> with actual workflows
    if '<Workflows />' in content:
        content = content.replace('<Workflows />', workflows_xml)
        print("   ✓ Replaced <Workflows /> with workflow definitions")
    else:
        print("   ⚠️  WARNING: <Workflows /> tag not found, appending workflows before </ImportExportXml>")
        content = content.replace('</ImportExportXml>', f'{workflows_xml}\n</ImportExportXml>')

    # Add connection references after <Entities>...</Entities>
    if '<connectionreferences>' not in content:
        # Find where to insert (after </Entities>)
        entities_end = content.find('</Entities>')
        if entities_end > 0:
            # Find the next newline after </Entities>
            insert_pos = content.find('\n', entities_end) + 1
            content = content[:insert_pos] + '\n' + conn_refs_xml + '\n' + content[insert_pos:]
            print("   ✓ Added connection references")
        else:
            print("   ⚠️  WARNING: Could not find </Entities> tag")
    else:
        print("   ℹ️  Connection references already exist")

    # Write updated Customizations.xml
    with open(customizations_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Successfully integrated {len(list(workflows_dir.glob('*.json')))} Cloud Flows")
    print(f"   • {len(connections)} connection references added")
    print(f"   • Updated: {customizations_file}")

    print("\n📋 Next steps:")
    print("   1. Commit these changes")
    print("   2. Build the solution package")
    print("   3. Import into Dataverse for Teams")
    print("   4. Configure connections in Power Automate after import")

if __name__ == "__main__":
    main()
