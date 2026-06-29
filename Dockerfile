FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libmagic1 \
    libgl1 \
    libglib2.0-0 \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*
    
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir uv

COPY requirements.txt ./

RUN if [ -s requirements.txt ]; then uv pip install --system --no-cache-dir -r requirements.txt; fi

COPY . .

CMD ["python3", "main.py"]
