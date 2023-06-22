import re
import json
from datetime import datetime
from elasticsearch import Elasticsearch
import time

# Configure Elasticsearch connection
es = Elasticsearch(['localhost'])  # Replace with your Elasticsearch host

log_file_path = 'logs/Object_detection.log'  # Replace with the actual path to your log file

# Regular expression pattern to extract log data
log_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|DATA) (.*)')
index_name ="new_logs"
# Function to convert log data to JSON format
def parse_log_data(line):
    match = log_pattern.match(line)
    if match:
        timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
        log_level = match.group(2)
        log_data = match.group(3)

        try:
            log_data = json.loads(log_data.replace("'", '"'))
        except json.JSONDecodeError:
            log_data = {}

        return {
            'timestamp': timestamp,
            'log_level': log_level,
            **log_data  # Unpack log_data dictionary as separate key-value pairs
        }

    return None

# Function to clear log file
def clear_log_file():
    with open(log_file_path, 'w'):
        pass
es.delete_by_query(index=index_name, body={"query": {"match_all": {}}})
# Continuously read log file and send data to Elasticsearch
while True:
    with open(log_file_path, 'r') as file:
        lines = file.readlines()

        if lines:
            for line in lines:
                log_entry = parse_log_data(line)
                if log_entry:
                    print(log_entry)
                    es.index(index=index_name, body=log_entry)

            clear_log_file()

    # Wait for a specific duration before checking the log file again
    # Adjust the sleep duration based on your requirements
    time.sleep(5)  # Wait for 5 seconds before checking the log file again
