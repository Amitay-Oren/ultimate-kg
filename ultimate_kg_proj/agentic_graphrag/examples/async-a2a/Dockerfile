# Use Python 3.13 slim image for smaller size
FROM python:3.13.2-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from parent directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the async-a2a application files
COPY async-a2a/agent.py .
COPY async-a2a/api_server.py .
COPY async-a2a/__init__.py .

# Copy .env from parent directory
COPY .env .env

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=api_server.py
ENV PORT=8080
ENV HOST=0.0.0.0

# Expose the port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the Flask API server
CMD ["python", "api_server.py"]