import os
from flask import Flask, render_template


def create_app(test_config=None):
    """Création et configuration de l'application. 'L'usine de l'application' comme il disent."""
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite')
    )

    from . import city, street
    app.register_blueprint(city.bp)
    app.register_blueprint(street.bp)

    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/street', endpoint='street_index')

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

    from . import db
    db.init_app(app)

    with app.app_context():
        db.init_db()

    return app
