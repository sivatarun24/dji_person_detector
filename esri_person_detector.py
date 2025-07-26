from arcgis.learn import SingleShotDetector
from pathlib import Path
import cv2
import os

# Load the model (you must have a trained .emd file from ArcGIS Pro)
MODEL_PATH = Path("model/person_detector_model.emd")  # Update with your actual path
ssd = SingleShotDetector.from_model(emd_path=MODEL_PATH)

def detect_persons(frame):
    # Save current frame temporarily
    temp_image_path = "temp_input.jpg"
    cv2.imwrite(temp_image_path, frame)

    # Predict using the ArcGIS model
    preds = ssd.predict(temp_image_path)

    persons = []
    for pred in preds:
        if pred['label'].lower() == 'person':
            x1, y1, x2, y2 = map(int, pred['bbox'])
            conf = float(pred['score'])
            persons.append((x1, y1, x2, y2, conf))

    # Clean up
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)

    return persons
