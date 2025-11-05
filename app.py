# app.py

import streamlit as st
import cv2
from phone_detection import detect_phone
from Face_detection import detect_faces
import time

# Streamlit Config - Must be first
st.set_page_config(page_title="AI Cheat Detection", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=AI+Cheat+Detection", width=150)
    mode = st.radio("Choose Mode", ["Idle", "Start Detection"])
    st.markdown("---")

# Custom CSS
st.markdown("""
    <style>   
    .stApp {background-color: #111827; color: white; font-family: 'Poppins', sans-serif;}
    .card {background-color: #1f2937; border-radius: 20px; padding: 30px; margin-bottom: 20px; box-shadow: 0px 4px 20px rgba(0,0,0,0.3);}
    </style>
""", unsafe_allow_html=True)

# Main Page
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title("🛡️ AI Cheat Detection System")
st.markdown("</div>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    FRAME_WINDOW = st.empty()

with col2:
    faces_placeholder = st.empty()
    phone_placeholder = st.empty()
    multiple_faces_placeholder = st.empty()
    suspicion_placeholder = st.empty()

alert_log = st.empty()

# Camera Setup
def setup_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Failed to access webcam.")
        return None
    return cap

# Initialize camera if not already
if "cap" not in st.session_state:
    st.session_state.cap = None

# Live Detection
if mode == "Start Detection":
    if st.session_state.cap is None:
        with st.spinner("Starting camera..."):
            st.session_state.cap = setup_camera()

    cap = st.session_state.cap

    if cap:
        stop_button = st.button("Stop Detection")

        while cap.isOpened() and not stop_button:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to grab frame from webcam.")
                break

            frame, phone_found = detect_phone(frame)
            frame, face_found, multiple_faces = detect_faces(frame)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(rgb, channels="RGB")

            # Update Metrics
            faces_placeholder.metric("Faces Detected", "✅" if face_found else "❌")
            phone_placeholder.metric("Phone Detected", "✅" if phone_found else "❌")
            multiple_faces_placeholder.metric("Multiple Faces", "✅" if multiple_faces else "❌")

            suspicion_score = 0
            if phone_found:
                suspicion_score += 50
            if not face_found or multiple_faces:
                suspicion_score += 50
            suspicion_placeholder.metric("Suspicion Score", f"{suspicion_score} / 100")

            # Alert Log
            alert_message = ""
            if phone_found:
                alert_message += "⚠️ Phone detected!\n"
            if not face_found:
                alert_message += "⚠️ No face detected!\n"
            if multiple_faces:
                alert_message += "⚠️ Multiple faces detected!\n"
            if alert_message == "":
                alert_message = "✅ No suspicious activity."

            alert_log.text(alert_message)

            # Give time for Streamlit to refresh
            time.sleep(0.05)

elif mode == "Idle":
    if st.session_state.cap:
        st.session_state.cap.release()
        st.session_state.cap = None
    st.info("Detection is idle.")
