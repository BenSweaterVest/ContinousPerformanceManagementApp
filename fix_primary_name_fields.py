#!/usr/bin/env python3
"""
Fix primary name fields by updating existing pm_name fields to include PrimaryName in DisplayMask
instead of adding duplicate fields
"""

import re

print("Updating existing pm_name fields to be primary name fields...")
print()

# Read the file
with open('/home/user/ContinousPerformanceManagementApp/solution/Other/Customizations.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# Count how many pm_name fields we find
count = 0

# Find all pm_name attribute blocks and update their DisplayMask to include PrimaryName
# Pattern: find attribute blocks with Name>pm_name</Name> and update DisplayMask

# Strategy: Find each pm_name attribute and ensure it has PrimaryName in DisplayMask
pattern = r'(<attribute PhysicalName="pm_name">.*?<DisplayMask>)([^<]+)(</DisplayMask>.*?</attribute>)'

def fix_display_mask(match):
    global count
    prefix = match.group(1)
    display_mask = match.group(2)
    suffix = match.group(3)

    # Check if PrimaryName is already in the mask
    if 'PrimaryName' not in display_mask:
        # Add PrimaryName to the beginning
        new_mask = 'PrimaryName|' + display_mask
        count += 1
        print(f"✓ Updated pm_name field (was: {display_mask}, now: {new_mask})")
        return prefix + new_mask + suffix
    else:
        print(f"  pm_name already has PrimaryName")
        return match.group(0)

content = re.sub(pattern, fix_display_mask, content, flags=re.DOTALL)

# Also need to ensure pm_name fields are required
# Update RequiredLevel if it's not 'required' or 'applicationrequired'
pattern2 = r'(<attribute PhysicalName="pm_name">.*?<RequiredLevel>)([^<]+)(</RequiredLevel>.*?</attribute>)'

def fix_required_level(match):
    prefix = match.group(1)
    req_level = match.group(2)
    suffix = match.group(3)

    if req_level not in ['required', 'applicationrequired', 'systemrequired']:
        print(f"  Updated RequiredLevel from {req_level} to required")
        return prefix + 'required' + suffix
    return match.group(0)

content = re.sub(pattern2, fix_required_level, content, flags=re.DOTALL)

# Write back
print()
print("Writing updated customizations.xml...")
with open('/home/user/ContinousPerformanceManagementApp/solution/Other/Customizations.xml', 'w', encoding='utf-8') as f:
    f.write(content)

lines = len(content.split('\n'))
print(f"✓ File updated: {lines} lines")
print(f"✓ Updated {count} pm_name fields to be primary name fields")
