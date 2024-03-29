CREATE DATABASE websim;

USE websim;

CREATE TABLE combo (
    alpha_id VARCHAR(10) PRIMARY KEY NOT NULL,
    created_at DATE,
    alpha_code VARCHAR(10000),
    settings VARCHAR(1000),
    sharpe FLOAT,
    fitness FLOAT,
    grade VARCHAR(50),
    self_corr FLOAT,
    prod_corr FLOAT,
    longCount INT,
    shortCount INT,
    pnl INT,
    returns_ FLOAT,
    turnover FLOAT,
    margin FLOAT,
    drawdown FLOAT,
    theme INT
);

CREATE TABLE signals (
    alpha_id VARCHAR(10) PRIMARY KEY NOT NULL,
    created_at DATE,
    alpha_code VARCHAR(3000),
    region VARCHAR(10),
    universe VARCHAR(10),
    settings VARCHAR(1000),
    sharpe FLOAT,
    fitness FLOAT,
    self_corr FLOAT,
    prod_corr FLOAT,
    longCount INT,
    shortCount INT,
    pnl INT,
    turnover FLOAT,
    theme INT,
    last_used DATE,
    count_used INT
);

CREATE TABLE submitted (
    alpha_id VARCHAR(10) PRIMARY KEY NOT NULL,
    created_at DATE,
    submitted_at DATE,
    alpha_code VARCHAR(10000),
    settings VARCHAR(1000),
    sharpe FLOAT,
    fitness FLOAT,
    grade VARCHAR(50),
    self_corr FLOAT,
    prod_corr FLOAT,
    longCount INT,
    shortCount INT,
    pnl INT,
    returns_ FLOAT,
    turnover FLOAT,
    margin FLOAT,
    drawdown FLOAT,
    theme INT,
    payout FLOAT,
    submitted VARCHAR(50)
);

CREATE TABLE log (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    logged_time DATETIME,
    func_name VARCHAR(50),
    exception VARCHAR(10000),
    response VARCHAR(10000)
);

CREATE TABLE login_log (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    logged_time DATETIME,
    func_name VARCHAR(50),
    exception VARCHAR(5000),
    response VARCHAR(5000)
);

CREATE TABLE alpha_error (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    logged_time DATETIME,
    alpha_code VARCHAR(8000),
    settings VARCHAR(1000),
    message VARCHAR(1000)
);

ALTER TABLE submitted MODIFY COLUMN alpha_code VARCHAR(10000);
ALTER TABLE combo MODIFY COLUMN alpha_code VARCHAR(10000);
ALTER TABLE signals ADD COLUMN actual_use INT DEFAULT 0 AFTER count_used, ADD COLUMN updated_at DATE AFTER created_at;