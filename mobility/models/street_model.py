from mobility.db import get_db
import datetime

def get_street_list():
    db = get_db()
    return db.execute('SELECT rue.rue_id, rue.nom, rue.code_postal, ville.nom AS city_name FROM rue JOIN ville ON rue.code_postal = ville.code_postal ORDER BY rue.code_postal')

def search_street_id(street_id: int):
    db = get_db()
    data = db.execute('SELECT * FROM rue WHERE rue_id=?', (street_id,)).fetchone()
    return Street(data[1], data[2], data[0])

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

    def get_street_traffic_proportions_by_week_day(self) -> dict:
        db = get_db()
        data = db.execute('SELECT * FROM traffic WHERE rue_id=?', (self.street_id,)).fetchall()
        t = {}
        for traffic in data:
            try:
                print(traffic["date"][:10])
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
            t[key]["lourd"] = (t[key]["lourd"]/total) * 100
            t[key]["voiture"] = (t[key]["voiture"]/total) * 100
            t[key]["velo"] = (t[key]["velo"]/total) * 100
            t[key]["pieton"] = (t[key]["pieton"]/total) * 100


        return t

    @staticmethod
    def get(street_id: int):
        db = get_db()
        data = db.execute('SELECT * FROM rue WHERE rue_id=?', (street_id,)).fetchone()

        if data is None:
            return None
        return Street(data["nom"], data["name"], data["rue_id"])
