FROM thingsboard/trendz-python-executor:1.11.0

USER root

# Remove existing Python installations
RUN apt-get update && \
    apt-get remove -y python python3 && \
    apt-get autoremove -y && \
    update-alternatives --remove-all python || true && \
    update-alternatives --remove-all python3 || true

# Install essential dependencies
RUN apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and install Python 3.11
RUN cd /tmp && \
    wget https://www.python.org/ftp/python/3.11.8/Python-3.11.8.tgz && \
    tar -xf Python-3.11.8.tgz && \
    cd Python-3.11.8 && \
    ./configure --enable-shared && \
    make -j2 && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.11.8 Python-3.11.8.tgz

# Update dynamic linker
RUN ldconfig

# Set up Python alternatives
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.11 1

# Create symbolic links
RUN ln -sf /usr/local/bin/python3.11 /usr/local/bin/python && \
    ln -sf /usr/local/bin/python3.11 /usr/local/bin/python3

# Install pip and essential packages
RUN wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py && \
    python3.11 get-pip.py && \
    rm get-pip.py

# Install only essential packages
RUN pip3.11 install --no-cache-dir \
    numpy \
    pandas \
    scikit-learn \
    mlflow \
    boto3   \
    prophet
COPY .env ./


# Set environment variables for Python
ENV PATH="/usr/local/bin:$PATH"
ENV PYTHONPATH="/usr/local/lib/python3.11/site-packages:${PYTHONPATH}"
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"

# Verify installation
RUN python --version && \
    which python