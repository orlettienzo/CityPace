from mobility.db import get_db

class Speed:
    def __init__(self, rue_id:int, date:str, tranche_de_vitesse:int, proportion:float):
        self.rue_id = rue_id
        self.date = date
        self.tranche_de_vitesse = tranche_de_vitesse
        self.proportion = proportion

    def delete(self):
        db = get_db()
        db.execute("DELETE FROM vitesse WHERE rue_id=? AND date=? AND tranche_de_vitesse=?", (self.rue_id, self.date, self.tranche_de_vitesse))
        db.commit()
        
    def add(self):
        db = get_db()
        db.execute("INSERT INTO vitesse(rue_id, date, tranche_de_vitesse, proportion) VALUES(?, ?, ?, ?)", (self.rue_id, self.date, self.tranche_de_vitesse, self.proportion))
        db.commit()

    @staticmethod
    def get(rue_id:int, date:str, tranche_de_vitesse:int):
        db = get_db()
        data = db.execute('SELECT * FROM vitesse WHERE rue_id=? AND date=? AND tranche_de_vitesse=?', (rue_id, date, tranche_de_vitesse)).fetchone()

        if data is None:
            return None
        return Speed(data["rue_id"], data["date"], data["tranche_de_vitesse"], data["proportion"])