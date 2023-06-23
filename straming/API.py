import time
import json
import uvicorn
from fastapi import FastAPI, Request
import numpy as np
import torch
import cv2

app = FastAPI()
models = {}

# # 1080p (HD): 1920x1080
# # 720p (HD): 1280x720
# # 480p (SD): 854x480
# # 360p (SD): 640x360
# # 240p (SD): 426x240
# frame = cv2.resize(frame, (854,480))
@app.post("/v1/video")
async def predict(request: Request):
    st= time.time()
    print(f"---------------",st)

    
    f = open("status.csv", "w")
    f.write(
        f'processing')
    f.close()


    frames = await request.body()
    frame = json.loads(frames)
    
    frame_np = np.array(frame, dtype=np.uint8) 
    
    results = models['yolov5n'](frame_np)
    results = np.array(results.render())
    results = results[0]
    cv2.imshow("Sys-Video", results)

    f = open("status.csv", "w")
    f.write(
        f'ready_to_receive')
    f.close()
    et = time.time()
    print(f"et: {et}   total time: {et-st}")
    key = cv2.waitKey(1)
    # Reset the cancel_processing flag
    print("Out")
    return {"message": "Returned succ"}


if __name__ == '__main__':
    for m in {'yolov5n'}:
        models[m] = torch.hub.load(
            'ultralytics/yolov5', m, force_reload=True, skip_validation=True)
    port = 5000
    uvicorn.run(app, host='0.0.0.0', port=port)
