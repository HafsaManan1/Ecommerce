#!/bin/bash

set -e

VENV_DIR="/home/$USER/Ecommerce/.venv"

cd /home/$USER/Ecommerce/

echo "Starting deployment process..."

if [ -d "$VENV_DIR" ]; then
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
else
    echo "Virtual environment not found. Creating one..."
    python3 -m venv .venv
    if [ $? -eq 0 ]; then
        echo "Virtual environment created successfully."
        source "$VENV_DIR/bin/activate"
    else
        echo "Failed to create the virtual environment. Please check for errors."
        exit 1
    fi
fi

echo "Installing project dependencies..."
pip install -r requirements.txt
echo "Installation completed successfully."

