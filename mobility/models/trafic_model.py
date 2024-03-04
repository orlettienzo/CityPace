from mobility.db import get_db

class Trafic:
    def __init__(self, rue_id:int, date:str, type_vehicule:str, nb_vehicules:int):
        self.rue_id = rue_id
        self.date = date
        self.type_vehicule = type_vehicule
        self.nb_vehicules = nb_vehicules

    def add(self):
        db = get_db()
        db.execute(
            "INSERT INTO trafic (rue_id, date, type_vehicule, nb_vehicules) VALUES (?, ?, ?, ?)",
            (self.rue_id, self.date, self.type_vehicule, self.nb_vehicules)
        )
        db.commit()

    def delete(self):
        db = get_db()
        db.execute("DELETE FROM trafic WHERE rue_id=? AND date=? AND type_vehicule=?", (self.rue_id, self.date, self.type_vehicule))
        db.commit()

    @staticmethod
    def get(rue_id:int, date:str, type_vehicule:str):
        db = get_db()
        data = db.execute('SELECT * FROM trafic WHERE rue_id=? AND date=? AND type_vehicule=?', (rue_id, date, type_vehicule)).fetchone()

        if data is None:
            return None
        return Trafic(data["rue_id"], data["date"], data["type_vehicule"], data["nb_vehicules"])