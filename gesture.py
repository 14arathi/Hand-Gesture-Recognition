     

import cv2
import mediapipe as mp
import numpy as np

mphands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hand = mphands.Hands()

gesture = {
    (0,0,0,0,0): "Fist",
    (1,0,0,0,0): "Thumbs-up",
    (0,1,1,0,0): "Peace",
    (1,1,1,1,1): "Open palm",
    (1,0,0,0,1): "Call"
}

def detect_gesture_from_image(image):
    # PIL image -> OpenCV image
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    img = cv2.flip(img, 1)

    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hand.process(img1)

    tipids = [4, 8, 12, 16, 20]
    gestures = "No Hand"
    fingercount = 0

    if result.multi_hand_landmarks:
        for handlm in result.multi_hand_landmarks:
            lmlist = []

            for id, lm in enumerate(handlm.landmark):
                cx = lm.x
                cy = lm.y
                lmlist.append([id, cx, cy])

            if len(lmlist) == 21:
                fingertips = []

                # THUMB LOGIC 
                if lmlist[8][1] < lmlist[20][1]:
                    if lmlist[4][1] > lmlist[3][1]:
                        fingertips.append(0)
                    else:
                        fingertips.append(1)
                else:
                    if lmlist[4][1] < lmlist[3][1]:
                        fingertips.append(0)
                    else:
                        fingertips.append(1)

                # OTHER FINGERS
                for i in range(1, 5):
                    if lmlist[tipids[i]][2] > lmlist[tipids[i]-2][2]:
                        fingertips.append(0)
                    else:
                        fingertips.append(1)

                fingercount = fingertips.count(1)
                gestures = gesture.get(tuple(fingertips), "Unknown")

            # Draw text
            cv2.putText(
                img,
                gestures,
                (35, 50),
                cv2.FONT_HERSHEY_COMPLEX,
                1.2,
                (0, 0, 255),
                2
            )

            # Draw landmarks
            mp_drawing.draw_landmarks(img, handlm, mphands.HAND_CONNECTIONS)

    # Convert back for Streamlit
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img, gestures, fingercount