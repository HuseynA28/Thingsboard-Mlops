
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip
RUN pip install mlflow mysqlclient
EXPOSE 5000
CMD ["mlflow", "server"]
