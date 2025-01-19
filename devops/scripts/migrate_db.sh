#!/bin/bash

VENV_DIR="/home/$USER/Ecommerce/venv"

cd /home/$USER/Ecommerce

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

python manage.py makemigrations

python manage.py migrate

