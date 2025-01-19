#!/bin/bash

set -e
echo "Starting gunicorn service..."
sudo systemctl restart gunicorn

