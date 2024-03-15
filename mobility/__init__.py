import os
import sqlite3
from flask import Flask, render_template, request
from flask_executor import Executor
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from mobility.models.appdata_model import db_populated
from mobility.models.get_stats import get_entry_list, get_number_of_streets_by_city, get_most_cyclable_cities
import mobility.csv_converter
from . import db, city, street, requests


def create_app(test_config=None) -> Flask:
    """Création et configuration de l'application. 'L'usine de l'application' 
    Retourne une instance de l'application configurée.
    """

    # initialisation des variables
    app = Flask(__name__, instance_relative_config=True)
    executor = Executor(app) # pour le traitement multithread
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    )

    # configuration selon si on est en mode test ou non
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.root_path, 'db.sqlite'),
        )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    def populate():
        mobility.csv_converter.populate_db()

    
    # chargement des blueprints
    app.register_blueprint(city.bp)
    app.register_blueprint(street.bp)
    app.register_blueprint(requests.bp)

    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/street', endpoint='street_index')
    app.add_url_rule('/request', endpoint='request_index')


    # chargement des routes
    @app.route('/about')
    def about() -> str:
        """Page 'À propos' du site."""
        return render_template('about.html')

    @app.route('/enzo')
    def enzo() -> str:
        """Page perso d'Enzo."""
        return render_template('enzo.html')

    @app.route('/tom')
    def tom() -> str:
        """Page perso de Tom."""
        return render_template('tom.html')

    @app.route('/nicolas')
    def nicolas() -> str:
        """Page perso de Nicolas."""
        return render_template('nicolas.html')

    @app.route('/johannes')
    def johannes() -> str:
        """Page perso de Johannes."""
        return render_template('johannes.html')

    @app.route('/liam')
    def liam() -> str:
        """Page perso de Liam."""
        return render_template('liam.html')

    @app.route('/robots.txt')
    def robots() -> str:
        """Page 'robots.txt' du site."""
        return 'User-agent: *\nDisallow: /'

    @app.route('/statistics')
    def statistics() -> str:
        """Page de statistiques."""
        if db_populated():
            entry_list = get_entry_list()
            number_of_streets_by_city = get_number_of_streets_by_city()
            most_cyclable_cities = get_most_cyclable_cities()
            return render_template("db_statistics.html", done=True, entry_list=entry_list, number_of_streets_by_city=number_of_streets_by_city, most_cyclable_cities=most_cyclable_cities)
        return render_template("db_statistics.html", done=False)

    @app.route('/resetdb', methods=['POST'])
    @limiter.limit("1/minute")
    def populate_task() -> str:
        """Permet de réinitialiser la base de données du site."""
        data = request.get_json()
        received_secret = data.get('secret')

        with open('mobility/secret.txt', 'r', encoding='utf-8') as file:
            secret = file.read().strip()

        if received_secret == secret:
            # initialisation de la base de données
            with app.app_context():
                db.init_db()
            executor.submit_stored('populate', populate)
            executor.futures.pop('populate')
            return 'Populating the database...'
        return 'nope'

    @app.route('/progress')
    def progress() -> str:
        """Retourne le pourcentage de progression de la réinitialisation de la base de données si vous avez de la chance."""
        # progress variable from mobility.csv_converter
        return f"{round(mobility.csv_converter.progress/18048*100, 1)}% done."

    @app.errorhandler(404)
    def page_not_found(e) -> str:
        """Page 404."""
        return render_template('404.html'), 404

    @app.errorhandler(429)
    def ratelimit_handler(e) -> str:
        """Page 429."""
        return render_template('429.html'), 429

    return app
