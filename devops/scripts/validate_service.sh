#!/bin/bash

set -e
gunicorn_status=0

if sudo systemctl is-active --quiet gunicorn; then
    echo "Service Gunicorn is running successfully"
else
    echo "Gunicorn service failed to start"
    gunicorn_status=1
fi

if [ "$gunicorn_status" -eq 1 ]; then
    echo "Gunicorn service failed to start"
    exit 1
else
    echo "Gunicorn is running successfully"
    exit 0
fi

