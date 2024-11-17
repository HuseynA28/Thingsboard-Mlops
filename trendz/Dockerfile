FROM thingsboard/trendz-python-executor:1.11.0

USER root

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    build-essential \
    libreadline-dev \
    libncursesw5-dev \
    libssl-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libbz2-dev \
    liblzma-dev \
    zlib1g-dev \
    uuid-dev \
    libffi-dev \
    libdb-dev \
    software-properties-common \
    pkg-config

# Download and install Python 3.12
RUN cd /tmp && \
    wget https://www.python.org/ftp/python/3.12.1/Python-3.12.1.tgz && \
    tar -xvf Python-3.12.1.tgz && \
    cd Python-3.12.1 && \
    ./configure --enable-optimizations \
                --with-lto \
                --with-computed-gotos \
                --enable-shared && \
    make -j$(nproc) && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.12.1 Python-3.12.1.tgz

# Update dynamic linker
RUN ldconfig

# Create symbolic links for Python 3.12
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.12 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 1 && \
    update-alternatives --set python /usr/local/bin/python3.12 && \
    update-alternatives --set python3 /usr/local/bin/python3.12

# Install pip for Python 3.12
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3.12 get-pip.py && \
    rm get-pip.py

# Verify installations
RUN python3.12 --version && \
    pip3.12 --version

# Install required packages with versions compatible with Python 3.12
RUN pip3.12 install --no-cache-dir \
    mlflow \
    "dask>=2023.3.0" \
    "distributed>=2023.3.0" \
    "numpy>=1.24.0" \
    pandas \
    scikit-learn \
    matplotlib \
    seaborn

# Set Python path and library path
ENV PYTHONPATH="/usr/local/lib/python3.12/site-packages:${PYTHONPATH}"
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*




# # Light Version 
# FROM thingsboard/trendz-python-executor:1.11.0

# USER root

# # Remove existing Python installations
# RUN apt-get update && \
#     apt-get remove -y python python3 && \
#     apt-get autoremove -y && \
#     update-alternatives --remove-all python || true && \
#     update-alternatives --remove-all python3 || true

# # Install essential dependencies
# RUN apt-get install -y --no-install-recommends \
#     wget \
#     build-essential \
#     libssl-dev \
#     zlib1g-dev \
#     libffi-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Download and install Python 3.12
# RUN cd /tmp && \
#     wget https://www.python.org/ftp/python/3.12.1/Python-3.12.1.tgz && \
#     tar -xf Python-3.12.1.tgz && \
#     cd Python-3.12.1 && \
#     ./configure --enable-shared && \
#     make -j2 && \
#     make altinstall && \
#     cd .. && \
#     rm -rf Python-3.12.1 Python-3.12.1.tgz

# # Update dynamic linker
# RUN ldconfig

# # Set up Python alternatives
# RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.12 1 && \
#     update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 1

# # Create symbolic links
# RUN ln -sf /usr/local/bin/python3.12 /usr/local/bin/python && \
#     ln -sf /usr/local/bin/python3.12 /usr/local/bin/python3

# # Install pip and essential packages
# RUN wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py && \
#     python3.12 get-pip.py && \
#     rm get-pip.py

# # Install only essential packages
# RUN pip3.12 install --no-cache-dir \
#     numpy \
#     pandas \
#     scikit-learn

# # Set environment variables for Python
# ENV PATH="/usr/local/bin:$PATH"
# ENV PYTHONPATH="/usr/local/lib/python3.12/site-packages:${PYTHONPATH}"
# ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"

# # Verify installation
# RUN python --version && \
#     which python