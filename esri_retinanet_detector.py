from arcgis.learn import RetinaNet
import cv2
import os

# Load the pre-trained Esri RetinaNet model for person detection
# Make sure the model is downloaded from Esri's GitHub:
# https://github.com/Esri/deep-learning-models/tree/main/ObjectDetection/Person
# and placed in the 'model/' directory
MODEL_PATH = "model/person_retinanet.emd"
model = RetinaNet.from_model(MODEL_PATH)

def detect_persons(frame):
    temp_image_path = "temp_input.jpg"
    cv2.imwrite(temp_image_path, frame)

    # Predict using Esri's RetinaNet
    predictions = model.predict(temp_image_path)

    persons = []
    for pred in predictions:
        if pred['label'].lower() == 'person':
            x1, y1, x2, y2 = map(int, pred['bbox'])
            conf = float(pred['score'])
            persons.append((x1, y1, x2, y2, conf))

    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)

    return persons
