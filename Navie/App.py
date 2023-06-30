import argparse
import csv
import argparse
import time
import base64
from fastapi import FastAPI, File, UploadFile
import uvicorn
from elasticsearch import Elasticsearch

# Creating a FastAPI endpoint.
app = FastAPI()
input_rate = 0
start_time = 0
total_in = 0

es = Elasticsearch()


DETECTION_URL = '/v1/object-detection'

idx = "image_data"

# Function to check if the Elasticsearch index exists
def index_exists(index):
    return es.indices.exists(index=index)


@app.post(DETECTION_URL)
async def predict(image: UploadFile = File(...)):
    global start_time
    global input_rate
    global total_in

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
    data = {
        "timestamp": x,
        "image_bytes": base64.b64encode(im_bytes).decode('utf-8'),
        "total_in": total_in
    }

    es.index(index=idx,id = total_in,  body=data)

    total_in += 1
    return


if __name__ == '__main__':
    port = 5000
    parser = argparse.ArgumentParser(description='Flask API exposing YOLOv5 model')
    parser.add_argument('--port', default=port, type=int, help='port number')
    opt = parser.parse_args()

    if not index_exists(idx):
        es.indices.create(index=idx)

    es.delete_by_query(index=idx, body={"query": {"match_all": {}}})
    es.indices.refresh(index="image_data")

    uvicorn.run(app, host='0.0.0.0', port=opt.port)
