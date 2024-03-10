import sqlite3
from flask import current_app, g

def get_db():
    """Returns the database connection. Create the connection if needed.

    Returns:
        db: The db connection to be used for SQL functions
    """
    #g is the shorthand for "globals" and allows registering available in the whole Flask app
    if 'db' not in g:
        #If it's not there, let's create the db connection
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        print(current_app.config['DATABASE'])

        # Instead of getting "tuple" out of queries, we'll get dictionaries of column->value
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Close the database

    Args:
        e: unused
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

# def populate():
#     import mobility.csv_converter
#     mobility.csv_converter.populate_db()


def init_db():
    """Initialisation de la base de données."""
    db = get_db()

    # if the database is empty:
    # try:
    #     db.execute('SELECT * FROM ville').fetchone()
    # except sqlite3.OperationalError:
        # with current_app.open_resource('schema.sql') as f:
        #     db.executescript(f.read().decode('utf8'))
    
    # drop the tables and recreate them
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    """To be called when an app is initialized

    Asks to call close_db when the app is closed
    Args:
        app: the application context
    """
    app.teardown_appcontext(close_db)
