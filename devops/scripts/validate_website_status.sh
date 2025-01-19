#!/bin/bash
set -e

http_status=$(curl -o /dev/null -s -w "%{http_code}" "$url")

if [ "$http_status" -eq 200 ]; then
    echo "Website is up and running. Returned HTTP status: $http_status"
    exit 0
else
    echo "Website is down. Returned HTTP status: $http_status"
    exit 1
fi

