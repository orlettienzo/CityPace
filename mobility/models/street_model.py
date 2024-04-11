"""Module contenant la classe Street et les fonctions associées."""
import datetime # requis pour la fonction get_street_traffic_proportions_by_week_day
import sqlite3
import requests
from mobility.utils.db import get_db

def get_street_list() -> sqlite3.Cursor:
    """Retourne la liste des rues de la base de données."""
    db = get_db()
    return db.execute('SELECT rue.rue_id, rue.nom, rue.code_postal, ville.nom AS city_name \
                      FROM rue JOIN ville ON rue.code_postal = ville.code_postal\
                      ORDER BY rue.code_postal')

def get_street_list_for_city(postal_code: int) -> sqlite3.Cursor:
    """Retourne la liste des rues de la base de données qui sont dans la ville passée en paramètre."""
    db = get_db()
    return db.execute('SELECT rue.rue_id, rue.nom, rue.code_postal, ville.nom AS city_name\
                      FROM rue JOIN ville ON rue.code_postal = ville.code_postal\
                      WHERE rue.code_postal=?', (postal_code,))

def get_street_mapinfo() -> sqlite3.Cursor:
    """Retourne les informations nécessaires pour la carte"""
    db = get_db()
    return db.execute('SELECT rue.rue_id, rue.nom, rue.code_postal, rue.polyline, ville.nom AS city_name\
                      FROM rue JOIN ville ON rue.code_postal = ville.code_postal')

class Street:
    """Classe représentant une rue"""
    def __init__(self, name, postal_code, street_id, polyline="") -> None:
        """Crée une nouvelle rue."""
        self.name = name
        self.postal_code = postal_code
        self.street_id = street_id
        self.polyline = polyline

    @staticmethod
    def get(street_id: int) -> "Street":
        """Retourne une rue de la base de données qui a l'id passé en paramètre."""
        db = get_db()
        data = db.execute('SELECT * FROM rue WHERE rue_id=?', (street_id,)).fetchone()

        if data is None:
            return None
        return Street(data[1], data[2], data[0], data[3])

    def delete(self):
        """Supprime la rue de la base de données."""
        db = get_db()
        db.execute("DELETE FROM rue WHERE rue_id=?", (self.street_id,))
        db.commit()

    def add(self):
        """Sauvegarde la rue dans la base de données."""
        db = get_db()
        if self.polyline == "":
            self.polyline = self.get_street_polyline_latlng()
        db.execute("INSERT INTO rue(rue_id,nom, code_postal, polyline ) VALUES(?, ?, ?, ?)", 
                    (self.street_id, self.name, self.postal_code, self.polyline))
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
            t[key]["lourd"] = round((t[key]["lourd"]/total) * 100, 2)
            t[key]["voiture"] = round((t[key]["voiture"]/total) * 100, 2)
            t[key]["velo"] = round((t[key]["velo"]/total) * 100, 2)
            t[key]["pieton"] = round((t[key]["pieton"]/total) * 100, 2)

        return t

    def get_street_polyline_latlng(self) -> str:
        """Retourne la liste des coordonnées de la polyline de la rue en utilisant geopy."""
        url = f"https://nominatim.openstreetmap.org/search?q={self.name}, {self.postal_code}, Belgium&format=json"
        try:
            result = requests.get(url= url, timeout=10)
            result_json = result.json()
            return f"{result_json[0]['lat']},{result_json[0]['lon']}"
        except Exception as e:
            print(f"Error: {e}")
            print(f"result: {result}")
            print(f"result_json: {result_json}")
            return ""
