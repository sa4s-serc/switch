# Installation steps for the tool

Clone the GitHub repository:

`git clone https://github.com/sa4s-serc/observability.git`

Run command:
`cd observability`

This project mainly uses:
> Elasticsearch and Kibana

> Python and libraries

>  React

## Setting up Elastic Search and Kibana 

Installing Elasticsearch and Kibana with Docker.

Will be using version Docker image version: 7.9.1

Start an Elasticsearch and Kibana container using a Docker-compose file:

Run command:

`docker-compose up`

Once ready:

Elasticsearch will be exposed on API `http://localhost:9200/`

Kibana will be exposed on API `http://localhost:5601/`

Now we will import Dashboard to Elasticsearch 

Run command in a new terminal:

`curl -X POST "http://localhost:5601/api/saved_objects/_import" -H "kbn-xsrf: true" --form file=@export.ndjson`

## Setting up Virtual Environment (optional)
` python3 -m venv ./venv`

 `source venv/bin/activate`

## Setting up Frontend

To install node module's:

Run command:

`npm install`

## Settign up Backend: Model loader, MAPE-K, Locust a load tester.

`cd NAVIE`

` pip install -r requirements.txt`

## How to start the application

Run the React-Application from the directory `observability` :

`npm run start`

Run the backend for the application from the directory `observability/NAVIE`:

`python3 Node.py`

## How to use the application

Create a ZIP folder for Image's you want for object-detection

You need to have a CSV file, with an interarrival rate for all the images

Upload the ZIP and CSV files. Also select the method, and SUBMIT.



