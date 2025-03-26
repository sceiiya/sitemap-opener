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
pyinstaller --name "Sitemap Opener" --icon "app_icon.ico" --onefile main.py

REM Run the program
echo Starting the application...
"dist\Sitemap Opener.exe"