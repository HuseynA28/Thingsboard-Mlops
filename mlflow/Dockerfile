# # mlflow/Dockerfile

# # Use an official Python runtime as a base image
# FROM python:3.12-slim

# # Set the working directory
# WORKDIR /app

# # Install MLflow
# RUN  pip install --upgrade pip  && \
#      pip install mlflow mysql

# # Expose port 5000 for MLflow
# EXPOSE 5000
# Use an official Python runtime as a base image
# # Start the MLflow server
# CMD ["mlflow", "server"]
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install MLflow and mysqlclient
RUN pip install mlflow mysqlclient

# Expose port 5000 for MLflow
EXPOSE 5000

# Start the MLflow server
CMD ["mlflow", "server"]

