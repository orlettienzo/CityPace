import sqlite3
from flask import current_app, g


def get_db():
    """Connexion à la base de données. Si la connexion n'existe pas, elle est créée."""
    if 'db' not in g:
        g.db = sqlite3.connect(
        current_app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Fermeture de la connexion à la base de données si elle existe."""
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """Initialisation de la base de données."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_app(app):
    """Enregistrement de la fonction init_db pour l'application."""
    app.teardown_appcontext(close_db)
