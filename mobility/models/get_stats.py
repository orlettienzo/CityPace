from mobility.db import get_db
import sqlite3

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
    return db.execute('SELECT ville.nom AS city_name, SUM(traffic.velo) AS number_of_cyclists FROM traffic JOIN rue ON traffic.rue_id = rue.rue_id JOIN ville ON rue.code_postal = ville.code_postal GROUP BY ville.nom ORDER BY number_of_cyclists DESC')
