#!/bin/bash
# Build Linux AppImage (portable, no extraction needed)

echo "Building Acuity AppImage for Linux..."

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

# Generate icons
echo "Generating app icons..."
python3 assets/create_icon.py

# Build with PyInstaller
echo "Building executable..."
pyinstaller --clean acuity.spec

# Create AppDir structure for AppImage
echo "Creating AppImage structure..."
mkdir -p dist/Acuity.AppDir/usr/bin
mkdir -p dist/Acuity.AppDir/usr/share/applications
mkdir -p dist/Acuity.AppDir/usr/share/icons/hicolor/512x512/apps

# Copy executable
cp -r dist/Acuity/* dist/Acuity.AppDir/usr/bin/

# Create desktop entry
cat > dist/Acuity.AppDir/Acuity.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Acuity
Comment=AI-powered focus tracker
Exec=Acuity
Icon=acuity
Categories=Productivity;Utility;
Terminal=false
EOF

# Copy icon
cp assets/icon_512.png dist/Acuity.AppDir/acuity.png
cp assets/icon_512.png dist/Acuity.AppDir/usr/share/icons/hicolor/512x512/apps/acuity.png

# Create AppRun script
cat > dist/Acuity.AppDir/AppRun << 'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
export PATH="${HERE}/usr/bin:${PATH}"
cd "${HERE}/usr/bin"
exec "${HERE}/usr/bin/Acuity/Acuity" "$@"
EOF

chmod +x dist/Acuity.AppDir/AppRun

# Download appimagetool if not present
if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    echo "Downloading appimagetool..."
    wget -q https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool-x86_64.AppImage
fi

# Create AppImage
echo "Building AppImage..."
ARCH=x86_64 ./appimagetool-x86_64.AppImage dist/Acuity.AppDir dist/Acuity-x86_64.AppImage

if [ -f "dist/Acuity-x86_64.AppImage" ]; then
    echo ""
    echo "✓ AppImage created: dist/Acuity-x86_64.AppImage"
    echo ""
    echo "Users can download and run it directly:"
    echo "  chmod +x Acuity-x86_64.AppImage"
    echo "  ./Acuity-x86_64.AppImage"
    echo ""
else
    echo "AppImage creation failed. Creating tar.gz instead..."

    # Fallback to tar.gz
    mkdir -p dist/acuity-linux
    cp -r dist/Acuity dist/acuity-linux/
    cp .env.example dist/acuity-linux/
    cp README.md dist/acuity-linux/
    cp QUICKSTART.md dist/acuity-linux/

    cat > dist/acuity-linux/run.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
./Acuity/Acuity
EOF
    chmod +x dist/acuity-linux/run.sh

    cd dist
    tar -czf acuity-linux-x64.tar.gz acuity-linux/
    cd ..

    echo "✓ TAR.GZ created: dist/acuity-linux-x64.tar.gz"
fi
