# import joblib
# import numpy as np
# from supabase import create_client
# import os

# model = joblib.load("models/recommender.pkl")

# supabase = create_client(
#     os.getenv("SUPABASE_URL"),
#     os.getenv("SUPABASE_KEY")
# )

# def get_recommendations(room_type, style, color_family):

#     mapping = {
#         "bedroom":0,
#         "living_room":1,
#         "office":2,
#         "guest_room":3,
#         "modern":0,
#         "luxury":1,
#         "minimal":2,
#         "rustic":3,
#         "light":0,
#         "medium":1,
#         "dark":2
#     }

#     input_vec = [[
#         mapping[room_type],
#         mapping[style],
#         mapping[color_family]
#     ]]

#     distances, indices = model.kneighbors(input_vec)

#     data = supabase.table("furniture").select("*").execute().data

#     return [data[i] for i in indices[0]]
import joblib
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

model = joblib.load("models/recommender.pkl")

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def get_recommendations(room_type, style, color_family):

    mapping = {
        "bedroom":0,
        "living_room":1,
        "office":2,
        "guest_room":3,
        "modern":0,
        "luxury":1,
        "minimal":2,
        "rustic":3,
        "light":0,
        "medium":1,
        "dark":2
    }

    input_vec = [[
        mapping[room_type],
        # mapping[style],
        mapping[color_family]
    ]]

    pred = model.predict(input_vec)[0]
    print(pred)

    # 🔥 GET DATA FROM DB
    data = supabase.table("furniture") \
        .select("*, furniture_images(image_url)") \
        .eq("condition", "New") \
        .execute().data

    # 🔥 SAFE FILTER (NO INDEX BUG)
    filtered = []

    for item in data:
        if item.get("room_type") == room_type and item.get("style") == style:
            filtered.append(item)

    # fallback (if empty)
    if not filtered:
        filtered = data

    # fix images
    for item in filtered:
        images = item.get("furniture_images", [])
        item["image_url"] = images[0]["image_url"] if images else None

    return filtered[:3]