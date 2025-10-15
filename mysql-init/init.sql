CREATE DATABASE IF NOT EXISTS mppt_loggers;
USE mppt_loggers;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    tg_id BIGINT,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS loggers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    identifier VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS logger_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    logger_id INT NOT NULL,
    voltage FLOAT NOT NULL,
    current FLOAT NOT NULL,
    power FLOAT NOT NULL,
    illuminance FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (logger_id) REFERENCES loggers(id) ON DELETE CASCADE
);