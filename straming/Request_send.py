from locust import HttpUser, task
from gevent import spawn
import time
import cv2
import numpy as np
import pandas as pd
import json

class MyUser(HttpUser):
    wait_times = []
    n = 0
    image_data = []
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n = 0
        video_path = '/home/arya/Desktop/Movies/detect.mp4'
        self.image_data.append(video_path)
        f = open("status.csv", "w")
        f.write(
            f'ready_to_receive')
        f.close()

    @task
    def my_task(self):
        video_path = self.image_data[self.n]
        video = cv2.VideoCapture(video_path)
 
        if (video.isOpened() == False):
            print("Error opening the video file")
        else:
            fps = video.get(5)
            print('Frames per second : ', fps,'FPS')
            total_frames = video.get(7)
            print('Frame count : ', total_frames)

        wait_in_frames = 1/fps
        while(video.isOpened()):
            print("HI")
            ret, frame = video.read()
            if not ret:
                break
               
            df = pd.read_csv('status.csv', header=None)
            array = df.to_numpy()
            status = array[0][0]
            
            if np.any(status == "ready_to_receive"):
                # # 1080p (HD): 1920x1080
                # # 720p (HD): 1280x720
                # # 480p (SD): 854x480
                # # 360p (SD): 640x360
                # # 240p (SD): 426x240
                # frame = cv2.resize(frame, (854,480))

                frames_json = json.dumps(frame.tolist())
                spawn(self.client.post ,  "/video", data=frames_json)
                print("Out of IFIFIF")
            
            time.sleep(wait_in_frames)

        self.n += 1
        video.release()

