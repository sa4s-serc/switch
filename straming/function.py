import numpy as np
import cv2
import pafy
import torch
import time

model = torch.hub.load('ultralytics/yolov5', 'yolov5n', force_reload=True)
path = '/home/arya/Desktop/Movies/detect.mp4'
capture = cv2.VideoCapture(path)

fps = capture.get(5)
print('Frames per second : ', fps,'FPS')

frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
print('Frame count:', frame_count)

frame_pos = 0

while( frame_pos < frame_count):
    st = time.time()
    print(frame_pos)
    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
    _, frame = capture.read()

    # # 1080p (HD): 1920x1080
    # # 720p (HD): 1280x720
    # # 480p (SD): 854x480
    # # 360p (SD): 640x360
    # # 240p (SD): 426x240
    # frame = cv2.resize(frame, (854,480))

    # results = models[current_model](frame)
    results = model(frame)
    # detection = results.pandas().xyxy[0]
    # confidences = detection['confidence'].tolist()

    # s = sum(confidences)
    # conf_sum += s

    # if (len(confidences) != 0):
    #     avg_conf = sum(confidences)/len(confidences)
    #     confidence_sum += avg_conf

    # convert to numpy array and normalize to range [0,1]
    results = np.array(results.render())
    # remove the first dimension (which has only one element)
    results = results[0]

    # display the image using imshow()
    cv2.imshow(f'obj-service',results)

    key = cv2.waitKey(1)
    st = time.time() - st

    total_frames_passed = int(st*fps)
    frame_pos += total_frames_passed
    


capture.release()
cv2.destroyAllWindows()