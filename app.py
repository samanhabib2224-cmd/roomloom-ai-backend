import os
from dotenv import load_dotenv

load_dotenv()

# Download model weights from S3 before any service imports them
from download_models import download_models
download_models()

from flask import Flask
from flask_cors import CORS
from routes.ai_routes import ai_bp
from analytics.model_report import print_report

app = Flask(__name__)
CORS(app)

app.register_blueprint(ai_bp)

@app.route("/")
def home():
    return "AI Backend Running"

if __name__ == "__main__":
    print_report()
    app.run(host="0.0.0.0")
