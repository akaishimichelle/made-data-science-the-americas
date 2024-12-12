# As a pre-requisite, 
#   1. Please make sure to be signed in to kaggle
#   2. Go to kaggle settings and create a new token (under API section). This will generate a "kaggle.json" file
#   3. Make a kaggle folder in your home directory (C:\Users\{your_username}\.kaggle).
#      You may use this command to check your home directory in command prompt: echo %USERPROFILE%
#   4. Place the "kaggle.json" file in the folder you created in step3

# The following imports will be automatically installed before running the pipeline via 'requirements.txt' file:
#  kagglehub
#  pandas 
#  requests

# Create virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

SCRIPT_DIR=$(dirname "$(realpath "$0")")

TESTS_PY="$SCRIPT_DIR/tests.py"
python3 "$TESTS_PY"
