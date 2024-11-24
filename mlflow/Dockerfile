FROM python:3.11-slim
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    curl \
    unzip \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm awscliv2.zip \
    && rm -rf aws

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir \
    mlflow\
    pymysql \
    cryptography \
    boto3 \
    mysqlclient \
    sqlalchemy \
    psycopg2-binary \
    numpy \
    pandas

# Expose MLflow port
EXPOSE 5000

# Set default environment variables (can be overridden)
ENV MYSQL_HOST=mysql
ENV MYSQL_PORT=3306

CMD ["sh", "-c", "mlflow server \
    --backend-store-uri mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DATABASE} \
    --artifacts-destination s3://${S3_MLFLOW_BUCKET_MLFLOW}/ \
    --default-artifact-root mlflow-artifacts:/artifacts \
    --host 0.0.0.0 \
    --port 5000 \
    --serve-artifacts"]