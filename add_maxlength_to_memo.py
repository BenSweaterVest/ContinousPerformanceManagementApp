#!/usr/bin/env python3
"""
Add MaxLength to all memo fields that are missing it.
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

for entity in entities:
    entity_file = tables_path / entity / 'Entity.xml'

    with open(entity_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: Find memo type fields that don't have MaxLength
    # Look for <Type>memo</Type> followed by attributes but no MaxLength before </attribute>
    pattern = r'(<Type>memo</Type>\s+<Name>[^<]+</Name>\s+<LogicalName>[^<]+</LogicalName>\s+<RequiredLevel>[^<]+</RequiredLevel>)(\s+(?!<MaxLength>))'

    def add_maxlength(match):
        # Add MaxLength after RequiredLevel
        return match.group(1) + '\n          <MaxLength>2000</MaxLength>' + match.group(2)

    new_content, count = re.subn(pattern, add_maxlength, content)

    if count > 0:
        with open(entity_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Added MaxLength to {count} memo field(s) in {entity}")
    else:
        print(f"  - {entity} (no changes needed)")

print("\n✓ All memo fields updated")
