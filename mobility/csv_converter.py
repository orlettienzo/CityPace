import os
import csv
import ast
import sqlite3
from flask import current_app, g
# import mobility.city
# import mobility.street
import mobility.models.city_model
import mobility.models.street_model
import mobility.models.speed_model
import mobility.models.v85_model
import mobility.models.trafic_model
import requests

def discord_notify(message):
    url = "https://discord.com/api/webhooks/1212030126792122430/WoBcKMxVkfSPG-lYdrYQ0UyRDt8l2hr1m8pJHlJ-TmFgDIfz6Nwcu69jWS5DAjOnbXpX"
    data = {
        "content": message
    }
    requests.post(url, data=data)


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

progress = 0

def populate_db():
    global progress
    previous_city_code_postal = 0
    previous_street_id = 0
    path = os.path.join(os.path.dirname(__file__), "ugly_csv.csv")
    with open(path, "r", encoding="utf-8") as file:
        print("populating database with ugly_csv.csv...")
        discord_notify("populating database with ugly_csv.csv...")

        reader = csv.DictReader(file)

        for row in reader:
            if reader.line_num % 1000 == 0:
                print(f"{reader.line_num}/18048 lines processed")
                discord_notify(f"{reader.line_num}/18048 lines processed")

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
                speed = mobility.models.speed_model.Speed(row["rue_id"], row["date"], index_tranche_de_vitesse*5, t[index_tranche_de_vitesse])
                speed.add()

            # v85
            # estimation de la limite de vitesse qui est respectée par 85% des usagers de la route (15% des usagers dépassent cette vitesse). Cette valeur est absente si aucune usagers n'a été observé.
            t.sort()
            somme_cumulative = 0
            limite_vitesse = 0
            for proportion in t:
                somme_cumulative += proportion
                if somme_cumulative >= 0.85:
                    limite_vitesse = proportion
                    break
            
            v85 = mobility.models.v85_model.v85(row["rue_id"], row["date"], limite_vitesse)
            v85.add()

            # trafic
            traffic_dict = {"lourd":round(float(row["lourd"])), "voiture":round(float(row["voiture"])), "velo":round(float(row["velo"])), "pieton":round(float(row["pieton"]))}

            for type_vehicule, nb_vehicules in traffic_dict.items():
                trafic = mobility.models.trafic_model.Trafic(row["rue_id"], row["date"], type_vehicule, nb_vehicules)
                trafic.add()

            
            
    print("done!")
    discord_notify("done!")
