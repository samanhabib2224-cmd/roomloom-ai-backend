FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    libgomp1 \
    libgl1 \
    && apt-get clean

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

ENV PORT=8000

# Download models from S3, then start gunicorn
CMD ["sh", "-c", "python download_models.py && gunicorn app:app --bind 0.0.0.0:8000 --timeout 180 --workers 2"]
