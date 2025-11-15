#!/usr/bin/env python3
"""
Validate that our solution structure aligns with Microsoft's Boards solution.
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
customizations_path = Path('/home/user/ContinousPerformanceManagementApp/solution/Other/Customizations.xml')

print("="*60)
print("VALIDATION: Alignment with Microsoft Boards Solution")
print("="*60)

# Check 1: Primarykey fields should NOT have MaxLength
print("\n1. Checking primarykey fields (should NOT have MaxLength)...")
primarykey_issues = []
for entity in entities:
    entity_file = tables_path / entity / 'Entity.xml'
    with open(entity_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find primarykey attribute
    pk_pattern = r'<attribute PhysicalName="' + entity + r'id">.*?<Type>primarykey</Type>.*?</attribute>'
    pk_match = re.search(pk_pattern, content, re.DOTALL)

    if pk_match:
        pk_content = pk_match.group(0)
        if '<MaxLength>' in pk_content:
            primarykey_issues.append(entity)
            print(f"  ❌ {entity} - primarykey HAS MaxLength (should not)")
        else:
            print(f"  ✓ {entity} - primarykey OK (no MaxLength)")
    else:
        print(f"  ? {entity} - primarykey not found")

# Check 2: Custom nvarchar/memo fields should have API attributes
print("\n2. Checking custom nvarchar/memo fields (should have API attributes)...")
custom_field_issues = []
for entity in entities:
    entity_file = tables_path / entity / 'Entity.xml'
    with open(entity_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all custom nvarchar/memo fields (pm_ prefix, not primarykey, not primaryname if it's already been processed)
    custom_pattern = r'<attribute PhysicalName="(pm_\w+)">\s*<Type>(nvarchar|memo)</Type>.*?</attribute>'
    custom_matches = re.findall(custom_pattern, content, re.DOTALL)

    for match in custom_matches:
        field_name = match[0]
        field_type = match[1]

        # Get the full attribute content
        field_pattern = r'<attribute PhysicalName="' + field_name + r'">.*?</attribute>'
        field_match = re.search(field_pattern, content, re.DOTALL)

        if field_match:
            field_content = field_match.group(0)

            # Check for required API attributes
            missing_attrs = []
            required_attrs = [
                'ValidForUpdateApi',
                'ValidForReadApi',
                'ValidForCreateApi',
                'IsCustomField',
                'IsAuditEnabled',
                'IsSecured',
                'SourceType',
                'AutoNumberFormat',
                'IsSearchable',
                'IsFilterable',
                'IsRetrievable',
                'IsLocalizable'
            ]

            for attr in required_attrs:
                if attr not in field_content:
                    missing_attrs.append(attr)

            if missing_attrs:
                custom_field_issues.append(f"{entity}.{field_name}")
                print(f"  ❌ {entity}.{field_name} - Missing: {', '.join(missing_attrs[:3])}...")
            else:
                # Check for MaxLength or Length
                if field_type == 'nvarchar':
                    if 'Length>' not in field_content and 'MaxLength>' not in field_content:
                        custom_field_issues.append(f"{entity}.{field_name}")
                        print(f"  ❌ {entity}.{field_name} - Missing Length/MaxLength")
                    else:
                        print(f"  ✓ {entity}.{field_name} - OK")
                else:  # memo
                    if 'MaxLength>' not in field_content:
                        custom_field_issues.append(f"{entity}.{field_name}")
                        print(f"  ❌ {entity}.{field_name} - Missing MaxLength")
                    else:
                        print(f"  ✓ {entity}.{field_name} - OK")

# Check 3: Customizations.xml should be updated
print("\n3. Checking Customizations.xml...")
with open(customizations_path, 'r', encoding='utf-8') as f:
    customizations_content = f.read()

# Check if MaxLength is NOT in primarykey fields
pk_in_customizations_pattern = r'<attribute PhysicalName="pm_\w+id">\s*<Type>primarykey</Type>.*?</attribute>'
pk_in_customizations = re.findall(pk_in_customizations_pattern, customizations_content, re.DOTALL)

customizations_pk_issues = 0
for pk in pk_in_customizations:
    if '<MaxLength>' in pk:
        customizations_pk_issues += 1

if customizations_pk_issues > 0:
    print(f"  ❌ Found {customizations_pk_issues} primarykey fields with MaxLength in Customizations.xml")
else:
    print(f"  ✓ No primarykey fields have MaxLength in Customizations.xml")

# Check file size
file_size = customizations_path.stat().st_size
print(f"  ✓ Customizations.xml size: {file_size:,} bytes ({file_size/1024:.1f} KB)")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)

all_good = (
    len(primarykey_issues) == 0 and
    len(custom_field_issues) == 0 and
    customizations_pk_issues == 0
)

if all_good:
    print("✅ ALL CHECKS PASSED - Solution aligned with Microsoft structure!")
    print("\nReady to pack and import:")
    print("  1. Run: .\\deployment\\pack-solution.ps1")
    print("  2. Import the PerformanceManagement_1_0_0_0.zip")
else:
    print("❌ ISSUES FOUND:")
    if primarykey_issues:
        print(f"  - {len(primarykey_issues)} primarykey fields still have MaxLength")
    if custom_field_issues:
        print(f"  - {len(custom_field_issues)} custom fields missing API attributes")
    if customizations_pk_issues:
        print(f"  - {customizations_pk_issues} primarykey fields in Customizations.xml have MaxLength")

print("="*60)
