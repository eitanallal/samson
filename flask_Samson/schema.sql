DROP TABLE IF EXISTS history;

CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    LoadWeight DECIMAL(10,3),
    WeightDestroyed DECIMAL(10,3),
    TakeOffDistance DECIMAL(10,3),
    created_time TIMESTAMP DATE DEFAULT (datetime('now','localtime')))
    ;