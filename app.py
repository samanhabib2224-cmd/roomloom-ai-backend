from flask import Flask
from flask_cors import CORS
from routes.ai_routes import ai_bp
from analytics.model_report import print_report
import os   

app = Flask(__name__)
CORS(app)

app.register_blueprint(ai_bp)

if __name__ == "__main__":
    print_report() 
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))