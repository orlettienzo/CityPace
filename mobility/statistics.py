from flask import (Blueprint, render_template, request, redirect, url_for)
from mobility.models.get_stats import get_entry_list, get_number_of_streets_by_city, get_most_cyclable_cities
import sqlite3
from mobility.models.appdata_model import get_db_populated

bp = Blueprint('statistics', __name__)

@bp.route('/statistics')
def serve_statistics():
    if get_db_populated():
        try:
            entry_list = get_entry_list()
            number_of_streets_by_city = get_number_of_streets_by_city()
            # most_cyclable_cities = get_most_cyclable_cities() # enlever le commentaire quand la fonction sera implémentée
        except sqlite3.OperationalError:
            return render_template("statistics.html", done=False)
        return render_template("statistics.html", done=True, entry_list=entry_list, number_of_streets_by_city=number_of_streets_by_city) #, most_cyclable_cities=most_cyclable_cities)
    return render_template("statistics.html", done=False)
