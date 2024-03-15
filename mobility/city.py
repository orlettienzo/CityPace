from flask import Blueprint, render_template
from mobility.models.city_model import get_city_list
from mobility.models.appdata_model import db_populated


bp = Blueprint('city', __name__)

# Define the routes code
@bp.route('/')
def city_list() -> str:
    """Page d'accueil."""
    if db_populated():
        cities = get_city_list()
        return render_template("index.html", done=True, cities=cities)
    return render_template("index.html", done=False)
