# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file first
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install Ansible
RUN apt-get update && \
    apt-get install -y ansible && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . /app

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "check_ports.py"]