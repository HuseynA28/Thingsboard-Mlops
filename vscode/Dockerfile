# Use the official code-server image as the base
FROM codercom/code-server:latest

# Switch to root user to install packages
USER root

# Set environment variables for Miniconda installation
ENV CONDA_DIR=/opt/conda
ENV PATH=/opt/conda/bin:/usr/local/bin:$PATH

# Install system dependencies
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

# Download and install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p $CONDA_DIR && \
    rm /tmp/miniconda.sh && \
    $CONDA_DIR/bin/conda clean --all --yes

RUN $CONDA_DIR/bin/conda init bash


RUN conda install -y python=3.12

# **Option 2: Create a New Environment with a Different Name (Uncomment if Preferred)**
# RUN conda create -y -n myenv python=3.11

# Change ownership of the Conda directory to the 'coder' user
RUN chown -R coder:coder $CONDA_DIR

# Switch back to the 'coder' user
USER coder

# Ensure Conda is activated by default in all bash sessions for the 'coder' user
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> /home/coder/.bashrc && \
    echo "conda activate base" >> /home/coder/.bashrc

# Set the working directory
WORKDIR /app

# Optional: Clean up to reduce image size (already handled above, but included for completeness)
RUN conda clean -a -y