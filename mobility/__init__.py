import os
from flask import Flask, render_template
from flask_executor import Executor
import requests

def discord_notify(message):
    url = "https://discord.com/api/webhooks/1212030126792122430/WoBcKMxVkfSPG-lYdrYQ0UyRDt8l2hr1m8pJHlJ-TmFgDIfz6Nwcu69jWS5DAjOnbXpX"
    data = {
        "content": message
    }
    requests.post(url, data=data)


def create_app(test_config=None):
    """Création et configuration de l'application. 'L'usine de l'application' comme il disent."""
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    executor = Executor(app)
    db_populated = False

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.root_path, 'db.sqlite'),
        )

    from . import city, street
    app.register_blueprint(city.bp)
    app.register_blueprint(street.bp)

    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/street', endpoint='street_index')

    app.app_context().push()

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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/about')
    def about():
        return render_template('about.html', HelloWorld='Hello World 😎')

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
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    from . import db
    db.init_app(app)

    with app.app_context():
        db.init_db()
        
    @app.route('/populate')
    def populate_task():
        nonlocal db_populated

        if db_populated:
            return 'Database already populated'
        db_populated = True
        executor.submit(populate)
        discord_notify('submitting populate task to executor...')
        return 'Populating the database...'
    
    @app.route('/progress')
    def progress():
        # get progress variable from mobility.csv_converter
        import mobility.csv_converter
        return str(mobility.csv_converter.progress)

    def populate():
        import mobility.csv_converter
        mobility.csv_converter.populate_db()

    return app
