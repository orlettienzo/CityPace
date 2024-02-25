DROP TABLE IF EXISTS ville;
CREATE TABLE IF NOT EXISTS ville (
   code_postal INTEGER PRIMARY KEY,
   nom TEXT NOT NULL,
   population INTEGER NOT NULL
);
DROP TABLE IF EXISTS rue;
CREATE TABLE IF NOT EXISTS rue (
   rue_id INTEGER PRIMARY KEY,
   nom TEXT NOT NULL,
   code_postal INTEGER,
   FOREIGN KEY (code_postal) REFERENCES ville(code_postal)
);