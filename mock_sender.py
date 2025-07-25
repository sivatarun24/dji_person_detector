import socket
import json
import time
import os

# List of image filenames to send for each telemetry frame
image_files = ["person1.jpg", "person2.jpg", "person3.jpg", "person4.jpg", "person5.jpg"]
image_folder = "input"  # Folder containing the images

telemetries = [
    {
        "latitude": 34.062271,
        "longitude": -117.201897,
        "altitude": 30.5,
        "yaw": 75.0,
        "pitch": -20.0,
        "roll": 0.0,
        "fov": 82.6,
        "resolution": [384, 640]
    },
    {
        "latitude": 34.0972,
        "longitude": -117.2342,
        "altitude": 30.7,
        "yaw": 76.0,
        "pitch": -20.0,
        "roll": 0.0,
        "fov": 82.6,
        "resolution": [384, 640]
    },
    {
        "latitude": 34.0973,
        "longitude": -117.2343,
        "altitude": 30.9,
        "yaw": 77.0,
        "pitch": -21.0,
        "roll": 0.0,
        "fov": 82.6,
        "resolution": [448, 640]
    },
    {
        "latitude": 34.0973,
        "longitude": -117.2343,
        "altitude": 30.9,
        "yaw": 77.0,
        "pitch": -21.0,
        "roll": 0.0,
        "fov": 82.6,
        "resolution": [448, 640]
    },
    {
        "latitude": 34.0973,
        "longitude": -117.2343,
        "altitude": 30.9,
        "yaw": 77.0,
        "pitch": -21.0,
        "roll": 0.0,
        "fov": 82.6,
        "resolution": [448, 640]
    }
]

sock = socket.socket()
sock.connect(('127.0.0.1', 9999))

for i, metadata in enumerate(telemetries):
    try:
        image_path = os.path.join(image_folder, image_files[i])
        with open(image_path, "rb") as f:
            hex_image = f.read().hex()

        msg = {
            "type": "frame",
            "frame_id": i,
            "image": hex_image,
            "metadata": metadata
        }

        sock.sendall((json.dumps(msg) + '\n').encode())
        time.sleep(0.5)

    except FileNotFoundError:
        print(f"Image file '{image_files[i]}' not found in folder '{image_folder}'. Skipping...")
        continue

sock.close()
