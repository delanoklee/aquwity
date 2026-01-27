@echo off
REM Build Windows installer with Inno Setup

echo Building Acuity Windows Installer...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Generate icons
echo Generating app icons...
python assets\create_icon.py

REM Build with PyInstaller
echo Building executable...
pyinstaller --clean acuity.spec

REM Check if Inno Setup is installed
set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if exist "%INNO_PATH%" (
    echo Creating installer with Inno Setup...
    "%INNO_PATH%" installer\windows_installer.iss
    echo.
    echo ✓ Installer created: dist\AcuitySetup.exe
    echo.
) else (
    echo.
    echo Inno Setup not found. Creating ZIP package instead...
    echo To create a professional installer, install Inno Setup from:
    echo https://jrsoftware.org/isdl.php
    echo.

    REM Create distribution folder
    mkdir dist\acuity-windows
    xcopy /E /I dist\Acuity dist\acuity-windows\Acuity
    copy .env.example dist\acuity-windows\
    copy README.md dist\acuity-windows\
    copy QUICKSTART.md dist\acuity-windows\

    REM Create ZIP archive
    cd dist
    powershell Compress-Archive -Path acuity-windows -DestinationPath acuity-windows-x64.zip -Force
    cd ..

    echo ✓ ZIP created: dist\acuity-windows-x64.zip
)

pause
