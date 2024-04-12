"""Convertit le fichier ugly_csv.csv en données exploitables pour la base de données.
Ne pas exécuter ce fichier! Utilisez le fichier reset_local_db.py ou reset_online_db.py.
"""

import os
import time
import csv
import ast
import mobility.models.city_model
import mobility.models.street_model
import mobility.models.speed_model
import mobility.models.v85_model
import mobility.models.traffic_model
from mobility.utils.db import get_db


progress = 0
done = False
runtime = 0

def populate_db() -> None:
    """Peuple la base de données avec le fichier ugly_csv.csv."""
    global progress, done, runtime
    print("Peuplement de la base de données avec le fichier ugly_csv.csv...")

    start_time = time.time()

    # remove db_populated value from the database
    db = get_db()
    db.execute("DELETE FROM appdata WHERE data_id=1")
    db.commit()

    POPULATION = {"bruxelles":1_222_657,
              "grobbendonk":11_249,
              "liege":195_278,
              "namur":114_007,
              "jambes":20_125,
              "charleroi":202_267,
              "courtrai":77_741,
              "beveren":50_281,
              "herzele":17_723,
              }

    previous_city_code_postal = 0
    previous_street_id = 0
    path = os.path.join(os.path.dirname(__file__), "ugly_csv.csv")

    cities = []
    streets = []
    speeds = []
    v85s = []
    traffics = []

    with open(path, "r", encoding="utf-8") as file:
        print("csv file opened")

        reader = csv.DictReader(file)

        for row in reader:
            if reader.line_num % 1000 == 0:
                print(f"{reader.line_num}/18048 lignes traitées")

            progress = reader.line_num

            # villes
            city = mobility.models.city_model.City(row["nom_de_ville"].capitalize(), POPULATION[row["nom_de_ville"].lower()], row["code_postal"])
            if row["code_postal"] != previous_city_code_postal:
                if row["nom_de_ville"] == "Liege":
                    city.name = "Liège"
                cities.append((city.postal_code, city.name, city.population))

            previous_city_code_postal = row["code_postal"]

            # rues
            street = mobility.models.street_model.Street(row["nom_de_rue"], row["code_postal"], row["rue_id"])
            
            if row["rue_id"] != previous_street_id:
                if row["nom_de_rue"] == "Condereef":
                    street.name = "Condédreef"
                if row["nom_de_rue"] == "Montagne SainteBarbe":
                    street.name = "Montagne Sainte Barbe"
                if row["nom_de_rue"] == "Avenue prince de Liege":
                    street.name = "Avenue Prince de Liège"
                street.set_street_polyline_latlng()
                streets.append((street.street_id, street.name, street.postal_code, street.polyline))
            previous_street_id = row["rue_id"]

            # vitesse
            t = row["histogramme_0_a_120plus"]
            t = ast.literal_eval(t)
            for index_tranche_de_vitesse in range(len(t)):
                if t[index_tranche_de_vitesse] == 0:
                    continue
                speed = mobility.models.speed_model.Speed(row["rue_id"], row["date"], index_tranche_de_vitesse*5, t[index_tranche_de_vitesse])
                speeds.append((speed.rue_id, speed.date, speed.tranche_de_vitesse, speed.proportion))

            # v85
            if row["v85"] != "":
                v85 = mobility.models.v85_model.v85(row["rue_id"], row["date"], row["v85"])
                v85s.append((v85.rue_id, v85.date, v85.v85))

            # trafic
            traffic = mobility.models.traffic_model.Traffic(row["rue_id"], row["code_postal"], row["date"], round(float(row["lourd"])), round(float(row["voiture"])), round(float(row["velo"])), round(float(row["pieton"])))
            traffics.append((traffic.rue_id, traffic.code_postal, traffic.date, traffic.lourd, traffic.voiture, traffic.velo, traffic.pieton))

    print("Peuplement de la base de données...")

    mobility.models.city_model.City.bulk_add(cities)
    mobility.models.street_model.Street.bulk_add(streets)
    mobility.models.speed_model.Speed.bulk_add(speeds)
    mobility.models.v85_model.v85.bulk_add(v85s)
    mobility.models.traffic_model.Traffic.bulk_add(traffics)

    # insertion d'une valeur dans la base de données pour indiquer que la base de données est entièrement peuplée
    db = get_db()
    db.execute("INSERT INTO appdata(data_id, data_name, data_value) VALUES(?, ?, ?)", (1, "db_populated", 1))
    db.commit()

    runtime = round(time.time() - start_time, 2)
    print(f"Terminé en {runtime} secondes")

