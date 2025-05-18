FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Alembic configuration and scripts
# Assumes alembic.ini and the 'alembic' directory are in the root of the build context (./backend)
COPY alembic.ini .
COPY alembic ./alembic

# Copy application code
COPY app ./app

# Expose port (default FastAPI/uvicorn port)
EXPOSE 8001

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload", "--proxy-headers", "--forwarded-allow-ips", "*"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload", "--proxy-headers", "--forwarded-allow-ips", "*", "--root-path", "/proxy"]