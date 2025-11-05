# Face_detection.py

import cv2
import mediapipe as mp
import threading      # ✅ Import threading
from playsound import playsound

# Setup Mediapipe face detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Alarm Function
def play_face_alert():
    playsound('Beep.mp3')  # You can use the same 'Beep.mp3' sound


def detect_faces(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(frame_rgb)

    face_found = False
    multiple_faces = False

    if results.detections:
        face_count = len(results.detections)
        if face_count >= 1:
            face_found = True
        if face_count > 1:
            multiple_faces = True

        # Draw boxes
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 🛎️ Trigger alarm if needed
    if not face_found or multiple_faces:
        
        threading.Thread(target=play_face_alert, daemon=True).start()

    return frame, face_found, multiple_faces
