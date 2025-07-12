from flask import Flask, request, jsonify, send_from_directory
import cv2
import mediapipe as mp
import numpy as np
import base64
import re
import pickle
from grammar_corrector import correct_sentence  # ✅ Make sure this is working

app = Flask(__name__)

# Load ML model
with open("model/gesture_model.pkl", "rb") as f:
    model = pickle.load(f)

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.7)

# ✅ Route to serve signlive.html from `pages/`
@app.route("/")
def serve_signlive():
    return send_from_directory("pages", "signlive.html")

# ✅ Predict endpoint
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    image_data = data.get("image")

    # Clean and decode base64
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    image = base64.b64decode(image_data)
    nparr = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Flip to mirror like webcam
    img = cv2.flip(img, 1)

    # Convert and process
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for lm in result.multi_hand_landmarks:
            row = [v for p in lm.landmark for v in (p.x, p.y, p.z)]
            if len(row) == 63:
                pred = model.predict([row])[0]
                corrected = correct_sentence(pred)  # Use grammar AI here
                return jsonify({"prediction": pred, "corrected": corrected})

    return jsonify({"prediction": "No Hand", "corrected": "No Hand"})

if __name__ == "__main__":
    app.run(debug=True)
