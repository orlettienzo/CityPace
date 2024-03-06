from mobility.db import get_db

def get_db_populated():
    db = get_db()
    if db.execute("SELECT data_value FROM appdata WHERE data_id=?", (1,)).fetchone() is None:
        return False
    return True