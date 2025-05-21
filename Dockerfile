# Use Python 3.10 slim base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies required to build mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy the app files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=stuint.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run Flask app
CMD ["flask", "run"]
