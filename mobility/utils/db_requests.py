from flask import Blueprint, render_template, request
from mobility.models.city_model import get_city_list, City
from mobility.models.street_model import get_street_list_for_city, Street
from mobility.models.appdata_model import db_populated

bp = Blueprint('requests', __name__)

@bp.route('/request')
@bp.route('/request/<int:city_id>')
@bp.route('/request/<int:city_id>/<int:street_id>')
@bp.route('/request/<int:city_id>/<int:street_id>/<start_date>')
@bp.route('/request/<int:city_id>/<int:street_id>/<start_date>/<end_date>')
def request_page(city_id: int = None, street_id: int = None, start_date: str = None, end_date: str = None) -> str:
    """Page de requête."""
    print(f"GOT {city_id=} {street_id=} {start_date=} {end_date=}") # debug
    if not db_populated():
        return render_template("db_request.html", done=False)

    if street_id is not None:
        print("STREET_ID is not None")
        city_obj = City.get(city_id)
        street_obj = Street.get(street_id)
        location_for_url = f"/{street_obj.polyline.split(',')[0]}/{street_obj.polyline.split(',')[1]}/18"
        return render_template("db_request.html",
                               done=True,
                               cities=get_city_list(),
                               selected_city=city_id,
                               selected_street=street_id,
                               city_traffic_proportions=city_obj.get_city_traffic_proportions(),
                               city_name=city_obj.name,
                               streets=get_street_list_for_city(city_id),
                               street_traffic_proportions_by_week_day=street_obj.get_street_traffic_proportions_by_week_day(),
                               street_traffic_proportions_for_period=street_obj.get_street_traffic_proportions_for_period("2024-01-07T03:00:00.000Z", "2024-01-07T10:00:00.000Z"),
                               street_name=street_obj.name,
                               location=location_for_url)
    if city_id is not None:
        city_obj = City.get(city_id)
        return render_template("db_request.html",
                               done=True,
                               cities=get_city_list(),
                               selected_city=city_id,
                               city_traffic_proportions=city_obj.get_city_traffic_proportions(),
                               city_name=city_obj.name,
                               streets=get_street_list_for_city(city_id))
    
    return render_template("db_request.html", done=True, cities=get_city_list())

# @bp.route('/new_get_stats/<str:city_name>/<str:street_name>')
# @bp.route('/request/<str:city_name>/<str:street_name>/<str:start-date>/<str:end-date>')
# def new_get_stats(city_name: str, street_name: str, start_date: str = None, end_date: str = None) -> str:
#     if not db_populated():
#         return render_template("db_request.html", done=False)


# @bp.route("/get_stats", methods=["POST"])
def get_stats():
    """Retourne les statistiques demandées à partir de la page de requête."""
    if not db_populated(): # au cas où la base de données n'est pas encore peuplée
        return render_template("db_request.html", done=False)
    # on récupère les valeurs des champs de la page de requête
    # try:
    selected_city = int(request.form["ville"])
    # except KeyError:
    #     selected_city = 0

    try:
        selected_street = int(request.form["rue"])
    except KeyError:
        selected_street = 0

    if selected_city == 0:
        # si aucune ville n'est sélectionnée
        return render_template("db_request.html", done=True, cities=get_city_list())

    if selected_street == 0:
        # 0 = toutes les rues, on retourne que les statistiques pour la ville sélectionnée
        city_obj = City.get(selected_city) # on récupère l'objet City correspondant à la ville sélectionnée
        return render_template(
            "db_request.html", 
            done=True,
            cities=get_city_list(),
            selected_city=selected_city, # pour que la ville sélectionnée reste sélectionnée
            city_traffic_proportions=city_obj.get_city_traffic_proportions(),
            city_name=city_obj.name,
            streets=get_street_list_for_city(selected_city))

    # une ville et une rue sont sélectionnées
    # on retourne donc les statistiques pour la rue sélectionnée
    city_obj = City.get(selected_city)
    street_obj = Street.get(selected_street)
    location_for_url = f"/{street_obj.polyline.split(',')[0]}/{street_obj.polyline.split(',')[1]}/18"
    return render_template(
        "db_request.html",
        done=True,
        cities=get_city_list(),
        selected_city=selected_city, # pour que la ville sélectionnée reste sélectionnée
        selected_street=selected_street, # pour que la rue sélectionnée reste sélectionnée
        city_traffic_proportions=city_obj.get_city_traffic_proportions(),
        city_name=city_obj.name,
        streets=get_street_list_for_city(selected_city),
        street_traffic_proportions_by_week_day=street_obj.get_street_traffic_proportions_by_week_day(),
        street_traffic_proportions_for_period=street_obj.get_street_traffic_proportions_for_period("2024-01-07T03:00:00.000Z", "2024-01-07T10:00:00.000Z"),
        street_name=street_obj.name,
        location=location_for_url)
