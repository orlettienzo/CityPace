import os
from flask import Flask, render_template, request
from flask_executor import Executor
import mobility.csv_converter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address





def create_app(test_config=None):
    """Création et configuration de l'application. 'L'usine de l'application' """
    
    # initialisation des variables
    app = Flask(__name__, instance_relative_config=True)
    executor = Executor(app) # pour le traitement multithread
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    )
    db_populated = False # pour savoir si la base de données a été peuplée


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


    from . import db
    db.init_app(app)

    def populate():
        mobility.csv_converter.populate_db()

    
    # chargement des blueprints
    from . import city, street, statistics
    app.register_blueprint(city.bp)
    app.register_blueprint(street.bp)
    app.register_blueprint(statistics.bp)

    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/street', endpoint='street_index')
    app.add_url_rule('/statistics', endpoint='statistics_index')


    # chargement des routes
    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/enzo')
    def enzo():
        return render_template('enzo.html')

    @app.route('/tom')
    def tom():
        return render_template('tom.html')

    @app.route('/nicolas')
    def nicolas():
        return render_template('nicolas.html')

    @app.route('/johannes')
    def johannes():
        return render_template('johannes.html')

    @app.route('/liam')
    def liam():
        return render_template('liam.html')

    @app.route('/robots.txt')
    def robots():
        return 'User-agent: *\nDisallow: /'
    
    @app.route('/resetdb', methods=['POST'])
    @limiter.limit("1/minute")
    def populate_task():
        data = request.get_json()
        secret = data.get('secret')

        if secret == "Acgfi9^Ziy!$zpY39CRg4Ww7ZjbmHHwdnbkYYbVen6HN*&ZiY9y$QDU8fB$ED*8tBR!BAwUwA^STjcgXPkUY*oUe*S9YY@D$WEfuK4gA%vDC$mE7&j9tH&Js#6yJJ88D":
            # initialisation de la base de données
            with app.app_context():
                db.init_db()
            executor.submit_stored('populate', populate)
            executor.futures.pop('populate')
            return 'Populating the database...'
        return 'nope'

    @app.route('/progress')
    def progress():
        # progress variable from mobility.csv_converter
        return f"{round(mobility.csv_converter.progress/18048*100, 1)}% done."

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
