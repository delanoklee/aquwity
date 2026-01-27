#!/bin/bash
# Build script for macOS

echo "Building Acuity for macOS..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Build with PyInstaller
echo "Building macOS app bundle..."
pyinstaller --clean acuity.spec

# Create distribution folder
echo "Creating distribution package..."
mkdir -p dist/acuity-macos
cp -r dist/Acuity.app dist/acuity-macos/
cp .env.example dist/acuity-macos/
cp README.md dist/acuity-macos/
cp QUICKSTART.md dist/acuity-macos/

# Create DMG (requires create-dmg or hdiutil)
# Simple version using hdiutil
cd dist
hdiutil create -volname "Acuity" -srcfolder acuity-macos -ov -format UDZO acuity-macos-x64.dmg
cd ..

echo "Build complete! Package: dist/acuity-macos-x64.dmg"
