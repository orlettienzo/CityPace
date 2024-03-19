PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

--Todo : add your test database

DROP TABLE IF EXISTS rue;
CREATE TABLE IF NOT EXISTS rue (
    rue_id INTEGER,
    nom TEXT NOT NULL,
    code_postal INTEGER NOT NULL,
    PRIMARY KEY (rue_id),
    FOREIGN KEY (code_postal) REFERENCES ville(code_postal)
);

INSERT INTO rue (rue_id, nom, code_postal) VALUES (1, 'Rua A', 12345);
INSERT INTO rue (rue_id, nom, code_postal) VALUES (2, 'Rua B', 12345);


DROP TABLE IF EXISTS ville;
CREATE TABLE IF NOT EXISTS ville (
    code_postal INTEGER NOT NULL UNIQUE,
    nom TEXT NOT NULL,
    population INTEGER NOT NULL,
    PRIMARY KEY(code_postal)
);

INSERT INTO ville (code_postal, nom, population) VALUES (1000, 'Ville A', 12000);
INSERT INTO ville (code_postal, nom, population) VALUES (3000, 'Ville B', 36000);
INSERT INTO ville (code_postal, nom, population) VALUES (5200, 'Ville C', 500);

INSERT INTO ville (code_postal, nom, population)
VALUES
  (4000, 'Liège', 250000),
  (5000, 'Namur', 100000);

COMMIT;
