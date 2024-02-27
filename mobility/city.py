from flask import (Blueprint, render_template, request, redirect, url_for)
from mobility.models.city import get_city_list, search_by_postal_code, City
import requests

bp = Blueprint('city', __name__)

# Define the routes code
@bp.route('/')
def city_list():
    cities = get_city_list()
    return render_template("index.html", cities=cities)

@bp.route("/create", methods=["POST"])
def city_create():
    postal_code = request.form["postal_code"]
    if not search_by_postal_code(int(postal_code)):
        name = request.form["name"]
        population = request.form["population"]
        city = City(name, population, postal_code)
        city.save()

    ip = request.remote_addr
    data = {
        "content": f"{name} - {population} - {postal_code} created by {ip}"
    }
    requests.post("https://discord.com/api/webhooks/1212030126792122430/WoBcKMxVkfSPG-lYdrYQ0UyRDt8l2hr1m8pJHlJ-TmFgDIfz6Nwcu69jWS5DAjOnbXpX", json=data, timeout=10)
    return redirect(url_for("city.city_list"))

@bp.route("/delete/<int:postal_code>")
def city_delete(postal_code):
    city = City.get(postal_code)
    if city:
        city.delete()
    return redirect(url_for("city.city_list"))
