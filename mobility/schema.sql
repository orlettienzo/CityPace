DROP TABLE IF EXISTS ville;
CREATE TABLE IF NOT EXISTS ville (
    code_postal INTEGER NOT NULL UNIQUE,
    nom TEXT NOT NULL,
    population INTEGER NOT NULL,
    PRIMARY KEY(code_postal)
);
DROP TABLE IF EXISTS rue;
CREATE TABLE IF NOT EXISTS rue (
    rue_id INTEGER,
    nom TEXT NOT NULL,
    code_postal INTEGER NOT NULL,
    polyline TEXT,
    PRIMARY KEY (rue_id),
    FOREIGN KEY (code_postal) REFERENCES ville(code_postal)
);
DROP TABLE IF EXISTS vitesse;
CREATE TABLE IF NOT EXISTS vitesse (
    rue_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    tranche_de_vitesse INTEGER NOT NULL,
    proportion REAL NOT NULL,
    PRIMARY KEY (rue_id, date, tranche_de_vitesse),
    FOREIGN KEY (rue_id) REFERENCES rue(rue_id)
);
DROP TABLE IF EXISTS v85;
CREATE TABLE IF NOT EXISTS v85 (
    rue_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    v85_value REAL,
    PRIMARY KEY (rue_id, date)
    FOREIGN KEY (rue_id) REFERENCES rue(rue_id)
);
DROP TABLE IF EXISTS traffic;
CREATE TABLE IF NOT EXISTS traffic (
    rue_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    lourd INTEGER,
    voiture INTEGER,
    velo INTEGER,
    pieton INTEGER,
    FOREIGN KEY (rue_id) REFERENCES rue(rue_id),
    PRIMARY KEY (rue_id, date)
);
DROP TABLE IF EXISTS appdata;
CREATE TABLE IF NOT EXISTS appdata (
    data_id INTEGER NOT NULL,
    data_name TEXT NOT NULL,
    data_value INTEGER NOT NULL,
    PRIMARY KEY (data_id)
);
