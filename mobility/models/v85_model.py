from mobility.db import get_db

class v85:
    def __init__(self, rue_id:int, date:str, v85:float):
        self.rue_id = rue_id
        self.date = date
        self.v85 = v85

    def add(self):
        db = get_db()
        db.execute(
            "INSERT INTO v85 (rue_id, date, v85) VALUES (?, ?, ?)",
            (self.rue_id, self.date, self.v85)
        )
        db.commit()

    def delete(self):
        db = get_db()
        db.execute("DELETE FROM v85 WHERE rue_id=? AND date=?", (self.rue_id, self.date))
        db.commit()

    @staticmethod
    def get(rue_id:int, date:str):
        db = get_db()
        data = db.execute('SELECT * FROM v85 WHERE rue_id=? AND date=?', (rue_id, date)).fetchone()

        if data is None:
            return None
        return v85(data["rue_id"], data["date"], data["v85"])