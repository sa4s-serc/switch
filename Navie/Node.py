from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import zipfile
import os
import subprocess
import time
from elasticsearch import Elasticsearch

es = Elasticsearch(['localhost'])
app = FastAPI()

# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

process_running = False

def run_in_new_terminal(command):
    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])

def stop_process_in_terminal(file):
    command = f"pgrep -f {file}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error is None:
        output = output.decode().strip()  # Convert bytes to string
        print("Process ID:", output)
        command = f"kill {output}"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    else:
        print("Error:", error.decode())

@app.post("/api/upload")
async def upload_files(zipFile: UploadFile = File(...), csvFile: UploadFile = File(...)):
    try:
        # Create a directory to store the uploaded files
        upload_dir = "uploads"
        shutil.rmtree(upload_dir, ignore_errors=True)
        os.makedirs(upload_dir, exist_ok=True)

        # Save the uploaded files
        zip_path = os.path.join(upload_dir, zipFile.filename)
        csv_path = os.path.join(upload_dir, csvFile.filename)

        with open(zip_path, "wb") as zf:
            shutil.copyfileobj(zipFile.file, zf)

        with open(csv_path, "wb") as cf:
            shutil.copyfileobj(csvFile.file, cf)

        # Unzip the uploaded zip file
        unzip_dir = "unzipped"
        shutil.rmtree(unzip_dir, ignore_errors=True)
        os.makedirs(unzip_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(unzip_dir)

        print("Folder unzipped successfully.")

        # Perform additional logic with the unzipped folder here

        # Move the CSV file to the unzipped folder
        csv_dest_path = os.path.join(unzip_dir, csvFile.filename)
        shutil.move(csv_path, csv_dest_path)
        print("CSV file saved successfully.")

        CSV_FILE =  "unzipped/" + csvFile.filename
        IMAGES_FOLDER = "unzipped/"+zipFile.filename
        IMAGES_FOLDER = IMAGES_FOLDER[:-4]
        print(CSV_FILE , IMAGES_FOLDER)

        run_in_new_terminal('python3 App.py')
        time.sleep(0.5)
        run_in_new_terminal(f'export CSV_FILE="{CSV_FILE}" && export IMAGES_FOLDER="{IMAGES_FOLDER}" && locust -f Request_send.py --headless  --host=http://localhost:5000/v1 --users 1 --spawn-rate 1')
        run_in_new_terminal('python3 monitor.py')
        run_in_new_terminal('python3 logs_to_es.py')
        run_in_new_terminal('python3 metrics_to_es.py')

        return {"message": "Files uploaded and processed successfully."}

    except Exception as e:
        print("Error during file upload:", str(e))
        raise HTTPException(status_code=500, detail="An error occurred during file upload.")


@app.post("/execute-python-script")
async def execute_python_script():
    global process_running
    if(process_running):
        # print("Already processed")
        return {"message": "Python script already running."}
    try:
        # print("Ready to process file")
        # Start the process.py script
        run_in_new_terminal('python3 process.py')
        # process_path = "/home/arya/Desktop/SERC/ArchML-main/NAVIE/process2.py"
        # subprocess.Popen(["python3", "-u", process_path])
        process_running = True
        return {"message": "Python script started successfully."}

    except Exception as e:
        print("Error executing Python script:", str(e))
        raise HTTPException(status_code=500, detail="An error occurred while executing the Python script.")

@app.post("/api/stopProcess")
async def stopProcess():
    try:
        stop_process_in_terminal("Request_send.py")
        stop_process_in_terminal("App.py")
        stop_process_in_terminal("monitor.py")
        stop_process_in_terminal("logs_to_es.py")
        stop_process_in_terminal("metrics_to_es.py")
        return {"message" : "Stoped succesful"}
    except Exception as e:
        print("Error stoping:", str(e))
        raise HTTPException(status_code=500, detail="An error occurred while stoping")

    
@app.post("/api/downloadData")
async def startDownload():
    try:
        run_in_new_terminal('python3 get_data.py')
        return {"message" : "Downloaded succesful"}
    except Exception as e:
        print("Error stoping:", str(e))
        raise HTTPException(status_code=500, detail="An error occurred while stoping")

    

@app.post("/api/latest_metrics_data")
async def latest_metrics_data():
    try:
        index_name = 'final_metrics_data'
        # Search for the last document created
        search_body = {
            "query": {
                "match_all": {}
            },
            "sort": [
                {
                    "timestamp": {
                        "order": "desc"
                    }
                }
            ],
            "size": 1
        }
        search_result = es.search(index=index_name, body=search_body)
        # Extract the data from the search result
        if search_result['hits']['total']['value'] > 0:
            last_document = search_result['hits']['hits'][0]['_source']
            print(last_document)
            return {'message':last_document}
            
        else:
            return {'message':'No documrnt found'}
            print("No documents found in the index")

    except Exception as e:
        print("Error stoping:", str(e))
        raise HTTPException(status_code=500, detail="An error occurred while stoping")

@app.post("/api/latest_logs")
async def latest_log_data():
    try:
        index_name = 'new_logs'
        # Search for the last document created
        search_body = {
            "query": {
                "match_all": {}
            },
            "sort": [
                {
                    "timestamp": {
                        "order": "desc"
                    }
                }
            ],
            "size": 1
        }
        search_result = es.search(index=index_name, body=search_body)
        # Extract the data from the search result
        if search_result['hits']['total']['value'] > 0:
            last_document = search_result['hits']['hits'][0]['_source']
            print(last_document)
            return {'message':last_document}
            
        else:
            return {'message':'No documrnt found'}
            print("No documents found in the index")

    except Exception as e:
        print("Error stoping:", str(e))
        raise HTTPException(status_code=500, detail="An error occurred while stoping")

        



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3001)
