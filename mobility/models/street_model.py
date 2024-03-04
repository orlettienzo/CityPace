from mobility.db import get_db

def get_street_list():
    db = get_db()
    return db.execute('SELECT rue.rue_id, rue.nom, rue.code_postal, ville.nom AS city_name FROM rue JOIN ville ON rue.code_postal = ville.code_postal ORDER BY rue.rue_id')

def search_street_id(street_id: int):
    db = get_db()
    return db.execute('SELECT * FROM rue WHERE rue_id=?', (street_id,)).fetchall()

class Street:
    """Classe représentant une rue"""
    def __init__(self, name, postal_code, street_id=None):
        self.name = name
        self.postal_code = postal_code
        self.street_id = street_id

    def delete(self):
        db = get_db()
        db.execute("DELETE FROM rue WHERE rue_id=?", (self.street_id,))
        db.commit()

    def add(self):
        db = get_db()
        db.execute("INSERT INTO rue(rue_id,nom, code_postal ) VALUES(?, ?, ?)", ( self.street_id, self.name, self.postal_code))
        db.commit()

    @staticmethod
    def get(street_id: int):
        db = get_db()
        data = db.execute('SELECT * FROM rue WHERE rue_id=?', (street_id,)).fetchone()

        if data is None:
            return None
        return Street(data["nom"], data["name"], data["rue_id"])
