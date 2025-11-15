#!/usr/bin/env python3
"""
Fix critical solution structure issues identified from analysis of Microsoft reference solutions.

Issues addressed:
1. Fix Workflows XML nesting - move from inside <Roles/> to sibling level
2. Add missing RootComponents to Solution.xml (Canvas App type 300, Workflows type 29)
3. Remove invalid <connectionreferences> section from Customizations.xml

Based on:
- SOLUTION_STRUCTURE_ANALYSIS.md
- CRITICAL_FINDINGS_FROM_COMPASS.md
- Microsoft Boards solution comparison
"""

import re
from pathlib import Path

def fix_workflows_nesting(content: str) -> tuple[str, bool]:
    """
    Fix Workflows section nesting issue.

    Current (WRONG):
        <Roles />
          <Workflows>

    Should be (siblings):
        <Roles />
        <Workflows>

    Returns:
        tuple: (fixed_content, was_fixed)
    """
    # Pattern to find Roles followed by indented Workflows
    pattern = r'(<Roles\s*/>\n)([ \t]+)(<Workflows>)'

    matches = re.findall(pattern, content)
    if not matches:
        print("  ℹ️  Workflows nesting appears correct (not found nested under Roles)")
        return content, False

    # Fix: remove extra indentation from Workflows
    # The Workflows tag should have same indentation as Roles (4 spaces)
    fixed_content = re.sub(
        pattern,
        r'\1    \3',  # 4 spaces for proper indentation
        content
    )

    print(f"  ✓ Fixed Workflows nesting (moved to sibling level)")
    return fixed_content, True


def remove_connectionreferences_section(content: str) -> tuple[str, bool]:
    """
    Remove <connectionreferences> section from Customizations.xml.

    This section is not in the official schema documentation and may be causing
    validation issues. Connection references are already embedded as JSON in
    the Canvas App definition.

    Returns:
        tuple: (fixed_content, was_removed)
    """
    # Pattern to find entire connectionreferences section
    pattern = r'[ \t]*<connectionreferences>.*?</connectionreferences>\s*\n'

    matches = re.findall(pattern, content, re.DOTALL)
    if not matches:
        print("  ℹ️  No connectionreferences section found")
        return content, False

    # Remove the section
    fixed_content = re.sub(pattern, '', content, flags=re.DOTALL)

    print(f"  ✓ Removed <connectionreferences> section (not in official schema)")
    return fixed_content, True


