#!/bin/bash

# Check the HTTP status code using curl
status_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")

# Check if the status code is 200
if [ "$status_code" -eq 200 ]; then
    echo "The website is up and returned status code 200."
else
    echo "The website returned status code $status_code."
fi

