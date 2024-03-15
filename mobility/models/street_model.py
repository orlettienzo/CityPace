from mobility.db import get_db
import datetime # requis pour la fonction get_street_traffic_proportions_by_week_day
import sqlite3

def get_street_list() -> sqlite3.Cursor:
    """Retourne la liste des rues de la base de données."""
    db = get_db()
    return db.execute('SELECT rue.rue_id, rue.nom, rue.code_postal, ville.nom AS city_name FROM rue JOIN ville ON rue.code_postal = ville.code_postal ORDER BY rue.code_postal')

def get_street_list_for_city(postal_code: int) -> sqlite3.Cursor:
    """Retourne la liste des rues de la base de données qui sont dans la ville passée en paramètre."""
    db = get_db()
    return db.execute('SELECT rue.rue_id, rue.nom, rue.code_postal, ville.nom AS city_name FROM rue JOIN ville ON rue.code_postal = ville.code_postal WHERE rue.code_postal=?', (postal_code,))

def search_street_id(street_id: int) -> "Street": # à retirer
    """Retourne un objet Street qui a l'id passé en paramètre."""
    db = get_db()
    data = db.execute('SELECT * FROM rue WHERE rue_id=?', (street_id,)).fetchone()
    return Street(data[1], data[2], data[0])

class Street:
    """Classe représentant une rue"""
    def __init__(self, name, postal_code, street_id=None) -> None:
        """Crée une nouvelle rue."""
        self.name = name
        self.postal_code = postal_code
        self.street_id = street_id

    @staticmethod
    def get(street_id: int) -> "Street":
        """Retourne une rue de la base de données qui a l'id passé en paramètre."""
        db = get_db()
        data = db.execute('SELECT * FROM rue WHERE rue_id=?', (street_id,)).fetchone()

        if data is None:
            return None
        return Street(data["nom"], data["name"], data["rue_id"])

    def delete(self):
        """Supprime la rue de la base de données."""
        db = get_db()
        db.execute("DELETE FROM rue WHERE rue_id=?", (self.street_id,))
        db.commit()

    def add(self):
        """Sauvegarde la rue dans la base de données."""
        db = get_db()
        db.execute("INSERT INTO rue(rue_id,nom, code_postal ) VALUES(?, ?, ?)", ( self.street_id, self.name, self.postal_code))
        db.commit()

    def get_street_traffic_proportions_by_week_day(self) -> dict:
        """Calcule la proportion de chaque type de vehicule dans la rue pour chaque jour de la semaine."""
        db = get_db()
        data = db.execute('SELECT * FROM traffic WHERE rue_id=?', (self.street_id,)).fetchall()
        t = {} # tableau du traffic de chaque jour de la semaine
        for traffic in data:
            try:
                jour = datetime.datetime.strptime(traffic["date"][:10], '%Y-%m-%d').strftime('%A')
            except ValueError:
                jour = "Unknown"
            # t.append({"lourd": traffic["lourd"], "voiture": traffic["voiture"], "velo": traffic["velo"], "pieton": traffic["pieton"], "date": traffic["date"], "jour": jour})
            if jour in t:
                t[jour]["lourd"] += traffic["lourd"]
                t[jour]["voiture"] += traffic["voiture"]
                t[jour]["velo"] += traffic["velo"]
                t[jour]["pieton"] += traffic["pieton"]
            else:
                t[jour] = {"lourd": traffic["lourd"], "voiture": traffic["voiture"], "velo": traffic["velo"], "pieton": traffic["pieton"]}

        for key in t:
            total = t[key]["lourd"] + t[key]["voiture"] + t[key]["velo"] + t[key]["pieton"]
            if total == 0:
                t[key]["lourd"] = 0
                t[key]["voiture"] = 0
                t[key]["velo"] = 0
                t[key]["pieton"] = 0
                continue
            t[key]["lourd"] = (t[key]["lourd"]/total) * 100
            t[key]["voiture"] = (t[key]["voiture"]/total) * 100
            t[key]["velo"] = (t[key]["velo"]/total) * 100
            t[key]["pieton"] = (t[key]["pieton"]/total) * 100

        return t
