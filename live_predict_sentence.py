import cv2
import mediapipe as mp
import pickle
import time
from grammar_corrector import correct_sentence  # ✅ Grammar fixer (Hugging Face version)

# Load trained model
with open("model/gesture_model.pkl", "rb") as f:
    model = pickle.load(f)

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Webcam setup
cap = cv2.VideoCapture(0)

# Sentence storage
sentence = []
last_word = ""
last_word_time = time.time()
last_correction_time = time.time()
polished = ""  # initialized once

# Update sentence only if word changes
def update_sentence(word):
    global last_word, last_word_time, sentence
    if word != last_word and time.time() - last_word_time > 1:
        sentence.append(word)
        last_word = word
        last_word_time = time.time()

print("🎥 Live Sign Prediction Running — Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks:
        for lm in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
            row = [v for p in lm.landmark for v in (p.x, p.y, p.z)]
            if len(row) == 63:
                pred = model.predict([row])[0]
                update_sentence(pred)
                cv2.putText(frame, f"{pred}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    # 🧠 Grammar correction every 2 seconds only
    raw_text = " ".join(sentence[-5:])
    if time.time() - last_correction_time > 2:
        polished = correct_sentence(raw_text)
        last_correction_time = time.time()

    # Display corrected sentence
    cv2.putText(frame, polished, (10, 450),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow("Live Sign to Sentence", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
