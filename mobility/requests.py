from flask import Blueprint, render_template, request
from mobility.models.city_model import get_city_list, search_by_postal_code
from mobility.models.street_model import get_street_list,search_street_id, get_street_list_for_city
from mobility.models.appdata_model import db_populated

bp = Blueprint('requests', __name__)

@bp.route('/request')
def request_page() -> str:
    """Page de requête."""
    if db_populated():
        return render_template("db_request.html", done=True, cities=get_city_list())
    return render_template("db_request.html", done=False)

@bp.route("/get_stats", methods=["POST"])
def get_stats():
    """Retourne les statistiques demandées à partir de la page de requête."""
    selected_city = int(request.form["ville"])
    selected_street = int(request.form["rue"])
    print(f"{selected_city=}, {selected_street=}")

    if selected_city == 0:
        return render_template("db_request.html", done=True, cities=get_city_list())
    
    if selected_street == 0: # 0 = toutes les rues
        city_data = search_by_postal_code(selected_city)
        city_data = city_data.get_city_traffic_proportions()
        return render_template(
            "db_request.html", 
            done=True,
            cities=get_city_list(),
            selected_city=selected_city,
            city_data=city_data,
            streets=get_street_list_for_city(selected_city))

    city_data = search_by_postal_code(selected_city)
    city_data = city_data.get_city_traffic_proportions()
    data = search_street_id(selected_street)
    return render_template(
        "db_request.html",
        done=True,
        cities=get_city_list(),
        selected_city=selected_city,
        selected_street=selected_street,
        city_data=city_data,
        streets=get_street_list_for_city(selected_city),
        street_data=data.get_street_traffic_proportions_by_week_day())
