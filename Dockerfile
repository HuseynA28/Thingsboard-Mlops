FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.in ./
COPY .env ./
# Install pip-tools and compile requirements
RUN pip install --no-cache-dir pip-tools && \
    pip-compile requirements.in && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY myFastapi ./myFastapi/

EXPOSE 8060

# Modified command to point to the correct path
CMD ["uvicorn", "myFastapi.main:app", "--reload", "--host", "0.0.0.0", "--port", "8060"]