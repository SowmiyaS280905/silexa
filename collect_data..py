import cv2
import mediapipe as mp
import csv
import os

# Init MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# CSV Setup
CSV_FILE = 'gestures.csv'
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        header = [f'{i}_{axis}' for i in range(21) for axis in ('x', 'y')] + ['label']
        writer.writerow(header)

# Start camera
cap = cv2.VideoCapture(0)
label = input("Enter gesture label (e.g., OK, Hello): ").strip()

print("Press 'c' to capture. Press 'q' to quit.")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.append(lm.x)
                landmarks.append(lm.y)

            cv2.putText(frame, f'Gesture: {label}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                print(f"Captured: {label}")
                with open(CSV_FILE, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(landmarks + [label])
            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                exit()

    cv2.imshow("Collect Gesture Data", frame)
