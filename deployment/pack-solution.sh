#!/bin/bash
# Performance Management Solution - Pack Script (Mac/Linux)
# This script packs the Power Platform solution into a distributable ZIP file

echo "======================================"
echo "Performance Management Solution Pack"
echo "======================================"
echo ""

# Check if PAC CLI is installed
echo "Checking for Power Platform CLI..."
if ! command -v pac &> /dev/null; then
    echo "ERROR: Power Platform CLI not found!"
    echo ""
    echo "Please install PAC CLI:"
    echo "  1. Install .NET SDK: https://dotnet.microsoft.com/download"
    echo "  2. Run: dotnet tool install --global Microsoft.PowerApps.CLI.Tool"
    echo "  3. Add to PATH: export PATH=\"\$PATH:\$HOME/.dotnet/tools\""
    echo ""
    exit 1
fi

PAC_VERSION=$(pac --version 2>&1)
echo "Found PAC CLI: $PAC_VERSION"
echo ""

# Navigate to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "Project root: $PROJECT_ROOT"
echo ""

# Verify solution folder exists
if [ ! -d "solution" ]; then
    echo "ERROR: 'solution' folder not found!"
    exit 1
fi

# Pack the solution
echo "Packing solution..."
echo ""

OUTPUT_FILE="PerformanceManagement_1_0_0_0.zip"
OUTPUT_PATH="$PROJECT_ROOT/$OUTPUT_FILE"

# Remove existing zip if present
if [ -f "$OUTPUT_PATH" ]; then
    echo "Removing existing package..."
    rm -f "$OUTPUT_PATH"
fi

# Execute pack command
pac solution pack \
    --zipfile "$OUTPUT_FILE" \
    --folder "./solution" \
    --packagetype Unmanaged \
    --errorlevel Verbose

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "SUCCESS: Solution packed!"
    echo "======================================"
    echo ""
    echo "Output file: $OUTPUT_FILE"
    echo "Location: $PROJECT_ROOT"
    echo ""

    if [ -f "$OUTPUT_PATH" ]; then
        FILE_SIZE=$(du -h "$OUTPUT_PATH" | cut -f1)
        echo "File size: $FILE_SIZE"
    fi

    echo ""
    echo "Next steps:"
    echo "  1. Review the package"
    echo "  2. Run ./import-solution.sh to deploy"
    echo ""
else
    echo ""
    echo "======================================"
    echo "ERROR: Solution pack failed!"
    echo "======================================"
    echo ""
    echo "Please review the error messages above and:"
    echo "  - Check all XML files are well-formed"
    echo "  - Verify solution structure"
    echo "  - Ensure all required files exist"
    echo ""
    exit 1
fi
