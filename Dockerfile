FROM python:3.10-slim

WORKDIR /app

# System dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    && apt-get clean

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--timeout", "120"]