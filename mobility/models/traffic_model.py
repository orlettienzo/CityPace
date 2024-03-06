from mobility.db import get_db

class Traffic:
    def __init__(self, rue_id:int, date:str, lourd:int, voiture:int, velo:int, pieton:int):
        self.rue_id = rue_id
        self.date = date
        self.lourd = lourd
        self.voiture = voiture
        self.velo = velo
        self.pieton = pieton

    def add(self):
        db = get_db()
        db.execute(
            "INSERT INTO traffic (rue_id, date, lourd, voiture, velo, pieton) VALUES(?, ?, ?, ?, ?, ?)",
            (self.rue_id, self.date, self.lourd, self.voiture, self.velo, self.pieton)
        )
        db.commit()

    def delete(self):
        db = get_db()
        db.execute("DELETE FROM traffic WHERE rue_id=? AND date=?", (self.rue_id, self.date))
        db.commit()

    @staticmethod
    def get(rue_id:int, date:str):
        db = get_db()
        data = db.execute('SELECT * FROM traffic WHERE rue_id=? AND date=?', (rue_id, date)).fetchone()

        if data is None:
            return None
        return Traffic(data["rue_id"], data["date"], data["lourd"], data["voiture"], data["velo"], data["pieton"])