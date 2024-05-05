from flask import Blueprint, render_template
from mobility.models.city_model import get_city_list, City
from mobility.models.street_model import get_street_list_for_city, Street
from mobility.models.appdata_model import db_populated

bp = Blueprint('requests', __name__)

@bp.route('/request')
@bp.route('/request/<int:city_id>')
@bp.route('/request/<int:city_id>/')
@bp.route('/request/<int:city_id>/<int:street_id>')
@bp.route('/request/<int:city_id>/<int:street_id>/')
@bp.route('/request/<int:city_id>/<int:street_id>/<start_date>')
@bp.route('/request/<int:city_id>/<int:street_id>/<start_date>/<end_date>')
def request_page(city_id: int = None, street_id: int = None, start_date: str = None, end_date: str = None) -> str:
    """Page de requête."""
    print(f"\033[92mGot request for {city_id=}, {street_id=}, {start_date=}, {end_date=}\033[0m")
    if not db_populated():
        return render_template("db_request.html", done=False)

    if street_id is not None:
        city_obj = City.get(city_id)
        street_obj = Street.get(street_id)
        location_for_url = f"/{street_obj.polyline.split(',')[0]}/{street_obj.polyline.split(',')[1]}/18"
        if start_date is None:
            selected_time_span = street_obj.get_street_time_span()
        elif end_date is None:
            selected_time_span = {"start_date": start_date, "end_date": street_obj.get_street_time_span()["end_date"]}
        else:
            selected_time_span = {"start_date": start_date, "end_date": end_date}
        return render_template("db_request.html",
                               done=True,
                               cities=get_city_list(),
                               selected_city=city_id,
                               selected_street=street_id,
                               city_traffic_proportions=city_obj.get_city_traffic_proportions(),
                               city_name=city_obj.name,
                               streets=get_street_list_for_city(city_id),
                               street_traffic_proportions_by_week_day=street_obj.get_street_traffic_proportions_by_week_day(),
                               street_traffic_proportions_for_period=street_obj.get_street_traffic_proportions_for_period(selected_time_span["start_date"], selected_time_span["end_date"]),
                               street_traffic_over_time=street_obj.get_street_traffic_over_time(selected_time_span["start_date"], selected_time_span["end_date"]),
                               street_cumulative_traffic_over_time=street_obj.get_cumulative_street_traffic_over_time(selected_time_span["start_date"], selected_time_span["end_date"]),
                               street_time_span=street_obj.get_street_time_span(),
                               selected_time_span=selected_time_span,
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
