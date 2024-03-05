from flask import (Blueprint, redirect, render_template, request, url_for)
from mobility.models.street_model import get_street_list,search_street_id, Street
import sqlite3
import mobility.csv_converter

bp = Blueprint('street', __name__)

# Define the routes code
@bp.route('/street')
def street_list():
    if mobility.csv_converter.done:
        try:
            streets = get_street_list()
        except sqlite3.OperationalError:
            return render_template("street.html", done=False)
        return render_template("street.html", done=True, streets=streets)
    return render_template("street.html", done=False)

@bp.route("/create_street", methods=["POST"])
def street_create(name:str, postal_code:int, street_id:int):
    # street_id = request.form["street_id"]
    # if not search_street_id(int(street_id)):
    #     name = request.form["name"]
    #     postal_code = request.form["postal_code"]
    #     street = Street(name, postal_code, street_id)
    #     street.add()
    street = Street(name, postal_code, street_id)
    street.add()
    # return redirect(url_for("street.street_list"))

# @bp.route("/delete/<int:street_id>")
# def street_delete(street_id):
#     street = Street.get(street_id)
#     if street:
#         street.delete()
#     return redirect(url_for("street.street_list"))
