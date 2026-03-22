# Use official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Convert requirements.txt to UTF-8 to prevent pip read errors on Linux, then install dependencies
# We also install gunicorn for serving the Flask app in production
RUN apt-get update && apt-get install -y dos2unix && \
    iconv -f UTF-16LE -t UTF-8 requirements.txt > req_utf8.txt && \
    pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r req_utf8.txt && \
    pip install --no-cache-dir gunicorn

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on (Railway sets PORT environment variable)
EXPOSE 5000

# Run the app with gunicorn, binding it to 0.0.0.0 and the PORT environment variable
CMD gunicorn --workers=2 --threads=4 --worker-class=gthread --bind 0.0.0.0:$PORT app:app
