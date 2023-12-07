from ultralytics import YOLO
import cv2
import math
import numpy as np
import tensorflow
import pyttsx3

mtx = np.array([[600, 0, 320], [0, 600, 240], [0, 0, 1]])

def calculate_distance(box, real_object_size):
    focal_length = mtx[0, 0]
    object_width_in_pixels = box[2] - box[0]
    distance = ((real_object_size * focal_length)*(640/1440)) / object_width_in_pixels
    return distance

cap = cv2.VideoCapture(0)
cap.set(3, 2560)
cap.set(4, 1440)

mtx = np.array([[600, 0, 320], [0, 600, 240], [0, 0, 1]])


model = YOLO("ModelIRIS.pt")
'''
def calculate_distance(box, real_object_size):
    focal_length = mtx[0, 0]
    object_width_in_pixels = box[2] - box[0]
    distance = (real_object_size * focal_length) / object_width_in_pixels
    return distance
'''

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

#yolo task=detect mode=train model=yolov8m.pt data={dataset.location}/data.yaml epochs=128 imgsz=800 plots=True --save-dir 'C:\Users\anddk\OneDrive\Desktop\Code\Project - 10 Objects\arduino-1' --weights yolochange.pt

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    
    for r in results:
        boxes = r.boxes

        for box in boxes:

            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            real_object_size = 0.5
            distance = calculate_distance([x1, y1, x2, y2], real_object_size)

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 0.6
            color = (255, 255, 0)
            thickness = 2
            cv2.putText(img, f"What: {classNames[cls]}", org, font, fontScale, color, thickness)
            cv2.putText(img, f"How sure?: {confidence}", (x1, y1 + 20), font, fontScale, color, thickness)
            cv2.putText(img, f"How far?: {int(distance * 100)} centimeters", (x1, y1 + 40), font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()