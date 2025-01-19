#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e
health_check="https://foodmart.osolglobal.tech/"

# Check Gunicorn status
echo "Checking Gunicorn service status..."
if sudo systemctl is-active --quiet gunicorn; then
    echo "Service Gunicorn is running successfully"
else
    echo "Gunicorn service failed to start"
    exit 1
fi

# Validate website status
echo "Validating website status..."

http_status=$(curl -o /dev/null -s -w "%{http_code}" "$health_check")

if [ "$http_status" -eq 200 ]; then
    echo "The API is healthy. Returned HTTP status: $http_status"
    exit 0
else
    echo "The API is not healthy. Returned HTTP status: $http_status"
    exit 1
fi

