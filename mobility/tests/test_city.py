import os
import tempfile
import unittest

from mobility import create_app
from mobility.db import init_db, get_db


class TestCity(unittest.TestCase):
    def setUp(self):
        # Génère un fichier temporaire pour la base de données de test
        self.db_fd, self.db_path = tempfile.mkstemp()
        # Crée l'application de test avec le fichier temporaire pour la base de données de test
        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = get_db()

        init_db()

        # Lit le SQL pour peupler les données de test
        with open(os.path.join(os.path.dirname(__file__), "schema_test.sql"), "rb") as f:
            self.db.executescript(f.read().decode("utf8"))

    def test_city_list_with_db_populated(self):
        with self.app.test_client() as client:
            with self.app.app_context():
                db = get_db()

                # Requête pour compter le nombre d'enregistrements dans la table 'ville'
                cursor = db.execute("SELECT COUNT(*) FROM ville")
                result = cursor.fetchone()[0]

                # Vérifie si le nombre d'enregistrements est égal à 3 (5 à cause des autres tests)
                self.assertEqual(result, 5)

                # Effectue une requête GET vers la route '/'
                response = client.get('/')

            # Vérifie si la réponse a le code 200 (OK)
            self.assertEqual(response.status_code, 200)

    def test_city_list_with_db_not_populated(self):
        with self.app.test_client() as client:
            with self.app.app_context():
                db = get_db()

                # Supprime toutes les entrées de la table 'ville'
                db.execute("DELETE FROM ville")
                db.commit()

                # Requête pour compter le nombre d'enregistrements dans la table 'ville' après suppression
                cursor = db.execute("SELECT COUNT(*) FROM ville")
                result = cursor.fetchone()[0]

                # Vérifie si le nombre d'enregistrements est égal à 0
                self.assertEqual(result, 0)

                # Effectue une requête GET vers la route '/'
                response = client.get('/')


            # Vérifie si la réponse a le code 200 (OK)
            self.assertEqual(response.status_code, 200)


    def dbDown(self):
        # closing the db and cleaning the temp file
        close_db()
        os.close(self.db_fd)
        os.unlink(self.db_path)

if __name__ == '__main__':
    unittest.main()