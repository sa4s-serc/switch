import subprocess
from fastapi import FastAPI
import uvicorn
app = FastAPI()
script_process = []

@app.get('/start-script')
def start_script():
    global script_process
    CSV_FILE = 'unzipped/resampled_scaled_inter_arrivals.csv'
    IMAGES_FOLDER = 'unzipped/Images'
    # command= f'bash -c export CSV_FILE="{CSV_FILE}" && export IMAGES_FOLDER="{IMAGES_FOLDER}" && locust -f Request_send.py --headless  --host=http://localhost:5000/v1 --users 1 --spawn-rate 1'
    # command = 'python3 script.py'
    # command_list = command.split()
    script_process.append(subprocess.Popen(command,shell = True))
    # script_process.append(subprocess.Popen(['python3', 'script.py']))
    # script_process.append(subprocess.Popen(['python3', 'script2.py']))
    # script_process.append(subprocess.Popen(['locust', '-f', 'Request_send.py', '--host=http://localhost:5000/v1']))
    # script_process.append(subprocess.Popen(["python3 script2.py"]) )
    return {'message': 'Script started'}


@app.get('/stop-script')
def stop_script():
    global script_process
    for script in script_process:
        script.terminate()
    return {'message': 'Script stopped'}
   

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
