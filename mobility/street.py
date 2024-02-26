from flask import (Blueprint, redirect, render_template, request, url_for)

from mobility.models.street import Street
from mobility.models.street import get_street_list,search_street_id

bp = Blueprint('street', __name__)

# Define the routes code
@bp.route('/street')
def street_list():
    streets = get_street_list()
    return render_template("street.html", streets=streets)

@bp.route("/create_street", methods=["POST"])
def street_create():
    street_id = request.form["street_id"]
    if not search_street_id(int(street_id)):
        name = request.form["name"]
        postal_code = request.form["postal_code"]
        street = Street(name, postal_code, street_id)
        street.save()
    return redirect(url_for("street.street_list"))

@bp.route("/delete/<int:street_id>")
def street_delete(street_id):
    street = Street.get(street_id)
    if street:
        street.delete()
    return redirect(url_for("street.street_list"))
