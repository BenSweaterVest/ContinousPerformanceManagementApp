#!/usr/bin/env python3
"""
Add missing system relationships to customizations.xml
Fixes the AsyncOperation relationship creation error
"""

# Entity list
ENTITIES = [
    ("pm_StaffMember", "pm_staffmember"),
    ("pm_EvaluationQuestion", "pm_evaluationquestion"),
    ("pm_WeeklyEvaluation", "pm_weeklyevaluation"),
    ("pm_SelfEvaluation", "pm_selfevaluation"),
    ("pm_IDPEntry", "pm_idpentry"),
    ("pm_MeetingNote", "pm_meetingnote"),
    ("pm_Goal", "pm_goal"),
    ("pm_Recognition", "pm_recognition"),
    ("pm_ActionItem", "pm_actionitem"),
]

def generate_system_relationship(rel_name, rel_type, referencing_entity, referenced_entity, referencing_attr):
    """Generate XML for a system relationship"""
    return f"""    <EntityRelationship Name="{rel_name}">
      <EntityRelationshipType>OneToMany</EntityRelationshipType>
      <IsCustomRelationship>0</IsCustomRelationship>
      <IntroducedVersion>2.0.0.0</IntroducedVersion>
      <IsHierarchical>0</IsHierarchical>
      <ReferencingEntityName>{referencing_entity}</ReferencingEntityName>
      <ReferencedEntityName>{referenced_entity}</ReferencedEntityName>
      <CascadeAssign>NoCascade</CascadeAssign>
      <CascadeDelete>NoCascade</CascadeDelete>
      <CascadeReparent>NoCascade</CascadeReparent>
      <CascadeShare>NoCascade</CascadeShare>
      <CascadeUnshare>NoCascade</CascadeUnshare>
      <CascadeArchive>NoCascade</CascadeArchive>
      <ReferencingAttributeName>{referencing_attr}</ReferencingAttributeName>
      <RelationshipDescription>
        <Descriptions>
          <Description description="" languagecode="1033" />
        </Descriptions>
      </RelationshipDescription>
      <IsCustomizable>1</IsCustomizable>
      <IsValidForAdvancedFind>{"1" if "createdby" in rel_name or "modifiedby" in rel_name or "owner" in rel_name else "0"}</IsValidForAdvancedFind>
      <SchemaName>{rel_name}</SchemaName>
      <SecurityTypes>Append</SecurityTypes>
    </EntityRelationship>
"""

print("Generating system relationships for 9 entities...")
print()

all_relationships = []

for pascal_name, schema_name in ENTITIES:
    # 1. Business Unit relationship
    all_relationships.append(generate_system_relationship(
        f"business_unit_{schema_name}",
        "OneToMany",
        pascal_name,
        "BusinessUnit",
        "owningbusinessunit"
    ))

    # 2. Created By relationship
    all_relationships.append(generate_system_relationship(
        f"lk_{schema_name}_createdby",
        "OneToMany",
        pascal_name,
        "SystemUser",
        "createdby"
    ))

    # 3. Modified By relationship
    all_relationships.append(generate_system_relationship(
        f"lk_{schema_name}_modifiedby",
        "OneToMany",
        pascal_name,
        "SystemUser",
        "modifiedby"
    ))

    # 4. Owner relationship
    all_relationships.append(generate_system_relationship(
        f"owner_{schema_name}",
        "OneToMany",
        pascal_name,
        "Owner",
        "ownerid"
    ))

    # 5. Team relationship
    all_relationships.append(generate_system_relationship(
        f"team_{schema_name}",
        "OneToMany",
        pascal_name,
        "Team",
        "owningteam"
    ))

    # 6. User relationship
    all_relationships.append(generate_system_relationship(
        f"user_{schema_name}",
        "OneToMany",
        pascal_name,
        "SystemUser",
        "owninguser"
    ))

print(f"Generated {len(all_relationships)} system relationships (6 per entity × 9 entities)")
print()

# Read existing customizations.xml
print("Reading existing customizations.xml...")
with open('/home/user/ContinousPerformanceManagementApp/solution/Other/Customizations.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# Find where to insert (after <EntityRelationships> opening tag, before first custom relationship)
insert_marker = "  <EntityRelationships>\n"
if insert_marker in content:
    parts = content.split(insert_marker, 1)

    # Insert system relationships first
    new_content = parts[0] + insert_marker + "\n"
    new_content += "    <!-- System Relationships (6 per entity × 9 entities = 54 total) -->\n"
    new_content += "".join(all_relationships)
    new_content += "\n    <!-- Custom Entity Relationships -->\n"
    new_content += parts[1]

    # Write back
    print("Writing updated customizations.xml...")
    with open('/home/user/ContinousPerformanceManagementApp/solution/Other/Customizations.xml', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("✓ Successfully added 54 system relationships")
    print("✓ File updated: solution/Other/Customizations.xml")

    # Count lines
    lines = len(new_content.split('\n'))
    print(f"✓ New file size: {lines} lines")
else:
    print("ERROR: Could not find EntityRelationships section")
