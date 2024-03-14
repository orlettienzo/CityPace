from flask import (Blueprint, redirect, render_template, request, url_for)
from mobility.models.street_model import get_street_list,search_street_id, Street
import sqlite3
import mobility.csv_converter
from mobility.models.appdata_model import db_populated

bp = Blueprint('street', __name__)

# Define the routes code
@bp.route('/street')
def street_list():
    """Page des rues."""
    if db_populated():
        streets = get_street_list()
        return render_template("street.html", done=True, streets=streets)
    return render_template("street.html", done=False)
