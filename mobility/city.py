from flask import (
      Blueprint, render_template
)

bp = Blueprint('city', __name__)

# Define the routes code
@bp.route('/')
def city_list():
    cities = [(5000, "Namur", 496891), (1000, "Bruxelles", 1290000), (9000, "Gent", 262219), (2000, "Anvers", 525935)]
    return render_template("base.html", cities=cities)