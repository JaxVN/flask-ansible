# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file first
COPY app/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code
COPY app/ /app/

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app/app.py"]
