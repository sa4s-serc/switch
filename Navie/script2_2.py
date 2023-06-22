import os
from PIL import Image
import torch
import psutil
import time
# from models.common import DetectMultiBackend
# import cv2

def save_result(results, total_processed):
    # results.show()

    # Define the output folder path
    output_folder = os.path.abspath('Output')

    # Create the output folder if it doesn't exist
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)

    # Save the resultant image in the output folder
    file_name = f'Image{total_processed}'
    # output_image_path = os.path.join(output_folder, file_name)
    results.save(file_name, f"Ouput/{file_name}")  # or "PNG" for PNG format

    # print(f"Resultant image saved in: {output_image_path}")


RESULT_FILE = '/home/arya/Documents/log/log.csv'
with open(RESULT_FILE, 'w') as f:
    f.write('Image, Confidence, Response Time (s), CPU Consumption (%), Detection boxes\n')


model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)  # yolov5n - yolov5x6 or custom
# model = DetectMultiBackend("yolov5n.pt")
# Define the path to the folder containing the images to infer on
folder_path = '/home/arya/Desktop/SERC/yolov5/val2017'

# Get a list of all the image file names in the folder
image_file_names = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')]
i = 2
# Loop over each image file name, run inference and log the results
for image_file_name in image_file_names:
    # Load the image from file
    image_path = os.path.join(folder_path, image_file_name)
    image = Image.open(image_path)

    # Run inference on the image
    st = time.time()
    response = model(image)
    et = time.time()
    response_time = et - st

    detections = response.pandas().xyxy[0]
    confidences = detections['confidence'].tolist()
    if len(confidences) != 0:
        avg_conf = sum(confidences) / len(confidences)
    else:
        avg_conf = 0

    with open(RESULT_FILE, 'a') as f:
        f.write(
            f'{image_file_name}, {avg_conf}, {response_time:.4f}, {psutil.cpu_percent(interval=None)}, {len(confidences)}\n'
        )

    # Save the output image with bounding boxes    
    save_result(response ,i)
    i = i + 1   
    time.sleep(1)
