FROM thingsboard/trendz:1.11.0

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-sklearn python3-pandas python3-numpy && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Allow pip to install into system site-packages


ENV PIP_BREAK_SYSTEM_PACKAGES=1

# Install mlflow via pip
RUN pip3 install mlflow dask==2024.9.1 distributed==2024.9.1 numpy==2.0.2

# (Optional) Expose port if needed
EXPOSE 8888

