#!/bin/bash

set -e
#sudo chown -R "$USER:$USER" "$Destination_Dir"

cd /home/ubuntu/Ecommerce/devops/scripts/

./install_dependencies.sh
./migrate_db.sh
./start_server.sh
./validate_service.sh
