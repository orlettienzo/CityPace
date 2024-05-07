"""Module contenant la classe Street et les fonctions associées."""
import datetime # requis pour la fonction get_street_traffic_proportions_by_week_day
import sqlite3
import requests
from mobility.utils.db import get_db
import time

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
    return db.execute('''SELECT rue.rue_id, rue.nom, rue.code_postal, SUBSTR(rue.polyline, 1, INSTR(rue.polyline, ",")-1) AS latitude, SUBSTR(rue.polyline, INSTR(rue.polyline, ",")+1) AS longitude, ville.nom AS city_name, SUM(traffic.lourd) AS lourd, SUM(traffic.voiture) AS voiture, SUM(traffic.velo) AS velo, SUM(traffic.pieton) AS pieton
                        FROM rue JOIN ville ON rue.code_postal = ville.code_postal JOIN traffic ON rue.rue_id = traffic.rue_id
                        GROUP BY rue.rue_id''')

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

    @staticmethod
    def bulk_add(streets: list):
        """Ajoute une liste de rues dans la base de données."""
        db = get_db()
        db.executemany("INSERT INTO rue(rue_id, nom, code_postal, polyline ) VALUES(?, ?, ?, ?)", streets)
        db.commit()

    def delete(self):
        """Supprime la rue de la base de données."""
        db = get_db()
        db.execute("DELETE FROM rue WHERE rue_id=?", (self.street_id,))
        db.commit()

    def add(self):
        """Sauvegarde la rue dans la base de données."""
        db = get_db()
        db.execute("INSERT INTO rue(rue_id,nom, code_postal, polyline ) VALUES(?, ?, ?, ?)", 
                    (self.street_id, self.name, self.postal_code, self.polyline))
        db.commit()
    
    def get_amount_of_traffic_for_day(self, date: str) -> dict:
        """Retourne le nombre de chaque type de véhicule dans la rue pour une journée donnée.
        date doit être au format ISO (2024-01-05T15:00:00.000Z).
        note: l'heure n'est pas prise en compte.
        """
        # print(f"date: {date}")
        db = get_db()
        data = db.execute('SELECT * FROM traffic WHERE rue_id=? AND date BETWEEN ? AND ?', (self.street_id, date[:10], date[:10] + "T23:59:59.999Z")).fetchall()
        t = {"lourd": 0, "voiture": 0, "velo": 0, "pieton": 0}
        for traffic in data:
            t["lourd"] += traffic["lourd"]
            t["voiture"] += traffic["voiture"]
            t["velo"] += traffic["velo"]
            t["pieton"] += traffic["pieton"]
        return t

    def get_street_traffic_proportions_for_period(self, start_date: str, end_date: str) -> dict:
        """Calcule la proportion de chaque type de vehicule dans la rue pour une période donnée."""
        db = get_db()
        data = db.execute('SELECT * FROM traffic WHERE rue_id=? AND date BETWEEN ? AND ?', (self.street_id, start_date, end_date)).fetchall()
        t = {"lourd": 0, "voiture": 0, "velo": 0, "pieton": 0}
        for traffic in data:
            t["lourd"] += traffic["lourd"]
            t["voiture"] += traffic["voiture"]
            t["velo"] += traffic["velo"]
            t["pieton"] += traffic["pieton"]

        total = t["lourd"] + t["voiture"] + t["velo"] + t["pieton"]
        if total == 0:
            t["lourd"] = 0
            t["voiture"] = 0
            t["velo"] = 0
            t["pieton"] = 0
        else:
            t["lourd"] = round((t["lourd"]/total) * 100, 2)
            t["voiture"] = round((t["voiture"]/total) * 100, 2)
            t["velo"] = round((t["velo"]/total) * 100, 2)
            t["pieton"] = round((t["pieton"]/total) * 100, 2)

        return t
    
    def get_street_time_span(self) -> dict:
        """Retourne la date de début et de fin du traffic pour la rue."""
        db = get_db()
        data = db.execute('SELECT MIN(date) AS start_date, MAX(date) AS end_date FROM traffic WHERE rue_id=?', (self.street_id,)).fetchone()
        return {"start_date": data["start_date"], "end_date": data["end_date"]}

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

        # renommer les jours en français
        if "Monday" in t:
            t["Lundi"] = t.pop("Monday")
        if "Tuesday" in t:
            t["Mardi"] = t.pop("Tuesday")
        if "Wednesday" in t:
            t["Mercredi"] = t.pop("Wednesday")
        if "Thursday" in t:
            t["Jeudi"] = t.pop("Thursday")
        if "Friday" in t:
            t["Vendredi"] = t.pop("Friday")
        if "Saturday" in t:
            t["Samedi"] = t.pop("Saturday")
        if "Sunday" in t:
            t["Dimanche"] = t.pop("Sunday")


        return t

    def set_street_polyline_latlng(self) -> None:
        """Retourne la liste des coordonnées de la polyline de la rue en utilisant geopy."""
        url = f"https://nominatim.openstreetmap.org/search?q={self.name}, {self.postal_code}, Belgium&format=json"
        try:
            with requests.get(url= url, timeout=10) as result:
                result_json = result.json()
                self.polyline = f"{result_json[0]['lat']},{result_json[0]['lon']}"
        except Exception as e:
            print(f"Error: {e}")
            self.polyline = ""

    def get_street_traffic_over_time(self, start_date: str, end_date: str) -> dict:
        """Calcule le traffic de la rue pour chaque jour de la période donnée en utilisant la méthode get_amount_of_traffic_for_day.
        start_date et end_date doivent être au format ISO (2024-01-05T15:00:00.000Z)"""
        number_of_days = (datetime.datetime.strptime(end_date[:10], '%Y-%m-%d') - datetime.datetime.strptime(start_date[:10], '%Y-%m-%d')).days
        t = {"lourd": [], "voiture": [], "velo": [], "pieton": [], "labels": []}
        datelist = []

        # step = max(1, number_of_days // 10) # peut être ajusté pour obtenir un graphique plus lisible et faire moins de requêtes
        for i in range(0, number_of_days + 1):
            datelist.append((datetime.datetime.strptime(start_date[:10], '%Y-%m-%d') + datetime.timedelta(days=i)).isoformat() + ".000Z")

        weekdays = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

        for date in datelist:
            amount_lourd, amount_voiture, amount_velo, amount_pieton = self.get_amount_of_traffic_for_day(date).values()
            t["lourd"].append(amount_lourd)
            t["voiture"].append(amount_voiture)
            t["velo"].append(amount_velo)
            t["pieton"].append(amount_pieton)
            t["labels"].append(f"{weekdays[datetime.datetime.strptime(date[:10], '%Y-%m-%d').weekday()]} {datetime.datetime.strptime(date[:10], '%Y-%m-%d').strftime('%d-%m-%y')}")

        return t
    
    def get_cumulative_street_traffic_over_time(self, start_date: str, end_date: str) -> dict:
        """Calcule le traffic de la rue pour chaque jour de la période donnée en utilisant la méthode get_amount_of_traffic_for_day.
        start_date et end_date doivent être au format ISO (2024-01-05T15:00:00.000Z)"""
        number_of_days = (datetime.datetime.strptime(end_date[:10], '%Y-%m-%d') - datetime.datetime.strptime(start_date[:10], '%Y-%m-%d')).days
        t = {"lourd": [], "voiture": [], "velo": [], "pieton": [], "labels": []}
        datelist = []

        for i in range(number_of_days + 1):
            datelist.append((datetime.datetime.strptime(start_date[:10], '%Y-%m-%d') + datetime.timedelta(days=i)).isoformat() + ".000Z")

        weekdays = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        sum_lourd, sum_voiture, sum_velo, sum_pieton = 0, 0, 0, 0

        for date in datelist:
            amount_lourd, amount_voiture, amount_velo, amount_pieton = self.get_amount_of_traffic_for_day(date).values()
            sum_lourd += amount_lourd
            sum_voiture += amount_lourd + amount_voiture
            sum_velo += amount_lourd + amount_voiture + amount_velo
            sum_pieton += amount_lourd + amount_voiture + amount_velo + amount_pieton
            t["lourd"].append(sum_lourd)
            t["voiture"].append(sum_voiture)
            t["velo"].append(sum_velo)
            t["pieton"].append(sum_pieton)
            t["labels"].append(f"{weekdays[datetime.datetime.strptime(date[:10], '%Y-%m-%d').weekday()]} {datetime.datetime.strptime(date[:10], '%Y-%m-%d').strftime('%d-%m-%y')}")

        return t
    
    def get_speed_proportions(self, start_date: str, end_date: str) -> dict:
        """Retourne la proportion de véhicules qui roulent à une certaine tranche de vitesse.
        Retourne un dictionnaire avec les clés "0-5", "5-10", ... "110-115", "120+" et les valeurs sont des float de sommes de proportions."""
        db = get_db()
        data = db.execute('SELECT * FROM vitesse WHERE rue_id=? AND date BETWEEN ? AND ?', (self.street_id, start_date, end_date)).fetchall()
        t = {}
        for i in range(0, 121, 5):
            t[f"{i}-{i+5} km/h"] = 0
        t["120+ km/h"] = 0

        max_proportion = 0

        for proportion in data:
            if proportion["tranche_de_vitesse"] == 0:
                continue
            if proportion["tranche_de_vitesse"] == 120:
                t["120+ km/h"] += proportion["proportion"]
                continue
            t[f"{proportion['tranche_de_vitesse']}-{proportion['tranche_de_vitesse']+5} km/h"] += proportion["proportion"]
            max_proportion = max(max_proportion, t[f"{proportion['tranche_de_vitesse']}-{proportion['tranche_de_vitesse']+5} km/h"])

        # normalisation
        if max_proportion == 0:
            return t
        
        for key in t:
            t[key] = round((t[key] / max_proportion) * 100, 2)

        return t

    def get_street_coordinates(self) -> str:
        """Retourne les coordonnées de la rue.
        returns as a string "latitude,longitude"
        """
        db = get_db()
        data = db.execute('SELECT polyline FROM rue WHERE rue_id=?', (self.street_id,)).fetchone()
        return data["polyline"]
