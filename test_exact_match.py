"""
Test to ensure web version matches desktop version exactly
"""
import cv2
import mediapipe as mp
import joblib
import pandas as pd
import numpy as np
import time

# Load model and labels (same as both versions)
print("Loading model and labels...")
model = joblib.load('model.pkl')
data = pd.read_csv('gestures.csv', header=None)
labels = sorted(data.iloc[:, -1].unique())

print(f"Model: {type(model)}")
print(f"Labels: {labels}")

# MediaPipe setup (same as detect_sign.py)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Test with sample data from CSV
print("\n=== Testing with CSV sample data ===")
sample_landmarks = data.iloc[0, :-1].values
sample_label = data.iloc[0, -1]
print(f"Sample landmarks length: {len(sample_landmarks)}")
print(f"Sample label: {sample_label}")

# Test prediction (exact same as detect_sign.py line 74)
prediction = model.predict([sample_landmarks])[0]
print(f"Prediction: {prediction}")
print(f"Matches expected: {prediction == sample_label}")

# Test with camera (same as detect_sign.py)
print("\n=== Testing with camera (same as detect_sign.py) ===")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not available")
    exit()

print("📷 Camera opened. Press 'q' to quit, 's' to test single frame")

frame_count = 0
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
        
        # EXACT same landmark extraction as detect_sign.py
        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.extend([lm.x, lm.y])
        
        if len(landmarks) == 42:
            # EXACT same prediction as detect_sign.py
            prediction = model.predict([landmarks])[0]
            prediction_text = prediction
            
            frame_count += 1
            if frame_count % 30 == 0:  # Every 30 frames
                print(f"🧠 Frame {frame_count}: Detected '{prediction}'")
                print(f"   Landmarks sample: {landmarks[:6]}")  # First 3 points
    
    # Display (same as detect_sign.py)
    cv2.putText(frame, f'Gesture: {prediction_text}', (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
    cv2.putText(frame, 'EXACT DESKTOP VERSION TEST', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, 'Press Q to quit, S to test single frame', (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)
    
    cv2.imshow("EXACT Desktop Test", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s') and result.multi_hand_landmarks:
        # Single frame test
        hand_landmarks = result.multi_hand_landmarks[0]
        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.extend([lm.x, lm.y])
        
        if len(landmarks) == 42:
            prediction = model.predict([landmarks])[0]
            print(f"\n🔍 SINGLE FRAME TEST:")
            print(f"   Landmarks length: {len(landmarks)}")
            print(f"   First 10 values: {landmarks[:10]}")
            print(f"   Prediction: '{prediction}'")
            print(f"   Available labels: {labels}")

cap.release()
cv2.destroyAllWindows()

print("\n✅ Desktop version test complete!")
print("Now compare this with the web version behavior.")
