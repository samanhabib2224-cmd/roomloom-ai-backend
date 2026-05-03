def auto_tag_furniture(name, color):

    name = name.lower()
    color = (color or "").lower()

    # 🏠 ROOM TYPE (expanded)
    if "bed" in name:
        room_type = "bedroom"
    elif "sofa" in name or "coffee" in name:
        room_type = "living_room"
    elif "table" in name:
        room_type = "guest_room"
    elif "office" in name or "desk" in name:
        room_type = "office"
    else:
        room_type = "living_room"

    # 🎨 STYLE (advanced)
    if "wood" in name:
        style = "rustic"
    elif "luxury" in name or "gold" in name:
        style = "luxury"
    elif "minimal" in name:
        style = "minimal"
    else:
        style = "modern"

    # 🌈 COLOR FAMILY
    if any(c in color for c in ["white", "cream", "beige"]):
        color_family = "light"
    elif any(c in color for c in ["black", "brown"]):
        color_family = "dark"
    else:
        color_family = "medium"

    return room_type, style, color_family

