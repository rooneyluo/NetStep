#!/bin/bash

# Function to stop the application
cleanup() {
    echo "Stopping the application"
    deactivate 2>/dev/null || echo "Virtual environment not active"
    cd "$SCRIPT_DIR" || exit
    exit
}

# trap keyboard interrupt (control-c)
trap cleanup EXIT INT TERM

# Get the script's directory
SCRIPT_DIR="$(pwd)"
echo "Script directory: $SCRIPT_DIR"


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

# Start the application
echo "Starting the application"
PROJECT_DIR="$SCRIPT_DIR/project"
if [ -d "$PROJECT_DIR" ]; then
    cd "$PROJECT_DIR" || exit
    # Activate the virtual environment
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

# Start the web server
BACKEND_DIR="$PROJECT_DIR/backend"
if [ -d "$BACKEND_DIR" ]; then
    cd "$BACKEND_DIR" || exit
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
else
    echo "Error: Backend directory $BACKEND_DIR not found."
    exit 1
fi
