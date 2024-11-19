FROM codercom/code-server:latest

# Switch to root for installation
USER root

# Environment variables
ENV CONDA_DIR=/opt/conda
ENV PATH=/opt/conda/bin:/usr/local/bin:$PATH

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    git \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p $CONDA_DIR && \
    rm /tmp/miniconda.sh && \
    $CONDA_DIR/bin/conda clean --all --yes

RUN $CONDA_DIR/bin/conda init bash

# Install Python 3.12
RUN conda install -y python=3.12

# Setup VSCode directories
RUN mkdir -p /home/coder/.local/share/code-server/User && \
    touch /home/coder/.local/share/code-server/User/settings.json && \
    chown -R coder:coder /home/coder/.local && \
    chown -R coder:coder $CONDA_DIR

# Switch back to coder user
USER coder

# Configure conda for coder user
RUN echo ". $CONDA_DIR/bin/conda" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

WORKDIR /app

# Cleanup
RUN conda clean -a -y