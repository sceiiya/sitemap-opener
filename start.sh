if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    # python3 -m venv venv
    python -m venv venv
fi


# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On MacOS/Linux:
# source venv/bin/activate

# Install the requirements
pip install -r requirements.txt

# Run
# python3 main.py
python main.py

# Stop and deactivate the virtual environment
# deactivate