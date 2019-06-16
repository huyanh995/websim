CREATE DATABASE websim;

USE websim;

CREATE TABLE combo (
    alpha_id VARCHAR(10) PRIMARY KEY NOT NULL,
    created_at DATE,
    alpha_code VARCHAR(3000),
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
    alpha_code VARCHAR(3000),
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

CREATE TABLE count_use (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    func_name VARCHAR(50),
    no1 INT,
    no2 INT,
    no3 INT
);

