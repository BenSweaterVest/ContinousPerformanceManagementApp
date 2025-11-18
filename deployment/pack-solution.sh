#!/bin/bash
# Performance Management Solution - Pack Script (Mac/Linux)
# Creates a Teams-ready solution ZIP directly from solution/ contents

set -euo pipefail

echo "======================================"
echo "Performance Management Solution Pack"
echo "======================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SOLUTION_DIR="$PROJECT_ROOT/solution"
RELEASE_DIR="$PROJECT_ROOT/releases"
export PROJECT_ROOT_PATH="$PROJECT_ROOT"

if [ ! -d "$SOLUTION_DIR" ]; then
    echo "ERROR: 'solution' folder not found!"
    exit 1
fi

echo "Project root: $PROJECT_ROOT"
echo ""

# Read version from Solution.xml
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 is required to read the solution version."
    exit 1
fi

VERSION=$(python3 <<'PY'
import xml.etree.ElementTree as ET
from pathlib import Path
path = Path("solution") / "Other" / "Solution.xml"
tree = ET.parse(path)
elem = tree.find(".//Version")
if elem is None or not elem.text:
    raise SystemExit("Could not find <Version> in Solution.xml")
print(elem.text.strip())
PY
)

OUTPUT_FILE="PerformanceManagement_v${VERSION}.zip"
OUTPUT_PATH="$RELEASE_DIR/$OUTPUT_FILE"
export OUTPUT_FILE_NAME="$OUTPUT_FILE"

mkdir -p "$RELEASE_DIR"

echo "Packaging version $VERSION → releases/$OUTPUT_FILE"
echo ""

rm -f "$OUTPUT_PATH"

# Attempt to use zip if available, otherwise fall back to python
if command -v zip >/dev/null 2>&1; then
    (
        cd "$SOLUTION_DIR"
        zip -rq "$OUTPUT_PATH" . -x "*.DS_Store" "__MACOSX/*" "*~" "Thumbs.db"
    )
else
    echo "zip command not found. Falling back to python3 compression..."
    python3 <<'PY'
import os
import zipfile
from pathlib import Path

project_root = Path(os.environ["PROJECT_ROOT_PATH"])
solution_dir = project_root / "solution"
output_path = project_root / "releases" / os.environ["OUTPUT_FILE_NAME"]
excludes = {"__MACOSX", ".DS_Store", "Thumbs.db"}

with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(solution_dir):
        rel_root = os.path.relpath(root, solution_dir)
        for name in files:
            if name in excludes:
                continue
            src = Path(root) / name
            rel = os.path.normpath(os.path.join(rel_root, name))
            if rel == ".":
                rel = name
            zf.write(src, rel)
PY
fi

if [ ! -f "$OUTPUT_PATH" ]; then
    echo "ERROR: Failed to create $OUTPUT_FILE"
    exit 1
fi

FILE_SIZE=$(du -h "$OUTPUT_PATH" | cut -f1)
SHA=$(sha256sum "$OUTPUT_PATH" | awk '{print $1}')

echo "======================================"
echo "SUCCESS: Solution packed!"
echo "======================================"
echo ""
echo "Output file : releases/$OUTPUT_FILE"
echo "File size   : $FILE_SIZE"
echo "SHA256      : $SHA"
echo ""
echo "Next steps:"
echo "  1. Upload releases/$OUTPUT_FILE to Microsoft Teams → Power Apps → Import"
echo "  2. Or run ./import-solution.sh with your environment credentials"
echo ""
