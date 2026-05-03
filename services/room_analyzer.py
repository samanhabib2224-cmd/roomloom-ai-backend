import numpy as np
import cv2

from services.scene_detection import detect_scene
from services.color_analysis import extract_colors
from services.recommender import get_recommendations
from services.style_predictor import detect_style
from services.yolo_detector import detect_space
#from services.recommendation_engine import get_recommendations

def analyze_room(image, furniture_type):

    file_bytes = np.frombuffer(image.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # 🧠 ROOM DETECTION
    room_type = detect_scene(img)

    # 🎨 COLORS
    colors, color_family = extract_colors(img)

    # 💡 LIGHTING
    brightness = np.mean(img)

    if brightness > 180:
        lighting = "bright"
    elif brightness > 120:
        lighting = "medium"
    else:
        lighting = "dim"

    # 📏 SPACE
    space = detect_space(img)

    # 🎯 STYLE LOGIC (IMPROVED)
    style = detect_style(img)

    # 🔥 FURNITURE → ROOM OVERRIDE (IMPORTANT)
    ft = furniture_type.lower()

    if "bed" in ft:
        room_type = "bedroom"
    elif "sofa" in ft or "chair" in ft:
        room_type = "living_room"
    elif "office" in ft or "desk" in ft:
        room_type = "office"
    elif "table" in ft:
        room_type = "guest_room"

    # 🎯 FINAL RECOMMENDATION
    recommendations = get_recommendations(
    room_type,
    style,
    color_family
)

    return {
        "room_type": room_type,
        "lighting": lighting,
        "style": style,
        "colors": colors,
        "space": space,
        "recommendations": recommendations
    }