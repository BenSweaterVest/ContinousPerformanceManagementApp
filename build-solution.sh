#!/bin/bash
# Manual Solution Package Builder
# Creates a properly formatted Dataverse solution ZIP file

set -e

echo "🔨 Building Performance Management Solution Package..."

# Get version from Solution.xml
VERSION=$(grep -oP '<Version>\K[0-9.]+' solution/Other/Solution.xml)
ZIP_NAME="PerformanceManagement_${VERSION//./_}.zip"

echo "📌 Version: $VERSION"
echo "📦 Output: $ZIP_NAME"

# Clean up any previous build
rm -rf packed_solution
rm -f "$ZIP_NAME"

# Create temporary directory for packed format
echo ""
echo "📁 Creating packed solution structure..."
mkdir -p packed_solution

# Copy files to root with lowercase names (Dataverse requirement)
echo "   ✓ Copying solution.xml (lowercase)"
cp solution/Other/Solution.xml packed_solution/solution.xml

echo "   ✓ Copying customizations.xml (lowercase)"
cp solution/Other/Customizations.xml packed_solution/customizations.xml

echo "   ✓ Copying [Content_Types].xml"
cp "solution/[Content_Types].xml" "packed_solution/[Content_Types].xml"

# Copy subdirectories
if [ -d solution/CanvasApps ]; then
    echo "   ✓ Copying CanvasApps/"
    cp -r solution/CanvasApps packed_solution/
fi

if [ -d solution/Workflows ]; then
    echo "   ✓ Copying Workflows/"
    cp -r solution/Workflows packed_solution/
fi

if [ -d solution/Tables ]; then
    echo "   ✓ Copying Tables/"
    cp -r solution/Tables packed_solution/
fi

# Create ZIP
echo ""
echo "📦 Creating ZIP archive..."
cd packed_solution

# Zip all normal files
zip -r "../${ZIP_NAME}" * > /dev/null

# Add [Content_Types].xml (starts with bracket, not matched by *)
zip -u "../${ZIP_NAME}" "[Content_Types].xml" > /dev/null

cd ..

# Verify ZIP was created
if [ -f "$ZIP_NAME" ]; then
    SIZE=$(stat -c%s "$ZIP_NAME" 2>/dev/null || stat -f%z "$ZIP_NAME")
    SIZE_KB=$((SIZE / 1024))
    echo "✅ Package created: ${ZIP_NAME} (${SIZE_KB} KB)"
else
    echo "❌ ERROR: Failed to create package!"
    exit 1
fi

# Verify ZIP contents
echo ""
echo "🔍 Verifying ZIP structure..."

# Check for required files at root
if unzip -l "$ZIP_NAME" | grep -q "^ *[0-9]* *[0-9-]* [0-9:]* solution.xml$"; then
    echo "   ✓ solution.xml found at root"
else
    echo "   ❌ ERROR: solution.xml not at root"
    exit 1
fi

if unzip -l "$ZIP_NAME" | grep -q "^ *[0-9]* *[0-9-]* [0-9:]* customizations.xml$"; then
    echo "   ✓ customizations.xml found at root"
else
    echo "   ❌ ERROR: customizations.xml not at root"
    exit 1
fi

if unzip -l "$ZIP_NAME" | grep -q "^ *[0-9]* *[0-9-]* [0-9:]* \[Content_Types\].xml$"; then
    echo "   ✓ [Content_Types].xml found at root"
else
    echo "   ❌ ERROR: [Content_Types].xml not at root"
    exit 1
fi

# Show summary
echo ""
echo "📋 ZIP Contents Summary:"
unzip -l "$ZIP_NAME" | grep -E "(solution\.xml|customizations\.xml|Content_Types|CanvasApps|Workflows|Tables)" | head -15

# Cleanup
echo ""
echo "🧹 Cleaning up temporary files..."
rm -rf packed_solution

echo ""
echo "✅ Build complete!"
echo ""
echo "📥 Next steps:"
echo "   1. Import ${ZIP_NAME} into Dataverse for Teams"
echo "   2. Configure connections (Dataverse, Office 365)"
echo "   3. Turn on Cloud Flows"
echo "   4. Test the Canvas App"
echo ""
echo "📄 Expected import:"
echo "   • 9 Tables"
echo "   • 4 Cloud Flows"
echo "   • 1 Canvas App"
