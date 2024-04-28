from mobility.utils.db import get_db
import sqlite3
from mobility.utils.moon_utils import age, phase, MoonPhase
from datetime import datetime

def get_entry_list() -> sqlite3.Cursor:
    """Retourne la liste du nombre d'entrées dans chaque table de la base de données sous la forme d'un curseur sqlite3."""
    db = get_db()
    return db.execute('''
                      SELECT "ville" AS table_name, COUNT(*) AS number_of_entries FROM ville UNION ALL 
                      SELECT "rue" AS table_name, COUNT(*) AS number_of_entries FROM rue UNION ALL 
                      SELECT "vitesse" AS table_name, COUNT(*) AS number_of_entries FROM vitesse UNION ALL 
                      SELECT "v85" AS table_name, COUNT(*) AS number_of_entries FROM v85 UNION ALL 
                      SELECT "traffic" AS table_name, COUNT(*) AS number_of_entries FROM traffic
                      ''')

def get_number_of_streets_by_city() -> sqlite3.Cursor:
    """Retourne le nombre de rues par ville sous la forme d'un curseur sqlite3."""
    db = get_db()
    return db.execute('SELECT ville.nom AS city_name, COUNT(rue.nom) AS number_of_streets FROM rue JOIN ville ON rue.code_postal = ville.code_postal GROUP BY ville.nom ORDER BY number_of_streets DESC')

def get_most_cyclable_cities() -> sqlite3.Cursor:
    """Retourne les villes les plus cyclables sous la forme d'un curseur sqlite3."""
    db = get_db()
    # return number of bikes per city divided by the population of the city
    return db.execute('SELECT ville.nom AS city_name, population, ROUND(SUM(traffic.velo)*1.0/population, 2) AS bikes_per_person, SUM(traffic.velo) as number_of_bikes FROM traffic JOIN rue ON traffic.code_postal = rue.code_postal JOIN ville ON rue.code_postal = ville.code_postal GROUP BY ville.nom ORDER BY bikes_per_person DESC LIMIT 5')

def get_most_traffic_streets() -> sqlite3.Cursor:
    """Retourne les rues avec le plus de véhicules par heure sous la forme d'un curseur sqlite3."""
    db = get_db()
    return db.execute('SELECT rue.nom AS street_name, SUM(traffic.voiture)+SUM(traffic.lourd)+SUM(traffic.velo)+SUM(traffic.pieton) AS vehicles_per_hour FROM traffic JOIN rue ON traffic.code_postal = rue.code_postal GROUP BY rue.nom ORDER BY vehicles_per_hour DESC LIMIT 5')

def get_bike_ratio_on_full_moon_days() -> float:
    """Retourne le ratio de cyclistes les jours de pleine lune."""
    db = get_db()
    data = db.execute('SELECT DATE(traffic.date) AS date, SUM(traffic.velo) AS number_of_cyclists FROM traffic GROUP BY DATE(traffic.date) ORDER BY number_of_cyclists DESC').fetchall()

    full_moon_bikes = 0
    other_days_bikes = 0
    full_moon_days = 0
    other_days = 0

    for row in data:
        date = datetime.strptime(row['date'], '%Y-%m-%d').date()
        bikes = row['number_of_cyclists']

        if phase(age(date)) == MoonPhase.FULL_MOON:
            full_moon_bikes += bikes
            full_moon_days += 1
        else:
            other_days_bikes += bikes
            other_days += 1

    return round((full_moon_bikes / full_moon_days) / (other_days_bikes / other_days), 2)
