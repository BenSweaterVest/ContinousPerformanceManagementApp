#!/bin/bash
# Performance Management Solution - Import Script (Mac/Linux)
# This script imports the Power Platform solution into a Dataverse environment

ENVIRONMENT_ID=""
ENVIRONMENT_URL=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --environment-id)
            ENVIRONMENT_ID="$2"
            shift 2
            ;;
        --environment-url)
            ENVIRONMENT_URL="$2"
            shift 2
            ;;
        *)
            if [ -z "$ENVIRONMENT_ID" ] && [ -z "$ENVIRONMENT_URL" ]; then
                ENVIRONMENT_ID="$1"
            fi
            shift
            ;;
    esac
done

echo "========================================"
echo "Performance Management Solution Import"
echo "========================================"
echo ""

# Check if PAC CLI is installed
echo "Checking for Power Platform CLI..."
if ! command -v pac &> /dev/null; then
    echo "ERROR: Power Platform CLI not found!"
    echo ""
    echo "Please install PAC CLI:"
    echo "  dotnet tool install --global Microsoft.PowerApps.CLI.Tool"
    echo ""
    exit 1
fi

echo "Found PAC CLI"
echo ""

# Navigate to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Check for solution package
PACKAGE_FILE="PerformanceManagement_1_0_0_0.zip"
if [ ! -f "$PACKAGE_FILE" ]; then
    echo "ERROR: Solution package not found: $PACKAGE_FILE"
    echo ""
    echo "Please run ./pack-solution.sh first to create the package"
    echo ""
    exit 1
fi

echo "Found solution package: $PACKAGE_FILE"
echo ""

# Check authentication
echo "Checking authentication status..."
AUTH_LIST=$(pac auth list 2>&1)
if echo "$AUTH_LIST" | grep -q "No profiles"; then
    echo "Not authenticated to any environment"
    echo ""

    if [ -z "$ENVIRONMENT_ID" ] && [ -z "$ENVIRONMENT_URL" ]; then
        echo "Please provide environment credentials:"
        echo ""
        echo "Option 1 - By Environment ID:"
        echo "  ./import-solution.sh --environment-id 'your-env-id-here'"
        echo ""
        echo "Option 2 - By Environment URL:"
        echo "  ./import-solution.sh --environment-url 'https://yourorg.crm.dynamics.com'"
        echo ""
        echo "To find your environment:"
        echo "  1. Go to admin.powerplatform.microsoft.com"
        echo "  2. Select Environments"
        echo "  3. Copy the Environment ID or URL"
        echo ""
        exit 1
    fi

    echo "Authenticating..."
    if [ -n "$ENVIRONMENT_ID" ]; then
        pac auth create --environment "$ENVIRONMENT_ID"
    else
        pac auth create --url "$ENVIRONMENT_URL"
    fi

    if [ $? -ne 0 ]; then
        echo "ERROR: Authentication failed!"
        exit 1
    fi
fi

echo "Authenticated successfully"
echo ""

# Import solution
echo "Starting solution import..."
echo "This may take several minutes..."
echo ""

pac solution import \
    --path "$PACKAGE_FILE" \
    --async \
    --force-overwrite \
    --publish-changes

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "SUCCESS: Import initiated!"
    echo "========================================"
    echo ""
    echo "The solution is being imported asynchronously."
    echo ""
    echo "To monitor progress:"
    echo "  1. Go to admin.powerplatform.microsoft.com"
    echo "  2. Select your environment"
    echo "  3. Go to Solutions"
    echo "  4. Look for 'Performance Management System'"
    echo ""
    echo "After import completes:"
    echo "  1. Configure connection references (Office 365, Dataverse)"
    echo "  2. Enable Power Automate flows"
    echo "  3. Share the Canvas app with users"
    echo "  4. Load seed data (12 evaluation questions)"
    echo ""
else
    echo ""
    echo "========================================"
    echo "ERROR: Import failed!"
    echo "========================================"
    echo ""
    echo "Please review the error messages above"
    echo ""
    exit 1
fi
