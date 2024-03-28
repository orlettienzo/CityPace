import sqlite3
from flask import current_app, g

def get_db() -> sqlite3.Connection:
    """Renvoie la connexion à la base de données. Crée la connexion si nécessaire.

    Returns:
        db: La connexion à la base de données à utiliser pour les fonctions SQL
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        print(current_app.config['DATABASE'])

        # Au lieu d'obtenir un "tuple" à partir des requêtes, nous obtiendrons des dictionnaires de colonne->valeur
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None) -> None:
    """Ferme la base de données.

    Args:
        e: non utilisé
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db() -> None:
    """Réinitialisation de la base de données."""
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app) -> None:
    """À appeler lorsque une application est initialisée.

    Demande d'appeler close_db lorsque l'application est fermée.
    
    Args:
        app: le contexte de l'application
    """
    app.teardown_appcontext(close_db)
