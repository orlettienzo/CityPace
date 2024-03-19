PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

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

COMMIT;
