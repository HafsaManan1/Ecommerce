#!/bin/bash

set -e
rsync -avzu -e "ssh -i /var/lib/jenkins/.ssh/web-dev-ecommerce-py-01.pem" --exclude 'venv/' /home/jenkins/jenkins-agent/workspace/ecommerce-dev-py-01/ ubuntu@43.205.17.209:/home/ubuntu/Ecommerce/

#sudo chown -R "$USER:$USER" "$Destination_Dir"

#cd ./devops/scripts/
#./install_dependencies.sh
#./migrate_db.sh
#./start_server.sh
#./validate_service.sh

