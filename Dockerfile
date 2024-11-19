# FROM python:3.12-slim

# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements file
# COPY requirements.in ./
# COPY .env ./
# # Install pip-tools and compile requirements
# RUN pip install --no-cache-dir pip-tools && \
#     pip-compile requirements.in && \
#     pip install --no-cache-dir -r requirements.txt

# # Copy application code
# COPY myFastapi ./myFastapi/

# EXPOSE 8060

# # Modified command to point to the correct path
# CMD ["uvicorn", "myFastapi.main:app", "--reload", "--host", "0.0.0.0", "--port", "8060"]


####  Install FastAPI with JupyterLab to save some space and avoid installing Python packages twice. If you do not want that deactive the code below and active the code above
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and environment variables
COPY requirements.in .env ./
# Install requirements including Jupyter
RUN pip install --no-cache-dir pip-tools && \
    pip-compile requirements.in && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install jupyter jupyterlab

# Copy application code
COPY myFastapi ./myFastapi/
COPY Snowflake-ml-script ./Snowflake-ml-script/
# Copy the startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose both ports
EXPOSE 8060 1010

# Set the startup script as the entrypoint
CMD ["/app/start.sh"]


