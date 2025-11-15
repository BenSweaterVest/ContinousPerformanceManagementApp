#!/usr/bin/env python3
"""
Add missing attribute metadata elements to match Microsoft's structure.

Microsoft has these elements on ALL attributes that we're missing:
- SourceType
- IsGlobalFilterEnabled, IsSortableEnabled
- CanModifyGlobalFilterSettings, CanModifyIsSortableSettings
- IsDataSourceSecret
- AutoNumberFormat (empty element)
- IsSearchable, IsFilterable, IsRetrievable, IsLocalizable

Strategy: Add these after IsLocalizable if it exists, or after IntroducedVersion
"""

from pathlib import Path
import re
import xml.etree.ElementTree as ET

def add_missing_metadata_to_attribute(attribute_xml):
    """Add missing metadata elements to an attribute definition."""

    # Elements to add if missing (in order)
    missing_elements = []

    # Check what we're missing
    if '<SourceType>' not in attribute_xml:
        missing_elements.append('      <SourceType>0</SourceType>')

    if '<IsGlobalFilterEnabled>' not in attribute_xml:
        missing_elements.append('      <IsGlobalFilterEnabled>0</IsGlobalFilterEnabled>')

    if '<IsSortableEnabled>' not in attribute_xml:
        # Determine if sortable based on field type
        if '<Type>lookup</Type>' in attribute_xml or '<Type>owner</Type>' in attribute_xml:
            missing_elements.append('      <IsSortableEnabled>0</IsSortableEnabled>')
        else:
            missing_elements.append('      <IsSortableEnabled>0</IsSortableEnabled>')

    if '<CanModifyGlobalFilterSettings>' not in attribute_xml:
        missing_elements.append('      <CanModifyGlobalFilterSettings>1</CanModifyGlobalFilterSettings>')

    if '<CanModifyIsSortableSettings>' not in attribute_xml:
        missing_elements.append('      <CanModifyIsSortableSettings>1</CanModifyIsSortableSettings>')

    if '<IsDataSourceSecret>' not in attribute_xml:
        missing_elements.append('      <IsDataSourceSecret>0</IsDataSourceSecret>')

    if '<AutoNumberFormat>' not in attribute_xml and '<AutoNumberFormat />' not in attribute_xml:
        # Use empty element format like Microsoft
        missing_elements.append('      <AutoNumberFormat></AutoNumberFormat>')

    if '<IsSearchable>' not in attribute_xml:
        # Primary name fields are searchable, others generally not
        if 'IsPrimaryName>1</IsPrimaryName' in attribute_xml or '<Type>nvarchar</Type>' in attribute_xml:
            missing_elements.append('      <IsSearchable>1</IsSearchable>')
        else:
            missing_elements.append('      <IsSearchable>0</IsSearchable>')

    if '<IsFilterable>' not in attribute_xml:
        # Primary keys and lookups are filterable
        if 'IsPrimaryId>1</IsPrimaryId' in attribute_xml or '<Type>primarykey</Type>' in attribute_xml:
            missing_elements.append('      <IsFilterable>1</IsFilterable>')
        else:
            missing_elements.append('      <IsFilterable>0</IsFilterable>')

    if '<IsRetrievable>' not in attribute_xml:
        # Most fields are retrievable except lookups to system entities (like createdby)
        if '<Type>lookup</Type>' in attribute_xml or '<Type>owner</Type>' in attribute_xml:
            missing_elements.append('      <IsRetrievable>0</IsRetrievable>')
        else:
            missing_elements.append('      <IsRetrievable>1</IsRetrievable>')

    if '<IsLocalizable>' not in attribute_xml:
        missing_elements.append('      <IsLocalizable>0</IsLocalizable>')

    if not missing_elements:
        return attribute_xml

    # Find insertion point - after CanModifyAdditionalSettings or before displaynames
    insertion_points = [
        '</CanModifyAdditionalSettings>',
        '<displaynames>',
        '<Descriptions>',
        '</attribute>'
    ]

    for insertion_point in insertion_points:
        if insertion_point in attribute_xml:
            # Insert before this point
            insert_text = '\n'.join(missing_elements) + '\n      '
            attribute_xml = attribute_xml.replace(insertion_point, insert_text + insertion_point)
            return attribute_xml

    return attribute_xml


def main():
    customizations_path = Path("solution/Other/Customizations.xml")

    if not customizations_path.exists():
        print(f"❌ Error: {customizations_path} not found")
        return 1

    print(f"📖 Reading {customizations_path}...")
    with open(customizations_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    print(f"\n🔧 Adding missing attribute metadata elements...")

    # Find all attribute blocks
    attribute_pattern = r'(<attribute PhysicalName="[^"]*">.*?</attribute>)'
    attributes = list(re.finditer(attribute_pattern, content, re.DOTALL))

    print(f"   Found {len(attributes)} attribute definitions")

    total_modified = 0

    # Process each attribute
    for i, match in enumerate(reversed(attributes), 1):  # Reverse to maintain positions
        start, end = match.span()
        old_attr = match.group(1)
        new_attr = add_missing_metadata_to_attribute(old_attr)

        if new_attr != old_attr:
            content = content[:start] + new_attr + content[end:]
            total_modified += 1

    if total_modified == 0:
        print("\n⚠️  No changes made - attributes may already have all metadata")
        return 0

    # Write back
    print(f"\n💾 Writing updated Customizations.xml...")
    with open(customizations_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Success!")
    print(f"   • Modified {total_modified} attributes")
    print(f"   • File size: {len(original_content):,} → {len(content):,} bytes ({len(content) - len(original_content):+,})")

    # Count the additions
    print(f"\n📊 Elements added:")
    elements_to_count = [
        'SourceType',
        'IsGlobalFilterEnabled',
        'IsSortableEnabled',
        'CanModifyGlobalFilterSettings',
        'CanModifyIsSortableSettings',
        'IsDataSourceSecret',
        'IsSearchable',
        'IsFilterable',
        'IsRetrievable',
        'IsLocalizable'
    ]

    for element in elements_to_count:
        count = content.count(f'<{element}>')
        print(f"   • {element:35} {count:4} occurrences")

    return 0


if __name__ == "__main__":
    exit(main())
