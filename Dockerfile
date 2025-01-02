# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file first
COPY app/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install Ansible
RUN apt-get update && \
    apt-get install -y ansible && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Ansible playbook and inventory
COPY ansible/ /ansible/

# Copy the rest of the application code
COPY app/ /app/
COPY templates/ /app/templates/

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]