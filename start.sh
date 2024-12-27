#!/bin/bash

# Function to stop the application
cleanup() {
    echo "Stopping the application"
    deactivate 2>/dev/null || echo "Virtual environment not active"
    cd "$(dirname "$0")"
    exit
}

# trap keyboard interrupt (control-c)
trap cleanup EXIT INT TERM

# change to the directory of the script
cd "$(dirname "$0")"

echo "Starting the application"

echo "Starting the database"

echo "Starting the web server"

# activate the virtual environment
cd project
source venv/bin/activate

cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000


