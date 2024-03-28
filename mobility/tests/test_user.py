import os
import tempfile
import unittest

from mobility import create_app
from mobility.utils.db import get_db, close_db


class TestUser(unittest.TestCase):

    def setUp(self):
        # générer un fichier temporaire pour la base de données de test
        self.db_fd, self.db_path = tempfile.mkstemp()
        # créer l'application de test avec le fichier temporaire pour la base de données de test
        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = get_db()

        # lire le SQL pour peupler les données de test
        with open(os.path.join(os.path.dirname(__file__), "schema_test.sql"), "rb") as f:
            self.db.executescript(f.read().decode("utf8"))

    def tearDown(self):
        # fermeture de la base de données et nettoyage du fichier temporaire
        close_db()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    # def test_search_by_email(self):
    #     # test unitaire contre la base de données de test.
    #     # certaine fonction qui obtient des villes par code postal
    #     villes = some_package.some_search_code_postal(4000)
    #     self.assertEqual(len(villes), 1)
    #     self.assertEqual(villes[0]["nom"], 'Liège')


if __name__ == '__main__':
    unittest.main(verbosity=2)
