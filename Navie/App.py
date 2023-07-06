import argparse
import csv
import argparse
import time
import base64
from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
from elasticsearch import Elasticsearch
from Custom_Logger import logger

# Creating a FastAPI endpoint.
app = FastAPI()
input_rate = 0
start_time = 0
total_in = 0

es = Elasticsearch()


DETECTION_URL = '/v1/object-detection'

#index name for image_data
idx = "image_data"

# Function to check if the Elasticsearch index exists
def index_exists(index):
    return es.indices.exists(index=index)


@app.post(DETECTION_URL)
async def predict(image: UploadFile = File(...)):
    global start_time
    global input_rate
    global total_in
    try:
        if time.time() - start_time > 1:
            # Measure the input rate of images per second
            f = open("monitor.csv", "w")
            f.write(f"{input_rate}")
            f.close()
            start_time = time.time()
            input_rate = 0

        input_rate += 1
        im_bytes = await image.read()
        x = time.time()
        #here timestamp indicates the time of receiving the request.
        #total_in is the id of the image.
        data = {
            "timestamp": x,
            "image_bytes": base64.b64encode(im_bytes).decode('utf-8'),
            "total_in": total_in
        }

        es.index(index=idx,id = total_in,  body=data)

        total_in += 1
        return {"message" : "Uploaded image_data to ES"}
    except Exception as e:
        str =f"Error uploading image_data to ES: {str(e)}"
        logger.error(str)
        print(str)
        raise HTTPException(status_code=500, detail="An error occurred while stoping")
    


if __name__ == '__main__':
    port = 5000
    parser = argparse.ArgumentParser(description='Fast API exposing YOLOv5 model')
    parser.add_argument('--port', default=port, type=int, help='port number')
    opt = parser.parse_args()

    #checking and creating index for image_data in elasticsearch, to store image
    #data. This will work as a queue.
    if not index_exists(idx):
        es.indices.create(index=idx)

    es.delete_by_query(index=idx, body={"query": {"match_all": {}}})
    es.indices.refresh(index="image_data")

    uvicorn.run(app, host='0.0.0.0', port=opt.port)
