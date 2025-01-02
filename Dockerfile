# Base image
FROM python:3.9-slim

# Install Ansible and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    sshpass \
    ansible \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application code
COPY app/ ./app/
COPY ansible/ ./ansible/

# Install Python dependencies
RUN pip install --no-cache-dir -r app/requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app/app.py"]
