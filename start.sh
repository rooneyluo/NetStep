#!/bin/bash

# Function to stop the application
cleanup() {
    echo "Stopping the application"

    # Deactivate the virtual environment
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        deactivate
        echo "Virtual environment deactivated"
    else
        echo "No active virtual environment"
    fi

    # Kill uvicorn process
    if [ -n "$UVICORN_PID" ]; then
       echo "Uvicorn is running with PID(s): $UVICORN_PID"
       kill "$UVICORN_PID"
       
       # Wait for the process to terminate completely
       wait "$UVICORN_PID" 2>/dev/null  
       echo "Uvicorn process killed."
    fi
    
    echo "Cleanup complete"
    cd "$SCRIPT_DIR"
}

# trap keyboard interrupt (control-c)
trap cleanup EXIT INT TERM
echo "Trap set for EXIT, INT, and TERM signals"

# Get the script's directory
SCRIPT_DIR="$(pwd)"
echo "Script directory: $SCRIPT_DIR"

# Activate the virtual environment
echo "Activate the virtual environment"
PROJECT_DIR="$SCRIPT_DIR/project"
if [ -d "$PROJECT_DIR" ]; then
    cd "$PROJECT_DIR" || exit
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    else
        echo "Error: Virtual environment not found in $PROJECT_DIR"
        exit 1
    fi
else
    echo "Error: Project directory $PROJECT_DIR not found."
    exit 1
fi

# Start the database
DB_DIR="$SCRIPT_DIR/project/backend/database"
if [ -d "$DB_DIR" ]; then
    echo "Starting the database"
    cd "$DB_DIR" || exit
    if [ -f "create_db.py" ]; then
        python3 create_db.py
    else
        echo "Error: create_db.py not found in $DB_DIR"
        exit 1
    fi
else
    echo "Error: Database directory $DB_DIR not found."
    exit 1
fi

# Start the web server
BACKEND_DIR="$PROJECT_DIR/backend"
if [ -d "$BACKEND_DIR" ]; then
    cd "$BACKEND_DIR" || exit
    uvicorn main:app --host 0.0.0.0 --port 8000 &
    UVICORN_PID=$!
    wait $UVICORN_PID
else
    echo "Error: Backend directory $BACKEND_DIR not found."
    exit 1
fi
