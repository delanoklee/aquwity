# Acuity Deployment Guide

This guide explains how to build Acuity for distribution and deploy the website so end users can download it with one click.

## Overview

The deployment process has two parts:
1. **Build executables** for Windows, macOS, and Linux
2. **Deploy the website** with download links

## Part 1: Building Executables

### Prerequisites

- Python 3.8+
- Virtual environment
- Platform-specific build tools:
  - **Windows**: PowerShell (for creating ZIP)
  - **macOS**: Xcode Command Line Tools (for creating DMG)
  - **Linux**: tar (usually pre-installed)

### Building on Each Platform

#### On Windows

```bash
cd /home/del/codingprojects/acuity/mvp
build_scripts\build_windows.bat
```

Output: `dist/acuity-windows-x64.zip`

#### On macOS

```bash
cd /home/del/codingprojects/acuity/mvp
./build_scripts/build_mac.sh
```

Output: `dist/acuity-macos-x64.dmg`

#### On Linux

```bash
cd /home/del/codingprojects/acuity/mvp
./build_scripts/build_linux.sh
```

Output: `dist/acuity-linux-x64.tar.gz`

### What the Build Process Does

1. Creates/activates virtual environment
2. Installs all dependencies
3. Runs PyInstaller to create standalone executable
4. Packages the executable with README and .env.example
5. Creates platform-specific archive (ZIP, DMG, or TAR.GZ)

### Cross-Platform Building

**Note**: Each build script must run on its target platform. You cannot build a Windows executable on macOS, etc.

To build for all platforms, you need:
- A Windows machine or VM
- A macOS machine or VM
- A Linux machine or VM

**Alternative**: Use GitHub Actions for automated cross-platform builds (see below).

## Part 2: Hosting the Downloads

You have several options for hosting the executable files:

### Option 1: GitHub Releases (Recommended - Free)

1. **Create a GitHub repository**:
   ```bash
   cd /home/del/codingprojects/acuity/mvp
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/acuity.git
   git push -u origin main
   ```

2. **Create a release**:
   - Go to your repo on GitHub
   - Click "Releases" → "Create a new release"
   - Tag version: `v1.0.0`
   - Release title: `Acuity v1.0.0`
   - Upload the three files:
     - `acuity-windows-x64.zip`
     - `acuity-macos-x64.dmg`
     - `acuity-linux-x64.tar.gz`
   - Publish release

3. **Update website URLs**:
   Edit `website/script.js` and update the URLs:
   ```javascript
   const DOWNLOAD_URLS = {
       windows: 'https://github.com/yourusername/acuity/releases/latest/download/acuity-windows-x64.zip',
       mac: 'https://github.com/yourusername/acuity/releases/latest/download/acuity-macos-x64.dmg',
       linux: 'https://github.com/yourusername/acuity/releases/latest/download/acuity-linux-x64.tar.gz'
   };
   ```

### Option 2: Cloud Storage (Google Drive, Dropbox, etc.)

1. Upload the files to your cloud storage
2. Create public download links
3. Update `website/script.js` with the links

**Note**: Some services (like Google Drive) don't provide direct download links. GitHub Releases is easier.

### Option 3: Your Own Server

1. Upload files to your server
2. Make them accessible at URLs like:
   - `https://yoursite.com/downloads/acuity-windows-x64.zip`
3. Update `website/script.js` with these URLs

## Part 3: Deploying the Website

The website is a simple static site (HTML/CSS/JS) that can be hosted anywhere.

### Option 1: GitHub Pages (Free)

1. **Push website to GitHub**:
   ```bash
   cd /home/del/codingprojects/acuity/mvp
   # Make sure you've updated script.js with real download URLs
   git add website/
   git commit -m "Add website"
   git push
   ```

2. **Enable GitHub Pages**:
   - Go to your repo settings
   - Scroll to "Pages"
   - Source: Deploy from a branch
   - Branch: main
   - Folder: `/website`
   - Save

3. **Access your site**:
   - URL: `https://yourusername.github.io/acuity/`
   - Wait a few minutes for deployment

### Option 2: Netlify (Free)

