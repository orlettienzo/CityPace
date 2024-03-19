PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

--Todo : add your test database
INSERT INTO ville (code_postal, nom, population)
VALUES
  (4000, 'Liège', 250000),
  (5000, 'Namur', 100000);


COMMIT;
