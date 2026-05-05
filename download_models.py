import boto3
import os
from dotenv import load_dotenv

load_dotenv()

BUCKET = os.getenv("S3_BUCKET_NAME")

MODELS = [
    "models/resnet18_places365.pth.tar",
    "models/style_model.pth",
    "models/recommender.pkl",
    "models/yolov8n.pt",
    "models/categories_places365.txt",
]

def download_models():
    if not BUCKET:
        raise ValueError("S3_BUCKET_NAME environment variable is not set")

    s3 = boto3.client("s3")
    os.makedirs("models", exist_ok=True)

    for path in MODELS:
        if os.path.exists(path):
            print(f"[S3] Already exists, skipping: {path}")
            continue

        print(f"[S3] Downloading {path} ...")
        s3.download_file(BUCKET, path, path)
        print(f"[S3] Done: {path}")

if __name__ == "__main__":
    download_models()
