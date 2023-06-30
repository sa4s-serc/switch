import io
from PIL import Image
import time
import torch
import psutil
import pandas as pd
import imghdr
import os
from Custom_Logger import logger
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import base64
import datetime
 

models = {}
total_processed = 0
global_start_time = 0

metric_file_name = "metrics.csv"


def call_utility(r , C):
    Rmax = 1  # Maximum acceptable response time
    Rmin = 0.1  # Minimum acceptable response time
    Cmax = 1  # Maximum acceptable confidence score
    Cmin = 0.5 # Minimum acceptable confidence score

    # Penalties for exceeding thresholds
    pdv = 1  # Penalty for exceeding the response time threshold
    pev = 1  # Penalty for exceeding the confidence score threshold

    # Weights for the response time and confidence score in the utility function
    we = 0.5 #Confidence
    wd = 0.5 #Response Time

    if r > Rmax:
        Tτ = (Rmax - r) * pdv
    elif Rmin <= r <= Rmax:
        Tτ = r
    else:  # r < Rmin
        Tτ = (r - Rmin) * pdv


    if C > Cmax:
        Eτ = (Cmax - C) * pev
    elif Cmin <= C <= Cmax:
        Eτ = C
    else:  # C < Cmin
        Eτ = (C - Cmin) * pev

    utility_values = we * Eτ + wd * Tτ
    return utility_values

def get_current():
    df = pd.read_csv('model.csv', header=None)
    array = df.to_numpy()
    # print(array[0][0])
    return array[0][0]

def save_result(results, total_processed):
    output_folder = os.path.abspath('Output')

    # Create the output folder if it doesn't exist
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)

    # Save the resultant image in the output folder
    file_name = f'Image{total_processed}'
    # output_image_path = os.path.join(output_folder, file_name)
    results.save(file_name, f"Output/{file_name}")  # or "PNG" for PNG format



def process_row(im_bytes, start_time):

    # run's the object detection on the received data

    global total_processed
    global global_start_time

    image_format = imghdr.what(None, h=im_bytes)
    if image_format is None:
        return
    current_model = get_current()

    
    if current_model in models:
        logger.data( {"User Request Time": start_time , 'model': current_model} )
        try:
            if (total_processed == 0):
                global_start_time = time.time()

            im = Image.open(io.BytesIO(im_bytes))
            current_time = time.time()
            response = models[current_model](im)


            current_cpu = psutil.cpu_percent(interval=None)
            total_processed += 1

            detection = response.pandas().xyxy[0]
            confidences = detection['confidence'].tolist()
            current_conf = sum(confidences)
            current_boxes = len(confidences)

            if (current_boxes != 0):
                avg_conf = current_conf/current_boxes

            else:
                avg_conf = 0

            t = time.time()
            current_time = t - current_time #model processsing time
            start_time = t - start_time # total time take by image to finally output
            absolute_time = t - global_start_time 

            # writes the logs in a log.csv file.
            # print("To write in log file.\n")
            f = open(metric_file_name, "a")
            ts = datetime.datetime.now().isoformat()

            utility = call_utility(start_time , avg_conf )

            f.write(
                f'{ts},{total_processed},{avg_conf},{current_model},{current_cpu},{current_boxes},{current_time},{start_time},{absolute_time},{utility}\n')
            f.close()

            # save_result(response , total_processed-1)

            return detection.to_json(orient='records')
        
        except Exception as e:
            logger.error(e)
            return {'error': str(e)}
    else:
        return {'error': f'Model {current_model} not found'}
    
es = Elasticsearch()

def start_processing():

    # checks for the current image csv file in images folder, and if it exists, it sends the image_data to process_row function

    global total_processed
    while True:
        r = 0
        image_index = "image_data"
        current_image = total_processed
        next_image = total_processed+1

        if not es.exists(index=image_index, id=current_image):
            logger.error(f"File {total_processed}.csv does not exist")
 
            if not es.exists(index=image_index, id=next_image):
                time.sleep(0.3)
                continue
            else:
                logger.error(f"Skiping a Image file, processing the next")
    
                total_processed += 1
                current_image = next_image

        logger.data({"Processing File" : total_processed  })

        response = es.get(index=image_index, id= current_image) 
        image_data = response["_source"]

        timestamp = image_data["timestamp"]
        image_bytes_encoded = image_data["image_bytes"]
        # total_in = image_data["total_in"]

        image_bytes = base64.b64decode(image_bytes_encoded)

        try:
            process_row(image_bytes , timestamp)
            es.delete(index=image_index, id=current_image)
            logger.data({"Finished Processing File" : total_processed - 1 })

        except Exception as e:
            logger.error(e)
            logger.error(f"Skiping a Image file, processing the next")
            total_processed += 1

def create_or_clear_csv(file_path):
    if os.path.exists(file_path):
        # Clear the content of the existing CSV file
        with open(file_path, 'w') as f:
            f.truncate(0)
            # print(f"Cleared content of {file_path}")


if __name__ == '__main__':

    models = {}
    for m in {'yolov5n', 'yolov5s', 'yolov5m', 'yolov5l', 'yolov5x'}:
    # for m in {'yolov5n', 'yolov5s', 'yolov5m'}:
        models[m] = torch.hub.load(
            'ultralytics/yolov5', m, force_reload=True, skip_validation=True)

    logger.info(    {'Component': "Process" , "Action": "Model's loaded ready to start processing" }  ) 

    
    create_or_clear_csv(metric_file_name)
    # start processing the images.
    time.sleep(5)
    start_processing()
