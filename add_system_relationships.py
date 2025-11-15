#!/usr/bin/env python3
"""
Add system entity relationships that Dataverse expects for UserOwned entities.

Microsoft's solutions include 6 system relationships for EACH entity:
1. business_unit_<entity> - for OwningBusinessUnit
2. lk_<entity>_createdby - for CreatedBy
3. lk_<entity>_modifiedby - for ModifiedBy
4. owner_<entity> - for OwnerId
5. team_<entity> - for OwningTeam
6. user_<entity> - for OwningUser

Without these, the import fails when Dataverse tries to create automatic system relationships.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

# Our 9 custom entities
ENTITIES = [
    "pm_staffmember",
    "pm_evaluationquestion",
    "pm_weeklyevaluation",
    "pm_selfevaluation",
    "pm_idpentry",
    "pm_meetingnote",
    "pm_goal",
    "pm_recognition",
    "pm_actionitem"
]

# System relationship templates
SYSTEM_RELATIONSHIPS = [
    {
        "name_template": "business_unit_{entity}",
        "referenced_entity": "BusinessUnit",
        "attribute_name": "OwningBusinessUnit",
        "description": "Unique identifier for the business unit that owns the record"
    },
    {
        "name_template": "lk_{entity}_createdby",
        "referenced_entity": "SystemUser",
        "attribute_name": "CreatedBy",
        "description": "Unique identifier of the user who created the record."
    },
    {
        "name_template": "lk_{entity}_modifiedby",
        "referenced_entity": "SystemUser",
        "attribute_name": "ModifiedBy",
        "description": "Unique identifier of the user who modified the record."
    },
    {
        "name_template": "owner_{entity}",
        "referenced_entity": "Owner",
        "attribute_name": "OwnerId",
        "description": "Owner Id"
    },
    {
        "name_template": "team_{entity}",
        "referenced_entity": "Team",
        "attribute_name": "OwningTeam",
        "description": "Unique identifier for the team that owns the record."
    },
    {
        "name_template": "user_{entity}",
        "referenced_entity": "SystemUser",
        "attribute_name": "OwningUser",
        "description": "Unique identifier for the user that owns the record."
    }
]


def create_system_relationship_xml(entity_name, rel_template):
    """Create XML for a single system relationship"""
    # Get entity display name (capitalized) for XML
    entity_display = entity_name.replace("pm_", "").capitalize()

    xml = f'''    <EntityRelationship Name="{rel_template['name_template'].format(entity=entity_name)}">
      <EntityRelationshipType>OneToMany</EntityRelationshipType>
      <IsCustomizable>1</IsCustomizable>
      <IntroducedVersion>1.0</IntroducedVersion>
      <IsHierarchical>0</IsHierarchical>
      <ReferencingEntityName>{entity_name}</ReferencingEntityName>
      <ReferencedEntityName>{rel_template['referenced_entity']}</ReferencedEntityName>
      <CascadeAssign>NoCascade</CascadeAssign>
      <CascadeDelete>NoCascade</CascadeDelete>
      <CascadeReparent>NoCascade</CascadeReparent>
      <CascadeShare>NoCascade</CascadeShare>
      <CascadeUnshare>NoCascade</CascadeUnshare>
      <ReferencingAttributeName>{rel_template['attribute_name']}</ReferencingAttributeName>
      <RelationshipDescription>
        <Descriptions>
          <Description description="{rel_template['description']}" languagecode="1033" />
        </Descriptions>
      </RelationshipDescription>
    </EntityRelationship>
'''
    return xml


def main():
    customizations_path = Path("solution/Other/Customizations.xml")

    if not customizations_path.exists():
        print(f"❌ Error: {customizations_path} not found")
        return 1

    print(f"📖 Reading {customizations_path}...")
    with open(customizations_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the EntityRelationships section
    relationships_start = content.find("<EntityRelationships>")
    if relationships_start == -1:
        print("❌ Error: <EntityRelationships> section not found")
        return 1

    # Find the first existing relationship (after the opening tag)
    first_relationship = content.find("<EntityRelationship", relationships_start + 21)

    if first_relationship == -1:
        print("❌ Error: No existing relationships found")
        return 1

    print(f"\n✅ Found EntityRelationships section at position {relationships_start}")
    print(f"✅ First existing relationship at position {first_relationship}")

    # Generate all system relationships
    system_rels_xml = ""
    relationship_count = 0

    print(f"\n🔧 Generating system relationships for {len(ENTITIES)} entities...")
    for entity in ENTITIES:
        print(f"   • {entity}")
        for rel_template in SYSTEM_RELATIONSHIPS:
            system_rels_xml += create_system_relationship_xml(entity, rel_template)
            relationship_count += 1

    # Insert system relationships BEFORE existing custom relationships
    new_content = (
        content[:first_relationship] +
        system_rels_xml +
        content[first_relationship:]
    )

    # Write back
    print(f"\n💾 Writing updated Customizations.xml with {relationship_count} new system relationships...")
    with open(customizations_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    new_size = len(new_content)
    old_size = len(content)
    added_chars = new_size - old_size

    print(f"\n✅ Success!")
    print(f"   • Added {relationship_count} system relationships")
    print(f"   • File size: {old_size:,} → {new_size:,} chars ({added_chars:,} added)")
    print(f"   • New total: {relationship_count + 13} relationships")  # 13 existing custom
    print(f"\n📊 System relationships per entity:")
    print(f"   • business_unit_pm_<entity>")
    print(f"   • lk_pm_<entity>_createdby")
    print(f"   • lk_pm_<entity>_modifiedby")
    print(f"   • owner_pm_<entity>")
    print(f"   • team_pm_<entity>")
    print(f"   • user_pm_<entity>")

    return 0


if __name__ == "__main__":
    exit(main())