1. **Sign up at netlify.com**
2. **Deploy**:
   - Drag and drop the `website` folder into Netlify
   - Or connect your GitHub repo
3. **Custom domain** (optional):
   - Add a custom domain in settings
   - Example: `acuity.yourdomain.com`

### Option 3: Vercel (Free)

1. **Sign up at vercel.com**
2. **Import project**:
   - Connect your GitHub repo
   - Set root directory to `website`
   - Deploy
3. **Custom domain** (optional)

### Option 4: Your Own Server

Upload the `website` folder to your web server:

```bash
scp -r website/* user@yourserver.com:/var/www/acuity/
```

## Automated Builds with GitHub Actions

To automatically build for all platforms when you push code:

1. Create `.github/workflows/build.yml`:

```yaml
name: Build Acuity

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pyinstaller --clean acuity.spec
      - run: Compress-Archive -Path dist/Acuity -DestinationPath acuity-windows-x64.zip
      - uses: actions/upload-artifact@v3
        with:
          name: windows
          path: acuity-windows-x64.zip

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pyinstaller --clean acuity.spec
      - run: hdiutil create -volname "Acuity" -srcfolder dist/Acuity.app -ov -format UDZO acuity-macos-x64.dmg
      - uses: actions/upload-artifact@v3
        with:
          name: macos
          path: acuity-macos-x64.dmg

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: sudo apt-get install -y python3-tk
      - run: pip install -r requirements.txt
      - run: pyinstaller --clean acuity.spec
      - run: tar -czf acuity-linux-x64.tar.gz -C dist Acuity
      - uses: actions/upload-artifact@v3
        with:
          name: linux
          path: acuity-linux-x64.tar.gz

  release:
    needs: [build-windows, build-macos, build-linux]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v3
      - uses: softprops/action-gh-release@v1
        with:
          files: |
            windows/acuity-windows-x64.zip
            macos/acuity-macos-x64.dmg
            linux/acuity-linux-x64.tar.gz
```

2. Create a git tag and push:
```bash
git tag v1.0.0
git push origin v1.0.0
```

3. GitHub Actions will automatically build for all platforms and create a release!

## Quick Start Deployment Checklist

- [ ] Build executables on each platform (or use GitHub Actions)
- [ ] Create GitHub repo and push code
- [ ] Create GitHub Release and upload executables
- [ ] Update `website/script.js` with real download URLs
- [ ] Deploy website to GitHub Pages/Netlify/Vercel
- [ ] Test downloads from website on each platform
- [ ] Update GitHub repo URL in website footer

## Testing Downloads

After deployment, test each download:

1. Visit your website from different browsers
2. Verify OS detection works correctly
3. Click download button for each platform
4. Extract and run the executable
5. Verify setup wizard appears
6. Complete setup with a test API key
7. Ensure app launches successfully

## Updating Releases

When you make changes:

1. Build new executables
2. Create a new GitHub release (e.g., v1.0.1)
3. Upload new files
4. Website automatically uses "latest" release URL

## Cost

**Free hosting options**:
- GitHub Releases: Free (100 GB storage)
- GitHub Pages: Free (1 GB recommended)
- Netlify: Free tier (100 GB/month bandwidth)
- Vercel: Free tier (100 GB/month bandwidth)

**Paid options** (if you need more):
- Custom domain: ~$12/year
- Cloud storage: Varies
- Dedicated server: $5-50/month

## Troubleshooting

### Build fails on Windows
- Make sure you have Python installed
- Run as Administrator if permission issues

### Build fails on macOS
- Install Xcode Command Line Tools: `xcode-select --install`
- Make sure script is executable: `chmod +x build_scripts/build_mac.sh`

### Build fails on Linux
- Install tkinter: `sudo apt-get install python3-tk`
- Install build essentials: `sudo apt-get install build-essential`

### Website shows "Download not available"
- Update the URLs in `website/script.js`
- Make sure you've pushed the changes

### Download fails with 404
- Check that GitHub release is published (not draft)
- Verify filenames match exactly in script.js

## Support

For issues:
- Check the build output for errors
- Verify all dependencies are installed
- Test on the target platform
- Open an issue on GitHub if needed
