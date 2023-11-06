# Installation steps for the tool

Clone the GitHub repository:

```git clone https://github.com/sa4s-serc/observability.git```

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

> This will take time to install, you can check if it is ready by going to URL `http://localhost:9200/`.
> If a JSON object is displayed, with "cluster_name": "docker-cluster", you are ready to go.

Once ready:

Elasticsearch will be exposed on API `http://localhost:9200/`

Kibana will be exposed on API `http://localhost:5601/`

Now we will import Dashboard to Elasticsearch 

Run command in a new terminal:

`curl -X POST "http://localhost:5601/api/saved_objects/_import" -H "kbn-xsrf: true" --form file=@export.ndjson`

## Setting up Frontend

To install node module's:

Run command:

`npm install`

## Setting up Virtual Environment (optional)

Using virtualenv allows you to avoid installing Python packages globally

` python3 -m venv ./venv`

 `source venv/bin/activate`
 
## Settign up Backend: Model loader, MAPE-K, Locust a load tester.

`cd NAVIE`

`python3 process_model.py`

`pip install -r requirements.txt`

## How to start the application

Run the backend for the application from the directory `observability/NAVIE`:

`python3 Node.py`

Run the React-Application from the directory `observability` :

`npm run start`


## How to use the application

Create a ZIP folder for Image's you want for object-detection

You need to have a CSV file, with an interarrival rate for all the images

Upload the ZIP and CSV files. Also select the method, and SUBMIT.



