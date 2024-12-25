#!/bin/bash

echo "Starting the application"

echo "Starting the database"

echo "Starting the web server"

# activate the virtual environment
cd /project
source .venv/bin/activate

cd /backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
