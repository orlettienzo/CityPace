from mobility.utils.db import get_db
import sqlite3

def db_populated() -> bool:
    """Retourne vrai si la base de données a été initialisée, faux sinon."""
    db = get_db()
    try:
        if db.execute("SELECT data_value FROM appdata WHERE data_id=?", (1,)).fetchone() is None:
            return False
        return True
    except sqlite3.OperationalError:
        return False
