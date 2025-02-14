from mobility.utils.db import get_db

class Traffic:
    """Classe représentant le traffic dans une rue à une date/heure donnée."""
    def __init__(self, rue_id:int, code_postal:int, date:str, lourd:int, voiture:int, velo:int, pieton:int) -> None:
        """Crée un objet Traffic."""
        self.rue_id = rue_id
        self.code_postal = code_postal
        self.date = date
        self.lourd = lourd
        self.voiture = voiture
        self.velo = velo
        self.pieton = pieton

    @staticmethod
    def get(rue_id:int, date:str) -> "Traffic":
        """Retourne le traffic dans une rue à une date/heure donnée."""
        db = get_db()
        data = db.execute('SELECT * FROM traffic WHERE rue_id=? AND date=?', (rue_id, date)).fetchone()

        if data is None:
            return None
        return Traffic(data["rue_id"], data["code_postal"], data["date"], data["lourd"], data["voiture"], data["velo"], data["pieton"]) #fun fact: je crois ça ne marche pas (il faut utiliser data[index])

    @staticmethod
    def bulk_add(traffics: list) -> None:
        """Ajoute une liste de traffic dans la base de données."""
        db = get_db()
        db.executemany(
            "INSERT INTO traffic (rue_id, code_postal, date, lourd, voiture, velo, pieton) VALUES(?, ?, ?, ?, ?, ?, ?)",
            traffics
        )
        db.commit()

    def add(self) -> None:
        """Sauvegarde le traffic dans la base de données."""
        db = get_db()
        db.execute(
            "INSERT INTO traffic (rue_id, code_postal, date, lourd, voiture, velo, pieton) VALUES(?, ?, ?, ?, ?, ?, ?)",
            (self.rue_id, self.code_postal, self.date, self.lourd, self.voiture, self.velo, self.pieton)
        )
        db.commit()

    def delete(self) -> None:
        """Supprime le traffic de la base de données."""
        db = get_db()
        db.execute("DELETE FROM traffic WHERE rue_id=? AND date=?", (self.rue_id, self.date))
        db.commit()
