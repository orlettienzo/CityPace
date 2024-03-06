from flask import (Blueprint, render_template, request, redirect, url_for)
from mobility.models.city_model import get_city_list, search_by_postal_code, City
import sqlite3
from mobility.models.appdata_model import get_db_populated


bp = Blueprint('city', __name__)

# Define the routes code
@bp.route('/')
def city_list():
    if get_db_populated():
        try:
            cities = get_city_list()
        except sqlite3.OperationalError:
            return render_template("index.html", done=False)
        return render_template("index.html", done=True, cities=cities)
    return render_template("index.html", done=False)

@bp.route("/create", methods=["POST"])
def city_create(name:str, population:int, postal_code:int):

    # code pour ajouter une ville à partir du formulaire

    # postal_code = request.form["postal_code"]
    # if len(postal_code) != 4:
    #     return redirect(url_for("city.city_list"))
    # if not search_by_postal_code(int(postal_code)):
    #     name = request.form["name"]
    #     if 20< len(name) < 3:
    #         return redirect(url_for("city.city_list"))
    #     population = request.form["population"]
        # city = City(name, population, postal_code)
        # city.add()
    # return redirect(url_for("city.city_list"))
    # return redirect("/")

    # code pour simplement ajouter une ville 

    city = City(name, population, postal_code)
    city.add()

# code pour supprimer une ville

# @bp.route("/delete/<int:postal_code>")
# def city_delete(postal_code):
#     city = City.get(postal_code)
#     if city:
#         city.delete()
#     return redirect(url_for("city.city_list"))
