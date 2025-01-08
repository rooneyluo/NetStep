#!/bin/bash

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
    cd "$SCRIPT_DIR"
}

# trap keyboard interrupt (control-c)
trap cleanup EXIT INT TERM
echo "Trap set for EXIT, INT, and TERM signals"

# Get the script's directory
SCRIPT_DIR="$(pwd)"
echo "Script directory: $SCRIPT_DIR"

# Activate the virtual environment
echo "Activating the virtual environment"
PROJECT_DIR="$SCRIPT_DIR/project"
if [ -d "$PROJECT_DIR" ]; then
    cd "$PROJECT_DIR" || exit
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo "Virtual environment activated"
    else
        echo "Error: Virtual environment not found in $PROJECT_DIR"
        exit 1
    fi
else
    echo "Error: Project directory $PROJECT_DIR not found."
    exit 1
fi

BACKEND_DIR="$PROJECT_DIR/backend"
cd "$BACKEND_DIR" || exit

# Set PYTHONPATH to include the backend directory
export PYTHONPATH="$BACKEND_DIR"

# Run the tests
echo "Running the tests"
pytest

# Explicitly call cleanup to ensure it runs
cleanup