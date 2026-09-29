FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app ./app
COPY frontend ./frontend

# Create directory for database
RUN mkdir -p /app/data

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]