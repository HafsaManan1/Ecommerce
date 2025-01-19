#!/bin/bash

set -e
#sudo chown -R "$USER:$USER" "$Destination_Dir"

cd /home/ubuntu/Ecommerce/devops/scripts/

./install_dependencies.sh
./start_server.sh
./validate_service.sh
sleep 5
./validate_website_status.sh
