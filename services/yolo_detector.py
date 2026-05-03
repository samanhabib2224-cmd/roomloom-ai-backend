from ultralytics import YOLO
import numpy as np
import os

# ✅ LOCAL MODEL PATH
MODEL_PATH = "models/yolov8n.pt"

# ✅ LOAD MODEL (DOWNLOAD ONLY ONCE)
if not os.path.exists(MODEL_PATH):
    print("📥 Downloading YOLO model (one time only)...")
    
    model = YOLO("yolov8n.pt")   # download from internet
    
    os.makedirs("models", exist_ok=True)
    model.save(MODEL_PATH)       # save locally
    
    print("✅ YOLO model saved locally")

else:
    print("⚡ Loading YOLO from local file...")
    model = YOLO(MODEL_PATH)

# ✅ FUNCTION
def detect_space(img):

    results = model(img)[0]

    if results.boxes is None:
        return "large"

    boxes = results.boxes.xyxy.cpu().numpy()

    img_area = img.shape[0] * img.shape[1]

    occupied_area = 0

    for box in boxes:
        x1, y1, x2, y2 = box
        occupied_area += (x2 - x1) * (y2 - y1)

    ratio = occupied_area / img_area

    if ratio < 0.15:
        return "large"
    elif ratio < 0.35:
        return "medium"
    else:
        return "small"