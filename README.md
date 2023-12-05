# An Exampler for observing to analyze and observe the self-adaptive model switch in run-time.

Description from paper:

This documentation provides a comprehensive guide to set up and observe the self-adaptive model switching in runtime using the Observability Framework.

## Getting started

The system comprises distinct components, including a frontend written in React, a backend powered by FAST API in Python, and Elasticsearch serving as the database. Will be using YOLOv5 as object detection model .



<details>
<summary><b>Frontend</b></summary>

- **Technology Stack:** React
- **Startup Command:** `npm run start`
- **Port:** 3000
- **Access:** The web application is accessible at http://localhost:3000.
  
</details>

<details>
<summary><b>Backend</b></summary>

- **Technology Stack:** FAST API, Python
- **Startup Command:** `python3 Node.py`
- **Port:** 3001

</details>

<details>
<summary><b>Database</b></summary>

- **Technology:** Elasticsearch and Kibana
- **Data Storage:**
  1. Image data encoded from the input image.
  2. Metrics obtained from object detection, including confidence scores and detection boxes.
  3. System logs.

</details>

#### Requirment's:

- Install [Docker Engine](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) as standalone binaries.
- Minimum free space of 7 GB.
- The system is designed for Linux environments. If you do not have access to a Linux system, you can either utilize a virtual Linux machine or employ a Docker image of a Linux environment.
- If using virtual enviorment for set-up, pre install virtualenv.
  
## Installation

Clone the GitHub repository:

```bash
git clone https://github.com/sa4s-serc/observability.git
```

```bash
cd observability
```


## Setting up Elastic Search and Kibana 
Start the docker engine on your system.

Start Elasticsearch and Kibana containers using Docker Compose with image version 7.9.1:


```bash
docker-compose up
```

> Wait until ready, this may take time to install depending on the internet connection.
> You can check if it's ready by accessing Elasticsearch at http://localhost:9200/, and Kibana at http://localhost:5601/.

> Use a different terminal for the rest of the steps.

## Setting up Virtual Environment (optional)

Using virtualenv allows you to avoid installing Python packages globally

```bash
python3 -m venv ./venv

source venv/bin/activate
```
## Installation (only any one is requied)

<details>
<summary><b>Installation using setup.sh</b></summary>


 ```bash
chmod +x setup.sh
./setup.sh
```
</details>

<details>
<summary><b>Manual Installation</b></summary>
 
### Importing Dashboard


```bash
curl -X POST "http://localhost:5601/api/saved_objects/_import" -H "kbn-xsrf: true" --form file=@export.ndjson
```
 
### Setting up Frontend

To install node module's:

```bash
npm install
```


### Setting up Backend: Model loader, MAPE-K, Locust a load tester.


```bash
cd NAVIE

pip install -r requirements.txt

python3 process_model.py

```
</details>

## Run the application

Ensure `docker-compose.yml` is running:

If not running, run following coomand from directory `observability`
```bash
docker-compose up
```

Run the backend for the application from the directory `observability/NAVIE`:

```
python3 Node.py
```

Run the React-Application from the directory `observability` :

```
npm run start
```


## Using the Application

1. Create a folder named `Images` containing all input images.
2. Zip the `Images` folder and upload it.
3. Create a `.csv` file with inter-arrival rates for images and upload it.
4. Assign an `ID` to your experiment.
5. Choose an approach for running the experiment:
    - 4 self-adaptive approaches.
      - `NAIVE` and `AdaMLs` are different types of provided adaptation techniques.
      - `Write your own` modifies the NAIVE algorithm according to user input values.
      - `Write Your Own MAPE-K` is described below.
    - 5 single model approaches.

6. Click `Upload`.
7. Stop the process or when all images are processed, click `Stop Process`.
8. Download data for the experiment.
9. You can stat new experiment by clicking `New Process`
  
<details>
<summary><b>Write your own MAPE-K Guidelines</b></summary>


---

To effectively implement and utilize the MAPE-K framework, follow these steps:

**Upload the Following Files:**

   - **`monitor.py`:**
     - Description: This file monitors the relevant metrics for adaptation.
     - Guidelines: Refer to the `AdaMLs/monitor_ada.py` file for examples on extracting different metrics.
     - Implementation: Define a planner object and pass the extracted metrics to it.

   - **`planner.py`:**
     - Description: This code is responsible for determining the necessity of adaptation.
     - Implementation: Develop logic within this file to plan and decide whether adaptation is required.

   - **`Analyzer.py`:**
     - Description: This code determines the result of the adaptation process.
     - Implementation: Include logic to determine the adaptation step.

   - **`Execute.py`:**
     - Description: Executes the model switch.
     - Guidelines: Refer to the `AdaMLs/Execute.py` file for insights on how to switch models.
     - Implementation: Integrate the necessary logic to perform the model switch.

   - **`Knowledge.zip`:**
     - Description: A zip file containing all the knowledge files required by the MAPE-K framework for the successful generation and execution of adaptations.

**Folder Structure:**

   - Your code filees are saved in a folder structure: `NAIVE/external_MAPE_K_<id>`.
   - You have the flexibility to make direct changes to any file within this specified directory.

**Note:**

Ensure that the code files adhere to the specified guidelines for seamless integration with the MAPE-K framework.

</details>

## Using the final result's 
If you have downloaded the data for an experiment, the metric's data is stored in a CSV file: `Observability/Exported_metrics/exported-data-metrics_{id}` and the logs for the experiment are stored in a JSON file: `Observability/Exported_logs/exported-data-logs_{id}`.
 
