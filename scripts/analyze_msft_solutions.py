#!/usr/bin/env python3
"""
Analyze all Microsoft Teams reference solutions to validate our structural fixes.

Checks:
1. RootComponent types in Solution.xml (Canvas Apps type 300, Workflows type 29)
2. Workflows XML structure (sibling vs nested)
3. Connection references placement
4. Customizations.xml section ordering
5. Canvas Apps structure
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

def analyze_solution_xml(path: Path) -> dict:
    """Analyze Solution.xml for RootComponents."""
    result = {
        'path': str(path),
        'root_components': defaultdict(list),
        'canvas_apps': [],
        'workflows': [],
        'entities': []
    }

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all RootComponent entries
        pattern = r'<RootComponent\s+type="(\d+)"[^>]*(?:schemaName="([^"]+)")?'
        matches = re.findall(pattern, content)

        for comp_type, schema_name in matches:
            result['root_components'][comp_type].append(schema_name if schema_name else 'unnamed')

            if comp_type == '300':
                result['canvas_apps'].append(schema_name)
            elif comp_type == '29':
                result['workflows'].append(schema_name)
            elif comp_type == '1':
                result['entities'].append(schema_name)

    except Exception as e:
        result['error'] = str(e)

    return result


def analyze_customizations_xml(path: Path) -> dict:
    """Analyze Customizations.xml structure."""
    result = {
        'path': str(path),
        'has_workflows': False,
        'workflows_nested_in_roles': False,
        'has_connectionreferences': False,
        'has_canvasapps': False,
        'section_order': [],
        'canvas_apps': []
    }

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for main sections
        sections = [
            'Entities', 'Roles', 'Workflows', 'FieldSecurityProfiles',
            'Templates', 'EntityMaps', 'EntityRelationships', 'OrganizationSettings',
            'optionsets', 'WebResources', 'CustomControls', 'SolutionPluginAssemblies',
            'connectionreferences', 'CanvasApps', 'Languages'
        ]

        for section in sections:
            if f'<{section}>' in content or f'<{section} ' in content:
                result['section_order'].append(section)

                if section == 'Workflows':
                    result['has_workflows'] = True
                elif section == 'connectionreferences':
                    result['has_connectionreferences'] = True
                elif section == 'CanvasApps':
                    result['has_canvasapps'] = True

        # Check if Workflows is nested inside Roles
        # Look for pattern: <Roles /> followed by indented <Workflows>
        roles_workflows_pattern = r'<Roles\s*/>\s+<Workflows>'
        if re.search(roles_workflows_pattern, content):
            # Check indentation to see if it's nested
            nested_pattern = r'<Roles\s*/>\n[ \t]{6,}<Workflows>'
            if re.search(nested_pattern, content):
                result['workflows_nested_in_roles'] = True

        # Find Canvas App names
        app_name_pattern = r'<CanvasApp>.*?<Name>([^<]+)</Name>'
        result['canvas_apps'] = re.findall(app_name_pattern, content, re.DOTALL)

    except Exception as e:
        result['error'] = str(e)

    return result


def main():
    """Main analysis function."""
    print("\n" + "="*80)
    print("MICROSOFT TEAMS SOLUTION STRUCTURE ANALYSIS")
    print("="*80 + "\n")

    # Find all MSFT solution directories
    ref_dir = Path(__file__).parent.parent / "ref"
    msft_dirs = sorted(ref_dir.glob("MSFT_*_managed"))

    print(f"Found {len(msft_dirs)} Microsoft reference solutions:\n")

    all_results = {}

    for solution_dir in msft_dirs:
        solution_name = solution_dir.name
        print(f"\n{'='*80}")
        print(f"📦 {solution_name}")
        print('='*80)

        # Analyze Solution.xml
        solution_xml_path = solution_dir / "solution.xml"
        if solution_xml_path.exists():
            print(f"\n📄 Solution.xml:")
            sol_result = analyze_solution_xml(solution_xml_path)

            print(f"  Root Components by Type:")
            for comp_type, names in sorted(sol_result['root_components'].items()):
                type_name = {
                    '1': 'Entity',
                    '29': 'Workflow/Process',
                    '300': 'Canvas App',
                    '9': 'OptionSet'
                }.get(comp_type, f'Type {comp_type}')
                print(f"    Type {comp_type:>3} ({type_name:20s}): {len(names):2d} components")
                if comp_type in ['300', '29']:
                    for name in names[:5]:  # Show first 5
                        print(f"      - {name}")
                    if len(names) > 5:
                        print(f"      ... and {len(names) - 5} more")

            if sol_result['canvas_apps']:
                print(f"\n  ✅ Canvas Apps declared: {len(sol_result['canvas_apps'])}")
            else:
                print(f"\n  ⚠️  No Canvas Apps declared (type 300)")

            all_results[solution_name] = {'solution': sol_result}
        else:
            print(f"  ❌ solution.xml not found")

        # Analyze Customizations.xml
        customizations_path = solution_dir / "customizations.xml"
        if customizations_path.exists():
            print(f"\n📄 Customizations.xml:")
            cust_result = analyze_customizations_xml(customizations_path)

            print(f"  Sections present: {', '.join(cust_result['section_order'])}")

            if cust_result['has_workflows']:
                if cust_result['workflows_nested_in_roles']:
                    print(f"\n  ❌ Workflows NESTED inside Roles (same issue we had!)")
                else:
                    print(f"\n  ✅ Workflows properly structured as sibling of Roles")

            if cust_result['has_connectionreferences']:
                print(f"  ⚠️  Has <connectionreferences> section (we removed this)")
            else:
                print(f"  ✅ No <connectionreferences> section")

            if cust_result['has_canvasapps']:
                print(f"  ✅ Has <CanvasApps> section with {len(cust_result['canvas_apps'])} app(s)")
                for app in cust_result['canvas_apps']:
                    print(f"      - {app}")

            all_results[solution_name]['customizations'] = cust_result
        else:
            print(f"  ❌ customizations.xml not found")

    # Summary Analysis
    print("\n" + "="*80)
    print("SUMMARY: VALIDATION OF OUR STRUCTURAL FIXES")
    print("="*80 + "\n")

    # Check RootComponent type 300 usage
    solutions_with_canvas_rootcomponent = []
    solutions_without_canvas_rootcomponent = []

    for name, data in all_results.items():
        if 'solution' in data:
            if data['solution']['canvas_apps']:
                solutions_with_canvas_rootcomponent.append(name)
            else:
                solutions_without_canvas_rootcomponent.append(name)

    print("1️⃣  RootComponent Type 300 (Canvas App):")
    print(f"   With Canvas App RootComponents: {len(solutions_with_canvas_rootcomponent)}")
    for sol in solutions_with_canvas_rootcomponent:
        canvas_count = len(all_results[sol]['solution']['canvas_apps'])
        print(f"     ✅ {sol}: {canvas_count} Canvas App(s)")

    if solutions_without_canvas_rootcomponent:
        print(f"\n   Without Canvas App RootComponents: {len(solutions_without_canvas_rootcomponent)}")
        for sol in solutions_without_canvas_rootcomponent:
            print(f"     ⚠️  {sol}")

    # Check Workflows structure
    print("\n2️⃣  Workflows XML Structure:")
    workflows_nested = []
    workflows_correct = []

    for name, data in all_results.items():
        if 'customizations' in data:
            if data['customizations']['has_workflows']:
                if data['customizations']['workflows_nested_in_roles']:
                    workflows_nested.append(name)
                else:
                    workflows_correct.append(name)

    print(f"   Properly structured (sibling): {len(workflows_correct)}")
    for sol in workflows_correct:
        print(f"     ✅ {sol}")

    if workflows_nested:
        print(f"\n   Nested incorrectly: {len(workflows_nested)}")
        for sol in workflows_nested:
            print(f"     ❌ {sol}")

    # Check connectionreferences section
    print("\n3️⃣  <connectionreferences> Section:")
    with_connrefs = []
    without_connrefs = []

    for name, data in all_results.items():
        if 'customizations' in data:
            if data['customizations']['has_connectionreferences']:
                with_connrefs.append(name)
            else:
                without_connrefs.append(name)

    print(f"   With <connectionreferences>: {len(with_connrefs)}")
    for sol in with_connrefs:
        print(f"     ⚠️  {sol}")

    print(f"\n   Without <connectionreferences>: {len(without_connrefs)}")
    for sol in without_connrefs:
        print(f"     ✅ {sol}")

    # Overall Validation
    print("\n" + "="*80)
    print("VALIDATION RESULTS")
    print("="*80 + "\n")

    print("Our Fixes:")
    print("  1. ✅ Added RootComponent type 300 for Canvas App")
    print("  2. ✅ Added RootComponent type 29 for Workflows")
    print("  3. ✅ Fixed Workflows nesting (moved to sibling of Roles)")
    print("  4. ✅ Removed <connectionreferences> section")

    print("\nMicrosoft Solutions Alignment:")
    if solutions_with_canvas_rootcomponent:
        print(f"  ✅ {len(solutions_with_canvas_rootcomponent)}/{len(all_results)} Microsoft solutions use RootComponent type 300")
    else:
        print(f"  ⚠️  No Microsoft solutions use RootComponent type 300 (might be managed-only?)")

    if workflows_correct and not workflows_nested:
        print(f"  ✅ All {len(workflows_correct)} Microsoft solutions with Workflows use sibling structure")
    elif workflows_nested:
        print(f"  ⚠️  {len(workflows_nested)} Microsoft solutions have nested Workflows (unexpected!)")

    if not with_connrefs:
        print(f"  ✅ None of the {len(all_results)} Microsoft solutions have <connectionreferences> section")
    else:
        print(f"  ⚠️  {len(with_connrefs)} Microsoft solutions have <connectionreferences> (conflicts with our removal)")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
