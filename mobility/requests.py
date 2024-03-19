from flask import Blueprint, render_template, request
from mobility.models.city_model import get_city_list, search_by_postal_code
from mobility.models.street_model import search_street_id, get_street_list_for_city
from mobility.models.appdata_model import db_populated

bp = Blueprint('requests', __name__)

@bp.route('/request')
def request_page() -> str:
    """Page de requête."""
    if db_populated():
        return render_template("db_request.html", done=True, cities=get_city_list())
    # si la base de données n'est pas encore peuplée
    return render_template("db_request.html", done=False)

@bp.route("/get_stats", methods=["POST"])
def get_stats():
    """Retourne les statistiques demandées à partir de la page de requête."""
    if not db_populated(): # au cas où la base de données n'est pas encore peuplée
        return render_template("db_request.html", done=False)
    # on récupère les valeurs des champs de la page de requête
    selected_city = int(request.form["ville"])
    try:
        selected_street = int(request.form["rue"])
    except KeyError:
        selected_street = 0

    if selected_city == 0:
        # si aucune ville n'est sélectionnée
        return render_template("db_request.html", done=True, cities=get_city_list())

    if selected_street == 0:
        # 0 = toutes les rues, on retourne que les statistiques pour la ville sélectionnée
        return render_template(
            "db_request.html", 
            done=True,
            cities=get_city_list(),
            selected_city=selected_city, # pour que la ville sélectionnée reste sélectionnée
            city_data=search_by_postal_code(selected_city).get_city_traffic_proportions(),
            streets=get_street_list_for_city(selected_city))

    # une ville et une rue sont sélectionnées
    # on retourne donc les statistiques pour la rue sélectionnée
    return render_template(
        "db_request.html",
        done=True,
        cities=get_city_list(),
        selected_city=selected_city, # pour que la ville sélectionnée reste sélectionnée
        selected_street=selected_street, # pour que la rue sélectionnée reste sélectionnée
        city_data=search_by_postal_code(selected_city).get_city_traffic_proportions(),
        streets=get_street_list_for_city(selected_city),
        street_data=search_street_id(selected_street).get_street_traffic_proportions_by_week_day())
