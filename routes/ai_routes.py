from flask import Blueprint, request, jsonify
from services.room_analyzer import analyze_room

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/analyze-room", methods=["POST"])
def analyze():
    image = request.files["image"]
    furniture = request.form["furniture_type"]

    result = analyze_room(image, furniture)

    return jsonify(result)



@ai_bp.route("/analyze-product", methods=["POST"])
def analyze_product():

    image = request.files["image"]
    name = request.form.get("name", "")
    color = request.form.get("color", "")

    from services.product_analyzer import analyze_product_image

    result = analyze_product_image(image, name, color)

    return jsonify(result)