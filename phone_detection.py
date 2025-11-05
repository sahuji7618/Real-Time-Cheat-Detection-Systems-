import cv2
from datetime import datetime
import csv
from playsound import playsound
from ultralytics import YOLO
import threading
import os

# Load YOLO model once globally
model = YOLO("yolov8n.pt")

# Create folders and log file if needed
os.makedirs("snapshots", exist_ok=True)
if not os.path.exists("log.csv"):
    with open("log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Event"])

# Threaded alert function
def alert_actions(frame_copy):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    cv2.imwrite(f"snapshots/phone_{timestamp}.jpg", frame_copy)
    playsound('Beep.mp3')
    with open("log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), "Phone detected"])

# Core detection function for Streamlit use
def detect_phone(frame):
    frame = cv2.flip(frame, 1)
    results = model(frame)
    phone_detected = False

    for r in results:
        boxes = r.boxes.xyxy
        classes = r.boxes.cls
        for i in range(len(classes)):
            class_id = int(classes[i])
            label = model.names[class_id]
            if label == 'cell phone':
                phone_detected = True
                x1, y1, x2, y2 = map(int, boxes[i])
                cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=3)

    if phone_detected:
        threading.Thread(target=alert_actions, args=(frame.copy(),), daemon=True).start()

    return frame, phone_detected
