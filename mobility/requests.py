from flask import Blueprint, render_template, request
from mobility.models.city_model import get_city_list, search_by_postal_code
from mobility.models.street_model import get_street_list,search_street_id
from mobility.models.appdata_model import db_populated

bp = Blueprint('requests', __name__)

@bp.route('/request')
def request_page() -> str:
    """Page de requête."""
    if db_populated():
        cities = get_city_list()
        streets = get_street_list()
        return render_template("db_request.html", done=True, cities=cities, streets=streets)
    return render_template("db_request.html", done=False)

@bp.route("/get_stats", methods=["POST"])
def get_stats():
    """Retourne les statistiques demandées à partir de la page de requête."""
    city = int(request.form["ville"])
    street = int(request.form["rue"])
    if street == 0: # 0 = toutes les rues
        data = search_by_postal_code(city)
        return data.get_city_traffic_proportions()

    data = search_street_id(street)
    return data.get_street_traffic_proportions_by_week_day()
