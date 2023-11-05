# Installation steps for the tool

Clone the github repository:

`git clone https://github.com/sa4s-serc/observability.git`

Run command:
`cd observability`

This project mainly uses:
> Elasticsearch and Kibana

> Python and libraries

>  React

## Setting up Elasticseach and Kibana 

Installing Elasticsearch and Kibana with Docker.

Will be using version Docker image version: 7.9.1

Start an Elasticsearch and Kibana container using Docker-compose file:

Run command:

`docker-compose up`

Once ready:

Elasticsearch will be exposed on API `http://localhost:9200/`

Kibana will be exposed on API `http://localhost:5601/`

Now we will import Dashboard to Elasticsearch 

Run command:

`curl -X POST "http://localhost:5601/api/saved_objects/_import" -H "kbn-xsrf: true" --form file=@export.ndjson`

### Setting up Frontend

To install node module's:

Run command:
`npm install`

### Settign up Backend: Model loader, MAPE-K, Locust a load tester.

> ` pip install -r requirements.txt`
