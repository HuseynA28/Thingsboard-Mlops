
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*


# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm awscliv2.zip \
    && rm -rf aws

RUN pip install --upgrade pip
RUN pip install --no-cache-dir \
    mlflow \
    pymysql \
    cryptography \
    boto3 \
    mysqlclient \
    sqlalchemy \
    psycopg2-binary \
    numpy \
    pandas

EXPOSE 5000
CMD mlflow server \
    --backend-store-uri ${BACKEND_URI} \
    --default-artifact-root ${ARTIFACT_ROOT} \
    --host 0.0.0.0 \
    --port 5000 \
    --serve-artifacts
