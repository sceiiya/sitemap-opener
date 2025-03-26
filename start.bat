@echo off
REM start.bat

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

REM Run the program
echo Starting the application...
python main.py

@REM REM Deactivate when done
@REM deactivate
@REM pause