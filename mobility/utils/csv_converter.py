import os
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

def populate_db() -> None:
    """Peuple la base de données avec le fichier ugly_csv.csv."""
    global progress, done
    print("Peuplement de la base de données avec le fichier ugly_csv.csv...")

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
    with open(path, "r", encoding="utf-8") as file:
        print("fichier ouvert")

        reader = csv.DictReader(file)

        for row in reader:
            if reader.line_num % 1000 == 0:
                print(f"{reader.line_num}/18048 lignes traitées")

            progress = reader.line_num

            # villes
            city = mobility.models.city_model.City(row["nom_de_ville"].capitalize(), POPULATION[row["nom_de_ville"].lower()], row["code_postal"])
            if row["code_postal"] != previous_city_code_postal:
                city.add()
            previous_city_code_postal = row["code_postal"]

            # rues
            street = mobility.models.street_model.Street(row["nom_de_rue"], row["code_postal"], row["rue_id"])
            if row["rue_id"] != previous_street_id:
                street.add()
            previous_street_id = row["rue_id"]

            # vitesse
            t = row["histogramme_0_a_120plus"]
            t = ast.literal_eval(t)
            for index_tranche_de_vitesse in range(len(t)):
                if t[index_tranche_de_vitesse] == 0:
                    continue
                speed = mobility.models.speed_model.Speed(row["rue_id"], row["date"], index_tranche_de_vitesse*5, t[index_tranche_de_vitesse])
                speed.add()

            # v85
            # vérifie s'il y a une valeur pour row["v85"]
            if row["v85"] != "":
                v85 = mobility.models.v85_model.v85(row["rue_id"], row["date"], row["v85"])
                v85.add()

            # trafic
            traffic = mobility.models.traffic_model.Traffic(row["rue_id"], row["date"], round(float(row["lourd"])), round(float(row["voiture"])), round(float(row["velo"])), round(float(row["pieton"])))
            traffic.add()

    db = get_db()
    db.execute("INSERT INTO appdata(data_id, data_name, data_value) VALUES(?, ?, ?)", (1, "db_populated", 1))
    db.commit()

    print("Terminé!")
