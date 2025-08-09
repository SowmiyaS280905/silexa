import cv2
import numpy as np
import time
from gtts import gTTS
import os
import joblib
import pandas as pd
import mediapipe as mp

try:
    from playsound import playsound
except ImportError:
    playsound = None

# === Load Model & Labels ===
model = joblib.load("model.pkl")
data = pd.read_csv('gestures.csv', header=None)
labels = sorted(data.iloc[:, -1].unique())

# === Mediapipe Optimized ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# === TTS ===
prev_prediction = None
last_spoken = 0
cooldown = 2  # seconds

def speak_word(text):
    try:
        tts = gTTS(text=text, lang='en')
        filename = "voice.mp3"
        tts.save(filename)
        if playsound:
            playsound(filename, block=False)
        os.remove(filename)
    except Exception as e:
        print(f"[TTS Error]: {e} - Would have said: {text}")

# === Webcam ===
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("🎥 SILEXA - Real-Time Sign Detection Started")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    prediction_text = "No hand detected"

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.extend([lm.x, lm.y])

        if len(landmarks) == 42:
            prediction = model.predict([landmarks])[0]
            prediction_text = prediction

            current_time = time.time()
            if prediction != prev_prediction and (current_time - last_spoken > cooldown):
                print(f"🧠 Detected: {prediction}")
                speak_word(prediction)
                prev_prediction = prediction
                last_spoken = current_time

    # === Overlay UI ===
    cv2.putText(frame, f'Gesture: {prediction_text}', (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
    cv2.putText(frame, 'SILEXA - Real-time Detection', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, 'Press ESC to exit', (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)

    cv2.imshow("SILEXA Sign Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
