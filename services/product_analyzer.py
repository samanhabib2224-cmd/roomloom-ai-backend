import numpy as np
import cv2
from services.color_analysis import extract_colors

def analyze_product_image(image, name, color):

    # 📸 IMAGE READ
    file_bytes = np.frombuffer(image.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    name = name.lower()
    color = (color or "").lower()

    # 🏠 ROOM TYPE (STRONG LOGIC)
    if "bed" in name:
        room_type = "bedroom"
    elif "sofa" in name or "chair" in name:
        room_type = "living_room"
    elif "desk" in name or "office" in name:
        room_type = "office"
    elif "table" in name:
        room_type = "guest_room"
    else:
        room_type = "living_room"

    # 🎨 COLOR (HYBRID)
    colors, detected_family = extract_colors(img)

    if "white" in color or "beige" in color:
        color_family = "light"
    elif "black" in color or "brown" in color:
        color_family = "dark"
    else:
        color_family = detected_family  # fallback to AI

    # 💡 STYLE (BALANCED AI)
    brightness = np.mean(img)

    if brightness > 180 and color_family == "light":
        style = "minimal"
    elif brightness < 100 and color_family == "dark":
        style = "luxury"
    elif "wood" in name:
        style = "rustic"
    elif "gold" in name:
        style = "luxury"
    else:
        style = "modern"

    return {
        "room_type": room_type,
        "style": style,
        "color_family": color_family
    }