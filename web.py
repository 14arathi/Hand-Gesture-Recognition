
import streamlit as st
from PIL import Image
from gesture import detect_gesture_from_image

st.set_page_config(page_title="Hand Gesture Recognition", layout="centered")

st.title("Hand Gesture Recognition")
st.write("Capture your hand gesture and detect it using MediaPipe")

captured_image = st.camera_input("Capture your hand gesture")

if captured_image is not None:
    image = Image.open(captured_image)

    processed_img, gesture_name, finger_count = detect_gesture_from_image(image)

    st.success(f"Detected Gesture: {gesture_name}")
    st.info(f"Finger Count: {finger_count}")

    st.image(processed_img, caption="Processed Image", use_container_width=True)