FROM python:3.10.11-slim

WORKDIR /app

# Copy requirements first for better Docker caching
COPY requirements.txt .

# Install Python dependencies with specific flags to avoid compilation issues
RUN pip install --no-cache-dir --only-binary=all -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose port (Railway needs this)
EXPOSE 8000

# Run your main application
CMD ["python", "main.py"]