def add_missing_root_components(content: str) -> tuple[str, int]:
    """
    Add missing RootComponents to Solution.xml.

    Need to add:
    - Type 300 for Canvas App: pm_performancemanagement_12345
    - Type 29 for Workflows: WeeklyEvaluationReminder, QuarterlySelfEvalReminder,
      OneOnOneMeetingNotification, AdHocSelfEvalRequest

    Returns:
        tuple: (fixed_content, count_added)
    """
    # Find the RootComponents section
    root_components_pattern = r'(<RootComponents>)(.*?)(</RootComponents>)'
    match = re.search(root_components_pattern, content, re.DOTALL)

    if not match:
        print("  ❌ ERROR: Could not find <RootComponents> section")
        return content, 0

    existing_components = match.group(2)

    # Define the components we need to add
    components_to_add = [
        {
            'type': '300',
            'schemaName': 'pm_performancemanagement_12345',
            'behavior': '0',
            'description': 'Canvas App'
        },
        {
            'type': '29',
            'schemaName': 'WeeklyEvaluationReminder',
            'behavior': '0',
            'description': 'Workflow'
        },
        {
            'type': '29',
            'schemaName': 'QuarterlySelfEvalReminder',
            'behavior': '0',
            'description': 'Workflow'
        },
        {
            'type': '29',
            'schemaName': 'OneOnOneMeetingNotification',
            'behavior': '0',
            'description': 'Workflow'
        },
        {
            'type': '29',
            'schemaName': 'AdHocSelfEvalRequest',
            'behavior': '0',
            'description': 'Workflow'
        }
    ]

    # Check which components are already present
    components_added = []
    for component in components_to_add:
        schema_name = component['schemaName']
        comp_type = component['type']

        # Check if this component already exists
        existing_pattern = rf'schemaName="{schema_name}"'
        if re.search(existing_pattern, existing_components):
            print(f"  ℹ️  Component already exists: {schema_name} (type {comp_type})")
            continue

        components_added.append(component)

    if not components_added:
        print("  ℹ️  All required RootComponents already present")
        return content, 0

    # Build new RootComponent entries
    new_entries = []
    for component in components_added:
        entry = f'''      <RootComponent type="{component['type']}" schemaName="{component['schemaName']}" behavior="{component['behavior']}" />'''
        new_entries.append(entry)
        print(f"  ✓ Adding RootComponent: {component['schemaName']} (type {component['type']} - {component['description']})")

    # Insert new entries at the end of existing components (before closing tag)
    # Find the last RootComponent entry to maintain proper formatting
    last_component_match = re.search(r'(.*<RootComponent[^>]+/>)', existing_components, re.DOTALL)
    if last_component_match:
        insert_point = last_component_match.end()
        new_components = (
            existing_components[:insert_point] +
            '\n' + '\n'.join(new_entries) +
            existing_components[insert_point:]
        )
    else:
        # No existing components, just add them
        new_components = '\n' + '\n'.join(new_entries) + '\n    '

    # Replace the RootComponents section
    fixed_content = content.replace(
        match.group(0),
        match.group(1) + new_components + match.group(3)
    )

    return fixed_content, len(components_added)


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("FIXING SOLUTION STRUCTURE ISSUES")
    print("="*80 + "\n")

    # Paths
    solution_dir = Path(__file__).parent.parent / "solution"
    customizations_path = solution_dir / "Other" / "Customizations.xml"
    solution_xml_path = solution_dir / "Other" / "Solution.xml"

    # Track changes
    total_changes = 0

    # ========================================================================
    # 1. Fix Customizations.xml
    # ========================================================================
    print("📝 Fixing Customizations.xml...")

    if not customizations_path.exists():
        print(f"  ❌ ERROR: File not found: {customizations_path}")
        return

    print(f"  📂 Reading: {customizations_path}")
    with open(customizations_path, 'r', encoding='utf-8') as f:
        customizations_content = f.read()

    original_size = len(customizations_content)
    print(f"  📊 Original size: {original_size:,} bytes")

    # Fix 1: Workflows nesting
    print("\n  🔧 Fixing Workflows nesting...")
    customizations_content, workflows_fixed = fix_workflows_nesting(customizations_content)
    if workflows_fixed:
        total_changes += 1

    # Fix 2: Remove connectionreferences section
    print("\n  🔧 Removing invalid connectionreferences section...")
    customizations_content, connrefs_removed = remove_connectionreferences_section(customizations_content)
    if connrefs_removed:
        total_changes += 1

    # Write back Customizations.xml if changes were made
    if workflows_fixed or connrefs_removed:
        print(f"\n  💾 Writing updated Customizations.xml...")
        with open(customizations_path, 'w', encoding='utf-8') as f:
            f.write(customizations_content)

        new_size = len(customizations_content)
        size_diff = new_size - original_size
        print(f"  ✓ Updated size: {new_size:,} bytes ({size_diff:+,} bytes)")
    else:
        print("\n  ℹ️  No changes needed for Customizations.xml")

    # ========================================================================
    # 2. Fix Solution.xml
    # ========================================================================
    print("\n" + "="*80)
    print("📝 Fixing Solution.xml...")

    if not solution_xml_path.exists():
        print(f"  ❌ ERROR: File not found: {solution_xml_path}")
        return

    print(f"  📂 Reading: {solution_xml_path}")
    with open(solution_xml_path, 'r', encoding='utf-8') as f:
        solution_content = f.read()

    original_size = len(solution_content)
    print(f"  📊 Original size: {original_size:,} bytes")

    # Fix 3: Add missing RootComponents
    print("\n  🔧 Adding missing RootComponents...")
    solution_content, components_added = add_missing_root_components(solution_content)
    if components_added > 0:
        total_changes += components_added

    # Write back Solution.xml if changes were made
    if components_added > 0:
        print(f"\n  💾 Writing updated Solution.xml...")
        with open(solution_xml_path, 'w', encoding='utf-8') as f:
            f.write(solution_content)

        new_size = len(solution_content)
        size_diff = new_size - original_size
        print(f"  ✓ Updated size: {new_size:,} bytes ({size_diff:+,} bytes)")
    else:
        print("\n  ℹ️  No changes needed for Solution.xml")

    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\n✅ Total structural fixes applied: {total_changes}")

    if total_changes > 0:
        print("\n📋 Changes made:")
        if workflows_fixed:
            print("  • Fixed Workflows XML nesting (moved to sibling of Roles)")
        if connrefs_removed:
            print("  • Removed invalid <connectionreferences> section")
        if components_added > 0:
            print(f"  • Added {components_added} missing RootComponents to Solution.xml")

        print("\n⚠️  NEXT STEPS:")
        print("  1. Review changes in git diff")
        print("  2. Run: python scripts/repack_solution.py")
        print("  3. Test import into Teams environment")
    else:
        print("\nℹ️  No structural issues found - solution structure appears correct!")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
