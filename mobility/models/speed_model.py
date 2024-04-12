from mobility.utils.db import get_db

class Speed:
    """Classe représentant une vitesse."""
    def __init__(self, rue_id:int, date:str, tranche_de_vitesse:int, proportion:float) -> None:
        """Crée un objet Speed."""
        self.rue_id = rue_id
        self.date = date
        self.tranche_de_vitesse = tranche_de_vitesse
        self.proportion = proportion

    def delete(self) -> None:
        """Supprime la vitesse de la base de données."""
        db = get_db()
        db.execute("DELETE FROM vitesse WHERE rue_id=? AND date=? AND tranche_de_vitesse=?", (self.rue_id, self.date, self.tranche_de_vitesse))
        db.commit()

    def add(self) -> None:
        """Sauvegarde la vitesse dans la base de données."""
        db = get_db()
        db.execute("INSERT INTO vitesse(rue_id, date, tranche_de_vitesse, proportion) VALUES(?, ?, ?, ?)", (self.rue_id, self.date, self.tranche_de_vitesse, self.proportion))
        db.commit()

    @staticmethod
    def bulk_add(speeds: list) -> None:
        """Ajoute une liste de vitesses dans la base de données."""
        db = get_db()
        db.executemany("INSERT INTO vitesse(rue_id, date, tranche_de_vitesse, proportion) VALUES(?, ?, ?, ?)", speeds)
        db.commit()

    @staticmethod
    def get(rue_id:int, date:str, tranche_de_vitesse:int) -> "Speed":
        db = get_db()
        data = db.execute('SELECT * FROM vitesse WHERE rue_id=? AND date=? AND tranche_de_vitesse=?', (rue_id, date, tranche_de_vitesse)).fetchone()

        if data is None:
            return None
        return Speed(data["rue_id"], data["date"], data["tranche_de_vitesse"], data["proportion"])
