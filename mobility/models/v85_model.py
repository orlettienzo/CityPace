from mobility.utils.db import get_db

class v85:
    """Classe représentant une v85 (vitesse à laquelle 85% des véhicules roulent)."""
    def __init__(self, rue_id:int, date:str, v85:float) -> None:
        """Crée un objet v85."""
        self.rue_id = rue_id
        self.date = date
        self.v85 = v85

    def add(self) -> None:
        """Sauvegarde la v85 dans la base de données."""
        db = get_db()
        db.execute(
            "INSERT INTO v85 (rue_id, date, v85_value) VALUES (?, ?, ?)",
            (self.rue_id, self.date, self.v85)
        )
        db.commit()

    @staticmethod
    def bulk_add(v85s: list) -> None:
        """Ajoute une liste de v85 dans la base de données."""
        db = get_db()
        db.executemany(
            "INSERT INTO v85 (rue_id, date, v85_value) VALUES (?, ?, ?)",
            v85s
        )
        db.commit()

    def delete(self) -> None:
        """Supprime la v85 de la base de données."""
        db = get_db()
        db.execute("DELETE FROM v85 WHERE rue_id=? AND date=?", (self.rue_id, self.date))
        db.commit()

    @staticmethod
    def get(rue_id:int, date:str) -> "v85":
        """Retourne la v85 dans une rue à une date/heure donnée."""
        db = get_db()
        data = db.execute('SELECT * FROM v85 WHERE rue_id=? AND date=?', (rue_id, date)).fetchone()

        if data is None:
            return None
        return v85(data["rue_id"], data["date"], data["v85_value"])