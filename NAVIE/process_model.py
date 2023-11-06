from ultralytics import YOLO

for m in {'yolov5nu', 'yolov5su', 'yolov5mu', 'yolov5lu', 'yolov5xu'}:
    #models[m] = torch.hub.load('ultralytics/ultralytics', m, force_reload=False, device='cpu')
    z = m + ".pt"

print("Model loaded")
 