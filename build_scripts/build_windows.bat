@echo off
REM Build script for Windows

echo Building Acuity for Windows...

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

REM Build with PyInstaller
echo Building executable...
pyinstaller --clean acuity.spec

REM Create distribution folder
echo Creating distribution package...
mkdir dist\acuity-windows
xcopy /E /I dist\Acuity dist\acuity-windows\Acuity
copy .env.example dist\acuity-windows\
copy README.md dist\acuity-windows\
copy QUICKSTART.md dist\acuity-windows\

REM Create launcher batch file
echo @echo off > dist\acuity-windows\Acuity.bat
echo cd /d "%%~dp0" >> dist\acuity-windows\Acuity.bat
echo Acuity\Acuity.exe >> dist\acuity-windows\Acuity.bat

REM Create ZIP archive (requires 7-Zip or PowerShell)
cd dist
powershell Compress-Archive -Path acuity-windows -DestinationPath acuity-windows-x64.zip -Force
cd ..

echo Build complete! Package: dist\acuity-windows-x64.zip
pause
