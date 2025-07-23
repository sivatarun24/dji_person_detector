import socket
import json
import cv2
import numpy as np
from detector import detect_persons  # Must return (x1, y1, x2, y2, conf)
from coordinate_mapper import map_to_coordinates  # Should accept box[:4], metadata

import os
os.makedirs("output", exist_ok=True)


# Create TCP server socket
sock = socket.socket()
sock.bind(('0.0.0.0', 9999))  # Listen on all interfaces
sock.listen(1)
print("Receiver is waiting for connection on port 9999...")
conn, addr = sock.accept()
print(f"Connected by {addr}")

buffer = ""

try:
    while True:
        data = conn.recv(65536)
        if not data:
            print("Connection closed by sender.")
            break

        buffer += data.decode(errors="ignore")
        while '\n' in buffer:
            line, buffer = buffer.split('\n', 1)

            try:
                msg = json.loads(line)
                if msg.get("type") != "frame" or "image" not in msg or "metadata" not in msg:
                    print("Invalid message format, skipping...")
                    continue

                # Convert hex string to OpenCV frame
                frame_bytes = bytes.fromhex(msg["image"])
                frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
                frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

                if frame is None:
                    print("Failed to decode frame")
                    continue

                # Detect people (boxes must be in format: x1, y1, x2, y2, confidence)
                boxes = detect_persons(frame)
                coords = map_to_coordinates([box[:4] for box in boxes], msg["metadata"])

                for i, (x1, y1, x2, y2, conf) in enumerate(boxes):
                    point = coords[i]
                    lat = point.latitude
                    lon = point.longitude

                    # Draw bounding box around person
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Label with coordinates and confidence
                    label = f"{conf * 100:.1f}%"
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)

                    # Print to console
                    print(f"Person {i+1}:")
                    print(f"  Confidence: {conf * 100:.2f}%")
                    print(f"  GPS: ({lat:.6f}, {lon:.6f})")

                # Save entire frame (after all annotations are done)
                frame_id = msg.get("frame_id", 0)
                cv2.imwrite(f"output/frame_{frame_id}.jpg", frame)

                # Show frame
                cv2.imshow("Drone Frame", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Receiver interrupted by user.")
                    break

            except Exception as e:
                print("Error processing line:", e)
                continue

except KeyboardInterrupt:
    print("Receiver stopped.")

finally:
    conn.close()
    sock.close()
    cv2.destroyAllWindows()
