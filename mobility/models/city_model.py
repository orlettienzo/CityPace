from mobility.db import get_db

def get_city_list():
    """Retourne une liste de toutes les villes dans la base de données, ordonnées par code postal"""
    db = get_db()
    return db.execute('SELECT * FROM ville ORDER BY code_postal')

def search_by_postal_code(postal_code: int) -> "City":
    """Retourne une liste de toutes les villes dans la base de données 
    qui ont un code postal égal à celui passé en paramètre"""
    db = get_db()
    rawdata = db.execute('SELECT * FROM ville WHERE code_postal=?', (postal_code,)).fetchone()
    return City(rawdata[1], rawdata[2], rawdata[0])

class City:
    """Classe représentant une ville. Elle possède un nom, une population et un code postal."""
    def __init__(self, name, population, postal_code=None):
        self.name = name
        self.population = population
        self.postal_code = postal_code

    def delete(self):
        """Supprime la ville de la base de données."""
        db = get_db()
        db.execute("DELETE FROM ville WHERE code_postal=?", (self.postal_code,))
        db.commit()

    def add(self):
        """Sauvegarde la ville dans la base de données."""
        db = get_db()
        db.execute("INSERT INTO ville(code_postal,nom, population ) VALUES(?, ?, ?)", ( self.postal_code,self.name, self.population))
        db.commit()

    def get_city_traffic_proportions(self) -> dict:
        """Retourne la proportion de chaque type de vehicule dans la ville."""
        db = get_db()
        # get list of streets in the city
        streets = db.execute('SELECT * FROM rue WHERE code_postal=?', (self.postal_code,)).fetchall()
        # from traffic table get the number of each type of vehicle for each street
        traffic = []
        for street in streets:
            traffic.append(db.execute('SELECT * FROM traffic WHERE rue_id=?', (street["rue_id"],)).fetchall())

        # calculate the purcentage of each type of vehicle
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
        return {"lourd": (lourd/total) * 100, "voiture": (voiture/total) * 100, "velo": (velo/total) * 100, "pieton": (pieton/total) * 100}


    @staticmethod
    def get(postal_code: int):
        """Retourne une ville de la base de données qui a le code postal passé en paramètre."""
        db = get_db()
        data = db.execute('SELECT * FROM ville WHERE code_postal=?', (postal_code,)).fetchone()

        if data is None:
            return None
        return City(data["nom"], data["population"], data["code_postal"])
