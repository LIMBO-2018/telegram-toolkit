FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Install the package
RUN pip install -e .

# Create a volume for configuration and data
VOLUME /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set entrypoint
ENTRYPOINT ["telegram-toolkit"]
