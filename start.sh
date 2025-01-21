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

    echo "Cleanup complete"
    cd "$NETSTEP_DIR"
}

# trap keyboard interrupt (control-c)
trap cleanup EXIT INT TERM
echo "Trap set for EXIT, INT, and TERM signals"

# Get the script's directory
NETSTEP_DIR="$(pwd)"
echo "NetStep directory: $NETSTEP_DIR"

# Activate the virtual environment
PROJECT_DIR="$NETSTEP_DIR/project"
if [ -d "$PROJECT_DIR" ]; then
    echo "Activate the virtual environment"
    if [ -f "$PROJECT_DIR/venv/bin/activate" ]; then
        source $PROJECT_DIR/venv/bin/activate
    else
        echo "Error: Virtual environment not found in $PROJECT_DIR"
        return 1
    fi
else
    echo "Error: Project directory $PROJECT_DIR not found."
    return 1
fi

# Start the database
#DB_DIR="$NETSTEP_DIR/project/db"
#if [ -d "$DB_DIR" ]; then
#    echo "Starting the database"
#    if [ -f "$DB_DIR/init_db.py" ]; then
#        python3 $DB_DIR/init_db.py
#   else
#       echo "Error: init_db.py not found in $DB_DIR"
#       return 1
#   fi
#else
    #echo "Error: Database directory $DB_DIR not found."
    #return 1
#fi

# Start the web server
if [ -d "$PROJECT_DIR" ]; then
    echo "Starting the web server"
    if [ -f "$PROJECT_DIR/main.py" ]; then
        python3 $PROJECT_DIR/main.py
    else
        echo "Error: main.py not found in $PROJECT_DIR"
        return 1
    fi
else
    echo "Error: Project directory $PROJECT_DIR not found."
    return 1
fi
