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

# Validate website status
echo "Validating website status..."
http_status=$(curl -o /dev/null -s -w "%{http_code}" "$url")

if [ "$http_status" -eq 200 ]; then
    echo "Website is up and running. Returned HTTP status: $http_status"
    exit 0
else
    echo "Website is down. Returned HTTP status: $http_status"
    exit 1
fi

