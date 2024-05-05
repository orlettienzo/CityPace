from mobility.utils.db import get_db
import sqlite3

def get_city_list() -> sqlite3.Cursor:
    """Retourne une liste de toutes les villes dans la base de données, ordonnées par code postal"""
    db = get_db()
    return db.execute('SELECT * FROM ville ORDER BY code_postal')

class City:
    """Classe représentant une ville."""
    def __init__(self, name, population, postal_code=None) -> None:
        """Crée un objet City."""
        self.name = name
        self.population = population
        self.postal_code = postal_code

    def __str__(self) -> str:
        return f"{self.name} ({self.postal_code}), {self.population} habitants"

    @staticmethod
    def get(postal_code: int) -> "City":
        """Retourne une ville de la base de données qui a le code postal passé en paramètre."""
        db = get_db()
        data = db.execute('SELECT * FROM ville WHERE code_postal=?', (postal_code,)).fetchone()

        if data is None:
            return None
        return City(data[1], data[2], data[0])

    @staticmethod
    def bulk_add(cities: list) -> None:
        """Ajoute une liste de villes dans la base de données."""
        db = get_db()
        db.executemany("INSERT INTO ville(code_postal,nom, population ) VALUES(?, ?, ?)", cities)
        db.commit()

    def delete(self) -> None:
        """Supprime la ville de la base de données."""
        db = get_db()
        db.execute("DELETE FROM ville WHERE code_postal=?", (self.postal_code,))
        db.commit()

    def add(self) -> None:
        """Sauvegarde la ville dans la base de données."""
        db = get_db()
        db.execute("INSERT INTO ville(code_postal,nom, population ) VALUES(?, ?, ?)", ( self.postal_code,self.name, self.population))
        db.commit()

    def get_total_lourd(self) -> int:
        """Retourne le nombre total de véhicules lourds dans la ville."""
        db = get_db()
        streets = db.execute('SELECT * FROM rue WHERE code_postal=?', (self.postal_code,)).fetchall()
        total = 0
        for street in streets:
            total += db.execute('SELECT SUM(lourd) FROM traffic WHERE rue_id=?', (street["rue_id"],)).fetchone()[0]
        return total
    
    def get_total_voiture(self) -> int:
        """Retourne le nombre total de voitures dans la ville."""
        db = get_db()
        streets = db.execute('SELECT * FROM rue WHERE code_postal=?', (self.postal_code,)).fetchall()
        total = 0
        for street in streets:
            total += db.execute('SELECT SUM(voiture) FROM traffic WHERE rue_id=?', (street["rue_id"],)).fetchone()[0]
        return total
    
    def get_total_velo(self) -> int:
        """Retourne le nombre total de vélos dans la ville."""
        db = get_db()
        streets = db.execute('SELECT * FROM rue WHERE code_postal=?', (self.postal_code,)).fetchall()
        total = 0
        for street in streets:
            total += db.execute('SELECT SUM(velo) FROM traffic WHERE rue_id=?', (street["rue_id"],)).fetchone()[0]
        return total
    
    def get_total_pieton(self) -> int:
        """Retourne le nombre total de piétons dans la ville."""
        db = get_db()
        streets = db.execute('SELECT * FROM rue WHERE code_postal=?', (self.postal_code,)).fetchall()
        total = 0
        for street in streets:
            total += db.execute('SELECT SUM(pieton) FROM traffic WHERE rue_id=?', (street["rue_id"],)).fetchone()[0]
        return total

    def get_city_traffic_proportions(self) -> dict:
        """Calcule la proportion de chaque type de vehicule dans la ville.
        Retourne un dictionnaire avec les pourcentages de chaque type de vehicule.
        ex: {"lourd": 10, "voiture": 50, "velo": 20, "pieton": 20}
        """
        db = get_db()
        streets = db.execute('SELECT * FROM rue WHERE code_postal=?', (self.postal_code,)).fetchall()
        traffic = [] # tableau du traffic de chaque rue de la ville
        for street in streets:
            traffic.append(db.execute('SELECT * FROM traffic WHERE rue_id=?', (street["rue_id"],)).fetchall())

        # comptage du traffic total de la ville
        lourd = 0
        voiture = 0
        velo = 0
        pieton = 0
        for street in traffic:
            for vehicle in street:
                lourd += vehicle["lourd"]
                voiture += vehicle["voiture"]
                velo += vehicle["velo"]
                pieton += vehicle["pieton"]
        total = lourd + voiture + velo + pieton

        # calcul de la proportion de chaque type de vehicule
        return {"lourd": round((lourd/total) * 100, 2),
            "voiture": round((voiture/total) * 100, 2), 
            "velo": round((velo/total) * 100, 2), 
            "pieton": round((pieton/total) * 100, 2)}
    
    def get_city_traffic_proportions_for_period(self, start_date: str, end_date: str) -> dict:
        """Calcule la proportion de chaque type de vehicule dans la ville pour une période donnée.
        Retourne un dictionnaire avec les pourcentages de chaque type de vehicule.
        ex: {"lourd": 10, "voiture": 50, "velo": 20, "pieton": 20}
        """
        db = get_db()
        streets = db.execute('SELECT * FROM traffic WHERE code_postal=? AND date BETWEEN ? AND ?', (self.postal_code, start_date, end_date)).fetchall()
        traffic = []
        for street in streets:
            traffic.append(db.execute('SELECT * FROM traffic WHERE rue_id=?', (street["rue_id"],)).fetchall())

        # comptage du traffic total de la ville
        lourd = 0
        voiture = 0
        velo = 0
        pieton = 0
        for street in traffic:
            for vehicle in street:
                lourd += vehicle["lourd"]
                voiture += vehicle["voiture"]
                velo += vehicle["velo"]
                pieton += vehicle["pieton"]
        total = lourd + voiture + velo + pieton

        # calcul de la proportion de chaque type de vehicule
        return {"lourd": round((lourd/total) * 100, 2),
            "voiture": round((voiture/total) * 100, 2), 
            "velo": round((velo/total) * 100, 2), 
            "pieton": round((pieton/total) * 100, 2)}

    def get_city_time_span(self) -> dict:
        """Retourne la date de début et de fin du traffic pour la ville."""
        db = get_db()
        data = db.execute('SELECT MIN(date) AS start_date, MAX(date) AS end_date FROM traffic WHERE code_postal=?', (self.postal_code,)).fetchone()
        return {"start_date": data["start_date"], "end_date": data["end_date"]}
        
        