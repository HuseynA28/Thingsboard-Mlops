# Use an official Python runtime as a base image
FROM python:3.12-slim

WORKDIR /app

COPY requirements.in ./


RUN apt update 
RUN python -m venv venv && \
    echo "Virtual environment created successfully."

RUN pip install pip-tools && \
    pip-compile --upgrade requirements.in && \
    pip install --no-cache-dir -r requirements.txt
# Notify about the requirements file copy
RUN echo "Requirements file copied successfully."

COPY myFastapi ./

EXPOSE 8060

# Include a final echo to confirm the image was built successfully
RUN echo "Docker image built successfully."
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8060"]
