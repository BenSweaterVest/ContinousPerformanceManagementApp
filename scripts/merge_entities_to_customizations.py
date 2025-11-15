#!/usr/bin/env python3
"""
Merge all Entity.xml files into Customizations.xml to match Microsoft's structure.

Microsoft's working solutions have ALL entity definitions embedded in customizations.xml,
not in separate files. This script merges our separate Entity.xml files into a single
customizations.xml file that Dataverse can properly import.
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path

def merge_entities():
    """Merge all Entity.xml files into Customizations.xml"""

    # Read the current Customizations.xml template
    customizations_path = Path('/home/user/ContinousPerformanceManagementApp/solution/Other/Customizations.xml')

    # Create the root structure
    root = ET.Element('ImportExportXml')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

    entities_elem = ET.SubElement(root, 'Entities')

    # Entity definitions with their display names
    entity_configs = [
        ('pm_staffmember', 'Staff Member'),
        ('pm_evaluationquestion', 'Evaluation Question'),
        ('pm_weeklyevaluation', 'Weekly Evaluation'),
        ('pm_selfevaluation', 'Self Evaluation'),
        ('pm_idpentry', 'IDP Entry'),
        ('pm_meetingnote', 'Meeting Note'),
        ('pm_goal', 'Goal'),
        ('pm_recognition', 'Recognition'),
        ('pm_actionitem', 'Action Item'),
    ]

    tables_path = Path('/home/user/ContinousPerformanceManagementApp/solution/Tables')

    for entity_name, display_name in entity_configs:
        entity_xml_path = tables_path / entity_name / 'Entity.xml'

        if not entity_xml_path.exists():
            print(f"  ✗ Entity.xml not found for {entity_name}")
            continue

        print(f"Processing {entity_name}...")

        # Parse the Entity.xml file
        entity_tree = ET.parse(entity_xml_path)
        entity_root = entity_tree.getroot()

        # Create the Entity wrapper
        entity_wrapper = ET.SubElement(entities_elem, 'Entity')

        # Add the Name element with LocalizedName and OriginalName attributes
        name_elem = ET.SubElement(entity_wrapper, 'Name')
        name_elem.set('LocalizedName', display_name)
        name_elem.set('OriginalName', display_name)
        name_elem.text = entity_name

        # Find and copy the EntityInfo element from Entity.xml
        entity_info = entity_root.find('.//EntityInfo')
        if entity_info is not None:
            entity_wrapper.append(entity_info)
            print(f"  ✓ Added EntityInfo for {entity_name}")
        else:
            print(f"  ✗ EntityInfo not found in {entity_name}")

        # Find and copy FormXml if it exists
        form_xml = entity_root.find('.//FormXml')
        if form_xml is not None:
            entity_wrapper.append(form_xml)
            print(f"  ✓ Added FormXml for {entity_name}")

        # Find and copy RibbonDiffXml if it exists
        ribbon_diff = entity_root.find('.//RibbonDiffXml')
        if ribbon_diff is not None:
            entity_wrapper.append(ribbon_diff)

        # Find and copy CustomControlDefaultConfigXml if it exists
        custom_control = entity_root.find('.//CustomControlDefaultConfigXml')
        if custom_control is not None:
            entity_wrapper.append(custom_control)

        # Find and copy SavedQueries if they exist
        saved_queries = entity_root.find('.//SavedQueries')
        if saved_queries is not None:
            entity_wrapper.append(saved_queries)
            print(f"  ✓ Added SavedQueries for {entity_name}")

    # Add all the other empty sections
    ET.SubElement(root, 'Roles')
    ET.SubElement(root, 'Workflows')
    ET.SubElement(root, 'FieldSecurityProfiles')
    ET.SubElement(root, 'Templates')
    ET.SubElement(root, 'EntityMaps')
    ET.SubElement(root, 'EntityRelationships')
    ET.SubElement(root, 'OrganizationSettings')
    ET.SubElement(root, 'optionsets')
    ET.SubElement(root, 'CustomControls')
    ET.SubElement(root, 'SolutionPluginAssemblies')
    ET.SubElement(root, 'EntityDataProviders')

    # Add Languages
    languages = ET.SubElement(root, 'Languages')
    lang = ET.SubElement(languages, 'Language')
    lang.text = '1033'

    # Create the tree and write to file
    tree = ET.ElementTree(root)
    ET.indent(tree, space='  ')

    # Write with XML declaration and UTF-8 BOM
    with open(customizations_path, 'wb') as f:
        f.write(b'\xef\xbb\xbf')  # UTF-8 BOM
        tree.write(f, encoding='utf-8', xml_declaration=True)

    print(f"\n✓ Merged all entities into {customizations_path}")
    print("\nNext steps:")
    print("1. Run pack-solution.ps1 to create a new solution ZIP")
    print("2. Import the new solution into Dataverse for Teams")

if __name__ == '__main__':
    merge_entities()
