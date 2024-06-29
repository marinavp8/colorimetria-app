from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import dlib
import colorsys

app = Flask(__name__)
CORS(app)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def get_color(image, points):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.fillConvexPoly(mask, points, 255)
    mean = cv2.mean(image, mask=mask)[:3]
    return "#{:02x}{:02x}{:02x}".format(int(mean[2]), int(mean[1]), int(mean[0]))

def get_hair_color(image, landmarks, face):
    # Adjust the region based on the landmarks to better isolate the hair
    # Adding buffer zones around detected hairline
    padding = 10  # Adjust padding as necessary
    hair_region = np.array([(landmarks.part(i).x, max(landmarks.part(i).y - padding, 0)) for i in range(0, 17)], dtype=np.int32)
    if face.top() > padding:  # Use face directly here
        hair_region = np.vstack([hair_region, [(face.left(), face.top() - padding), (face.right(), face.top() - padding)]])
    
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.fillConvexPoly(mask, hair_region, 255)
    kernel = np.ones((10, 10), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=5)

    # Filter out skin-like colors based on predefined thresholds
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_skin_hsv = np.array([0, 10, 60])  # Lower bound of skin color in HSV
    upper_skin_hsv = np.array([20, 150, 255])  # Upper bound of skin color in HSV
    skin_mask = cv2.inRange(hsv_image, lower_skin_hsv, upper_skin_hsv)
    hair_mask = cv2.subtract(mask, skin_mask)
    
    hair_pixels = cv2.bitwise_and(image, image, mask=hair_mask)
    mean = cv2.mean(hair_pixels, mask=hair_mask)[:3]

    return "#{:02x}{:02x}{:02x}".format(int(mean[2]), int(mean[1]), int(mean[0]))



def convert_to_hsv(hex_color):
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    return colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

def score_color(hsv):
    h, s, v = hsv
    scores = {
        "Primavera": 0,
        "Verano": 0,
        "Otoño": 0,
        "Invierno": 0
    }
    if s > 0.5:  # Colores vivos
        if 0.02 <= h <= 0.1 or 0.8 <= h <= 0.98:  # Tonos rojos y rosados
            scores["Otoño"] += 2
        if 0.1 < h <= 0.29:  # Tonos amarillo a verde
            scores["Primavera"] += 2
        if 0.29 < h <= 0.6:  # Tonos verde a azul
            scores["Verano"] += 2
        if 0.6 < h < 0.8:  # Tonos azul a violeta
            scores["Invierno"] += 2
    else:  # Colores apagados
        if v < 0.5:
            scores["Invierno"] += 2  # Tonos oscuros
        else:
            scores["Verano"] += 1  # Tonos claros pero menos saturados
    return scores

def blend_colors(color1, color2):
    r1, g1, b1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
    r2, g2, b2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
    r = (r1 + r2) // 2
    g = (g1 + g2) // 2
    b = (b1 + b2) // 2
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def determine_colorimetria(hair, eyes, skin, lips):
    colors = [convert_to_hsv(hair), convert_to_hsv(eyes), convert_to_hsv(skin), convert_to_hsv(lips)]
    scores = [score_color(color) for color in colors]
    total_scores = {"Primavera": 0, "Verano": 0, "Otoño": 0, "Invierno": 0}
    for score in scores:
        for season, value in score.items():
            total_scores[season] += value
    return max(total_scores, key=total_scores.get)

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if not faces:
        return jsonify({"error": "No face detected"})

    face = faces[0]
    landmarks = predictor(gray, face)
    hair_color = get_hair_color(image, landmarks, face)
    left_eye_color = get_color(image, np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(36, 42)]))
    right_eye_color = get_color(image, np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(42, 48)]))
    eyes_color = blend_colors(left_eye_color, right_eye_color)
    skin_color = get_color(image, np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(1, 16)]))
    lips_color = get_color(image, np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(48, 60)]))

    colorimetria = determine_colorimetria(hair_color, eyes_color, skin_color, lips_color)
    return jsonify({
        "hair": hair_color,
        "eyes": eyes_color,
        "skin": skin_color,
        "lips": lips_color,
        "colorimetria": colorimetria
    })

if __name__ == '__main__':
    app.run(debug=True)

