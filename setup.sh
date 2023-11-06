#!/bin/bash
#Installing without virtual environment
# Run the curl command in a new terminal
curl -X POST 'http://localhost:5601/api/saved_objects/_import' -H 'kbn-xsrf: true' --form file=@export.ndjson

# Setting up Frontend
echo "Setting up Frontend"
echo "Installing Node modules..."
npm install

# Setting up Backend: Model loader, MAPE-K, Locust a load tester
echo "Setting up Backend"
echo "Changing directory to NAVIE..."
cd NAVIE

echo "Installing Python requirements..."
pip install -r requirements.txt

# # How to start the application
# echo "Starting the application"
# echo "Running the React-Application from the directory observability..."
# cd ../observability
# npm run start

# echo "Running the backend for the application from the directory observability/NAVIE..."
# cd NAVIE
# python3 Node.py
