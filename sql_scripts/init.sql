-- Create user and grant privileges
CREATE USER IF NOT EXISTS 'mlflow_user'@'%' IDENTIFIED BY 'secure_password123';
GRANT ALL PRIVILEGES ON mlflow_db.* TO 'mlflow_user'@'%';
FLUSH PRIVILEGES;

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS mlflow_db;