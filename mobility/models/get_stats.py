from mobility.db import get_db

def get_entry_list():
    db = get_db()
    return db.execute('''
                      SELECT "ville" AS table_name, COUNT(*) AS number_of_entries FROM ville UNION ALL 
                      SELECT "rue" AS table_name, COUNT(*) AS number_of_entries FROM rue UNION ALL 
                      SELECT "vitesse" AS table_name, COUNT(*) AS number_of_entries FROM vitesse UNION ALL 
                      SELECT "v85" AS table_name, COUNT(*) AS number_of_entries FROM v85 UNION ALL 
                      SELECT "traffic" AS table_name, COUNT(*) AS number_of_entries FROM traffic
                      ''')

def get_number_of_streets_by_city():
    db = get_db()
    return db.execute('SELECT ville.nom AS city_name, COUNT(rue.nom) AS number_of_streets FROM rue JOIN ville ON rue.code_postal = ville.code_postal GROUP BY ville.nom')

def get_most_cyclable_cities():
    db = get_db()
    # ça j'ai pas su faire