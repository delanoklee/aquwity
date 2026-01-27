#!/bin/bash
# Build script for Linux

echo "Building Acuity for Linux..."

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
echo "Building executable..."
pyinstaller --clean acuity.spec

# Create distribution folder
echo "Creating distribution package..."
mkdir -p dist/acuity-linux
cp -r dist/Acuity dist/acuity-linux/
cp .env.example dist/acuity-linux/
cp README.md dist/acuity-linux/
cp QUICKSTART.md dist/acuity-linux/

# Create launcher script
cat > dist/acuity-linux/run.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
./Acuity/Acuity
EOF

chmod +x dist/acuity-linux/run.sh

# Create archive
cd dist
tar -czf acuity-linux-x64.tar.gz acuity-linux/
cd ..

echo "Build complete! Package: dist/acuity-linux-x64.tar.gz"
