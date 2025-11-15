#!/usr/bin/env python3
"""
Generate EntityRelationship definitions for all custom lookup fields.
Based on Microsoft Boards solution structure.
"""

import re
from pathlib import Path

entities = [
    'pm_staffmember',
    'pm_evaluationquestion',
    'pm_weeklyevaluation',
    'pm_selfevaluation',
    'pm_idpentry',
    'pm_meetingnote',
    'pm_goal',
    'pm_recognition',
    'pm_actionitem'
]

tables_path = Path('/home/user/ContinousPerformanceManagementApp/solution/Tables')

lookups = []

for entity in entities:
    entity_file = tables_path / entity / 'Entity.xml'

    with open(entity_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all custom lookup attributes (pm_ prefix only, exclude system fields)
    # Pattern: find attribute with PhysicalName="pm_something" that has Type=lookup and Targets
    lookup_pattern = r'<attribute PhysicalName="(pm_\w+)">.*?<Type>lookup</Type>.*?<Name>(pm_\w+)</Name>.*?<Targets>\s*<Target>(.*?)</Target>\s*</Targets>'
    lookup_matches = re.findall(lookup_pattern, content, re.DOTALL)

    for physical_name, logical_name, target_entity in lookup_matches:
        # Skip if this is the primary key field (those shouldn't be lookups)
        if logical_name == f"{entity}id":
            continue

        lookups.append({
            'entity': entity,
            'physical_name': physical_name,
            'logical_name': logical_name,
            'target': target_entity
        })
        print(f"{entity}.{logical_name} -> {target_entity}")

print(f"\nTotal custom lookup fields needing relationships: {len(lookups)}")

# Generate EntityRelationship XML for each lookup
relationships_xml = []

for lookup in lookups:
    # Relationship name format: [ReferencedEntity]_[lookupfield]_[ReferencingEntity]
    # For systemuser lookups: systemuser_[fieldname]_[entity]
    # For custom entity lookups: [targetentity]_[fieldname]_[entity]

    referenced_entity = lookup['target']
    referencing_entity = lookup['entity']
    field_name = lookup['logical_name']

    # Create relationship name (truncated to avoid long names)
    if referenced_entity == 'systemuser':
        rel_name = f"systemuser_{field_name}_{referencing_entity}"
    else:
        rel_name = f"{referenced_entity}_{field_name}_{referencing_entity}"

    # Capitalize first letter of entities for display
    ref_display = referenced_entity.replace('pm_', '').replace('_', ' ').title()
    refing_display = referencing_entity.replace('pm_', '').replace('_', ' ').title()

    relationship_xml = f'''    <EntityRelationship Name="{rel_name}">
      <EntityRelationshipType>OneToMany</EntityRelationshipType>
      <IsCustomizable>1</IsCustomizable>
      <IntroducedVersion>1.0.0.0</IntroducedVersion>
      <IsHierarchical>0</IsHierarchical>
      <ReferencingEntityName>{referencing_entity}</ReferencingEntityName>
      <ReferencedEntityName>{referenced_entity}</ReferencedEntityName>
      <CascadeAssign>NoCascade</CascadeAssign>
      <CascadeDelete>RemoveLink</CascadeDelete>
      <CascadeReparent>NoCascade</CascadeReparent>
      <CascadeShare>NoCascade</CascadeShare>
      <CascadeUnshare>NoCascade</CascadeUnshare>
      <CascadeRollupView>NoCascade</CascadeRollupView>
      <IsValidForAdvancedFind>1</IsValidForAdvancedFind>
      <ReferencingAttributeName>{field_name}</ReferencingAttributeName>
      <RelationshipDescription>
        <Descriptions>
          <Description description="{ref_display} to {refing_display} relationship" languagecode="1033" />
        </Descriptions>
      </RelationshipDescription>
      <EntityRelationshipRoles>
        <EntityRelationshipRole>
          <NavPaneDisplayOption>UseCollectionName</NavPaneDisplayOption>
          <NavPaneArea>Details</NavPaneArea>
          <NavPaneOrder>10000</NavPaneOrder>
          <NavigationPropertyName>{field_name}</NavigationPropertyName>
          <RelationshipRoleType>1</RelationshipRoleType>
        </EntityRelationshipRole>
        <EntityRelationshipRole>
          <NavigationPropertyName>{rel_name}</NavigationPropertyName>
          <RelationshipRoleType>0</RelationshipRoleType>
        </EntityRelationshipRole>
      </EntityRelationshipRoles>
    </EntityRelationship>'''

    relationships_xml.append(relationship_xml)

# Write to file
output_file = Path('/home/user/ContinousPerformanceManagementApp/relationships.xml')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('  <EntityRelationships>\n')
    for rel in relationships_xml:
        f.write(rel + '\n')
    f.write('  </EntityRelationships>\n')

print(f"\nGenerated {len(relationships_xml)} relationships")
print(f"Saved to {output_file}")
