import os
import tempfile
import unittest

from flask import render_template_string

from mobility import create_app
from mobility.db import init_db, get_db

class TestStreet(unittest.TestCase):
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

    def test_street_list_with_db_populated(self):
        with self.app.test_client() as client:
            with self.app.app_context():
                db = get_db()

                # Requête pour compter le nombre d'enregistrements dans la table 'rue'
                cursor = db.execute("SELECT COUNT(*) FROM rue")
                result = cursor.fetchone()[0]

                # Vérifie si le nombre d'enregistrements est égal à 2
                self.assertEqual(result, 2)

            # Effectue une requête GET vers la route '/street'
            response = client.get('/street')

            # Vérifie si la réponse a le code 200 (OK)
            self.assertEqual(response.status_code, 200)

    def test_street_list_with_db_not_populated(self):
        with self.app.test_client() as client:
            with self.app.app_context():
                db = get_db()

                # Supprime toutes les entrées de la table 'rue'
                db.execute("DELETE FROM rue")
                db.commit()

                # Requête pour compter le nombre d'enregistrements dans la table 'rue' après suppression
                cursor = db.execute("SELECT COUNT(*) FROM rue")
                result = cursor.fetchone()[0]

                # Vérifie si le nombre d'enregistrements est égal à 0
                self.assertEqual(result, 0)

            # Effectue une requête GET vers la route '/street'
            response = client.get('/street')

            # Vérifie si la réponse a le code 200 (OK)
            self.assertEqual(response.status_code, 200)

    def test_street_route(self):
        # Rend le modèle 'street.html' en utilisant render_template_string
        with self.app.test_request_context('/street'):
            rendered_template = render_template_string("{% extends 'street.html' %}")

        # Convertit la chaîne rendue en octets.
        rendered_template_bytes = rendered_template.encode()

        # Vérifie si le modèle 'street.html' a été rendu correctement.
        self.assertIn(b"Liste des rues", rendered_template_bytes)


if __name__ == '__main__':
    unittest.main()
