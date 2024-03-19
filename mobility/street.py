from flask import Blueprint, render_template
from mobility.models.street_model import get_street_list
from mobility.models.appdata_model import db_populated

bp = Blueprint('street', __name__)

@bp.route('/street')
def street_list():
    """Page des rues."""
    if db_populated():
        streets = get_street_list()
        return render_template("street.html", done=True, streets=streets)
    # si la base de données n'est pas encore peuplée
    return render_template("street.html", done=False)
