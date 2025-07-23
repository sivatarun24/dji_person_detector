# from ultralytics import YOLO

# model = YOLO("yolov8n.pt")  # Use a YOLOv8 model (not yolov5s.pt)

# def detect_persons(frame):
#     results = model(frame)[0]  # get first result
#     boxes = []

#     for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
#         if int(cls.item()) == 0:  # class 0 = person
#             x1, y1, x2, y2 = map(int, box)
#             boxes.append((x1, y1, x2, y2))

#     return boxes


from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # or yolov8s.pt, etc.

def detect_persons(frame):
    results = model(frame)[0]
    persons = []

    for box, cls, conf in zip(results.boxes.xyxy, results.boxes.cls, results.boxes.conf):
        if int(cls.item()) == 0:  # class 0 = person
            x1, y1, x2, y2 = map(int, box)
            persons.append((x1, y1, x2, y2, float(conf)))

    return persons
