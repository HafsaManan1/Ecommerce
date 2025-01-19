#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check Gunicorn status
echo "Checking Gunicorn service status..."
if sudo systemctl is-active --quiet gunicorn; then
    echo "Service Gunicorn is running successfully"
else
    echo "Gunicorn service failed to start"
    exit 1
fi


