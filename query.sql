USE websim;

DROP TABLE signals

CREATE TABLE combo (
    alpha_id VARCHAR(10),
    created_at INT,
    alpha_code VARCHAR(3000),
    settings VARCHAR(255),
    sharpe FLOAT,
    fitness FLOAT,
    grade VARCHAR(10),
    self_corr INT,
    prod_corr INT,
    longCount INT,
    shortCount INT,
    pnl INT,
    turnover FLOAT,
    margin FLOAT,
    drawdown FLOAT,
    submitted VARCHAR(10)
);

CREATE TABLE signals (
    alpha_id VARCHAR(10) NOT NULL,
    created_at INT,
    alpha_code VARCHAR(3000),
    settings VARCHAR(255),
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

