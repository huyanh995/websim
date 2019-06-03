CREATE DATABASE websim;

USE websim;

CREATE TABLE combo (
    alpha_id VARCHAR(10),
    created_at DATE,
    alpha_code VARCHAR(3000),
    settings VARCHAR(1000),
    sharpe FLOAT,
    fitness FLOAT,
    grade VARCHAR(50),
    self_corr INT,
    prod_corr INT,
    longCount INT,
    shortCount INT,
    pnl INT,
    returns_ FLOAT,
    turnover FLOAT,
    margin FLOAT,
    drawdown FLOAT,
    submitted VARCHAR(50)
);

CREATE TABLE signals (
    alpha_id VARCHAR(10) NOT NULL,
    created_at DATE,
    alpha_code VARCHAR(3000),
    region VARCHAR(10),
    universe VARCHAR(10),
    settings VARCHAR(1000),
    sharpe FLOAT,
    fitness FLOAT,
    self_corr INT,
    prod_corr INT,
    longCount INT,
    shortCount INT,
    pnl INT,
    turnover FLOAT,
    count_used INT
);

CREATE TABLE log (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    logged_time DATETIME,
    func_name VARCHAR(50),
    exception VARCHAR(10000),
    response VARCHAR(10000)
);




