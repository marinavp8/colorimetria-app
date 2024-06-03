from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import dlib

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# CORS(app, resources={r"/upload": {"origins": "*"}}) 



# Cargar el detector de rostros y el predictor de puntos de referencia
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def get_color(image, points):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.fillConvexPoly(mask, points, 255)
    mean = cv2.mean(image, mask=mask)[:3]
    return "#{:02x}{:02x}{:02x}".format(int(mean[2]), int(mean[1]), int(mean[0]))

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) == 0:
        return jsonify({"error": "No face detected"})

    face = faces[0]
    landmarks = predictor(gray, face)

    hair_color = get_color(image, np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(0, 17)]))
    left_eye_color = get_color(image, np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(36, 42)]))
    right_eye_color = get_color(image, np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(42, 48)]))
    eyes_color = blend_colors(left_eye_color, right_eye_color)
    skin_color = get_color(image, np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(1, 16)]))
    lips_color = get_color(image, np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(48, 60)]))

    colorimetria = determine_colorimetria(hair_color, eyes_color, skin_color, lips_color)

    return jsonify({"hair": hair_color, "eyes": eyes_color, "skin": skin_color, "lips": lips_color, "colorimetria": colorimetria})

def blend_colors(color1, color2):
    r1, g1, b1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
    r2, g2, b2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
    r = (r1 + r2) // 2
    g = (g1 + g2) // 2
    b = (b1 + b2) // 2
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def determine_colorimetria(hair, eyes, skin, lips):
    warm_count = sum([is_warm(color) for color in [hair, eyes, skin, lips]])
    
    if warm_count >= 3:
        return "Primavera/Otono"
    else:
        return "Verano/Invierno"

def is_warm(color):
    r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    return r > b

if __name__ == '__main__':
    app.run(debug=True)
