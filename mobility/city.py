from flask import (Blueprint, render_template, request, redirect, url_for)
from mobility.models.city_model import get_city_list, search_by_postal_code, City

bp = Blueprint('city', __name__)

# Define the routes code
@bp.route('/')
def city_list():
    cities = get_city_list()
    return render_template("index.html", cities=cities)

@bp.route("/create", methods=["POST"])
def city_create(name:str, population:int, postal_code:int):
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
    city = City(name, population, postal_code)
    city.add()
    # return redirect(url_for("city.city_list"))
    # return redirect("/")

@bp.route("/delete/<int:postal_code>")
def city_delete(postal_code):
    city = City.get(postal_code)
    if city:
        city.delete()
    return redirect(url_for("city.city_list"))
