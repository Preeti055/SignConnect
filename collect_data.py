import cv2, mediapipe as mp, csv, os, time

label = input("Enter sign label: ").strip().lower()
os.makedirs("data", exist_ok=True)
path = f"data/{label}.csv"
file = open(path, "a", newline=""); writer = csv.writer(file)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
last_time = time.time(); count = 0
print("Press 'q' to quit. Auto-saving every 2s.")

while cap.isOpened():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1); rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb); frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks:
        for lm in result.multi_hand_landmarks:
            draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
            row = [v for p in lm.landmark for v in (p.x, p.y, p.z)]
            if time.time() - last_time > 2:
                writer.writerow(row); count += 1; last_time = time.time()
                print(f"✅ Sample {count} saved.")

    cv2.imshow("Collecting", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release(); file.close(); cv2.destroyAllWindows()
print(f"📁 Done: {count} saved to {path}")
