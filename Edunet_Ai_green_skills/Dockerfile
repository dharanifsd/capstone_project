# Green Skills AI - Dockerfile
# Multi-stage build for optimized container

# Stage 1: Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application files
COPY api.py start_server.py .
COPY models/ ./models/
COPY Datasets/ ./Datasets/

# Make sure scripts are executable
RUN chmod +x start_server.py

# Add local bin to PATH
ENV PATH=/root/.local/bin:$PATH

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run the API server
CMD ["python", "start_server.py"]

