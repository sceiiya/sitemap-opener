@echo off
REM setup.bat

REM Check if venv exists, create it if it doesn't
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Package the app with PyInstaller
echo Packaging the app...
pyinstaller --name "Sitemap Opener" --icon "app_icon.ico" --onefile --noconsole main.py

REM Compile the installer with Inno Setup
echo Compiling the installer...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss

REM Run the program
echo Starting the application...
"dist\Sitemap Opener.exe"