#!/usr/bin/env python3
"""
Remove <Format>text</Format> from pm_name fields in customizations.xml
Teams Dataverse doesn't accept Format elements for nvarchar string fields
"""

import re

# Read the file
with open('solution/Other/Customizations.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove <Format>text</Format> lines (with any amount of whitespace)
# This pattern matches the line with Format and the newline
content = re.sub(r'\s*<Format>text</Format>\s*\n', '', content)

# Write back
with open('solution/Other/Customizations.xml', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed <Format>text</Format> elements from customizations.xml")

# Count remaining pm_name fields
pm_name_count = content.count('PhysicalName="pm_name"')
format_text_count = content.count('<Format>text</Format>')

print(f"pm_name fields: {pm_name_count}")
print(f"Remaining <Format>text</Format> elements: {format_text_count}")
