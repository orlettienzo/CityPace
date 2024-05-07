import sqlite3
import unittest
from unittest.mock import MagicMock, patch
from requests.models import Response

# Importer la fonction à tester
from mobility.models.street_model import get_street_list, get_street_list_for_city

class TestGetStreetList(unittest.TestCase):
    def setUp(self):
        # Créer une base de données fictive
        self.db = MagicMock()

    @patch('mobility.models.street_model.get_db')
    def test_get_street_list(self, mock_get_db):
        # Définir le résultat attendu de la base de données
        expected_result = [
            (1, 'Rue A', '12345', 'Ville A'),
            (2, 'Rue B', '54321', 'Ville B')
            # Ajouter plus de tuples selon le besoin pour simuler le retour de la base de données
        ]

        # Configurer le comportement de execute() pour renvoyer l'objet MagicMock
        mock_execute = self.db.execute.return_value
        mock_execute.fetchall.return_value = expected_result

        # Définir le comportement attendu pour get_db()
        mock_get_db.return_value = self.db

        # Appeler la fonction à tester
        result = get_street_list()

        # Vérifier si la fonction a bien appelé execute() correctement
        self.assertEqual(result, self.db.execute.return_value)

if __name__ == '__main__':
    unittest.main()


import unittest
from mobility.models.street_model import Street

class TestStreet(unittest.TestCase):

    def test_init(self):
        street = Street("Main Street", "12345", 1)
        self.assertEqual(street.name, "Main Street")
        self.assertEqual(street.postal_code, "12345")
        self.assertEqual(street.street_id, 1)
        self.assertEqual(street.polyline, "")

    def test_init_with_polyline(self):
        street = Street("Elm Street", "54321", 2, "some_polyline_data")
        self.assertEqual(street.name, "Elm Street")
        self.assertEqual(street.postal_code, "54321")
        self.assertEqual(street.street_id, 2)
        self.assertEqual(street.polyline, "some_polyline_data")

    @patch('mobility.models.street_model.get_db')  # Remplacez 'your_module' par le nom réel du module contenant la classe
    def test_get_existing_street(self, mock_get_db):
        # Simuler une connexion à la base de données et un curseur
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Simuler le résultat de la base de données pour une rue existante
        mock_data = (1, "Main Street", 75000, "12345", "mock_polyline")
        mock_cursor.fetchone.return_value = mock_data

        # Appeler la méthode statique
        street = Street.get(1)

        # Afficher les données simulées pour analyse
        print("Données simulées :", mock_data)

        # Vérifier si la connexion à la base de données a été appelée
        mock_get_db.assert_called_once()

        # Vérifier si la requête a été exécutée correctement
        mock_db.execute.assert_called_once_with('SELECT * FROM rue WHERE rue_id=?', (1,))

        # Vérifier si le résultat est correct
        self.assertEqual(street.name, "Main Street")
        self.assertEqual(street.postal_code, 75000)
        self.assertEqual(street.street_id, 1)
        self.assertEqual(street.polyline, "12345")

    @patch('mobility.models.street_model.get_db')  # Remplacez 'your_module' par le nom réel du module contenant la classe
    def test_get_non_existing_street(self, mock_get_db):
        # Simuler une connexion à la base de données et un curseur
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Simuler le résultat de la base de données pour une rue non existante
        mock_cursor.fetchone.return_value = None

        # Appeler la méthode statique
        street = Street.get(100)

        # Vérifier si la connexion à la base de données a été appelée
        mock_get_db.assert_called_once()

        # Vérifier si la requête a été exécutée correctement
        mock_db.execute.assert_called_once_with('SELECT * FROM rue WHERE rue_id=?', (100,))

        # Vérifier si le résultat est None
        self.assertIsNone(street)

    @patch('mobility.models.street_model.get_db')  # Remplacez 'your_module' par le nom réel du module contenant la classe
    def test_bulk_add(self, mock_get_db):
        # Simuler une connexion à la base de données et un curseur
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Simuler une liste de rues
        streets = [
            (1, "Main Street", 75000, "mock_polyline1"),
            (2, "Broadway", 10001, "mock_polyline2"),
            (3, "Oak Street", 90210, "mock_polyline3")
        ]

        # Appeler la méthode statique
        Street.bulk_add(streets)

        # Vérifier si la connexion à la base de données a été appelée
        mock_get_db.assert_called_once()

        # Vérifier si l'instruction SQL a été exécutée correctement avec la liste fournie de rues
        expected_query = "INSERT INTO rue(rue_id, nom, code_postal, polyline ) VALUES(?, ?, ?, ?)"
        mock_db.executemany.assert_called_once_with(expected_query, streets)

        # Vérifier si la méthode commit a été appelée
        mock_db.commit.assert_called_once()

    @patch('mobility.models.street_model.get_db')  # Remplacez 'your_module' par le nom réel du module contenant la classe
    def test_delete(self, mock_get_db):
        # Simuler une connexion à la base de données et un curseur
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Créer un objet Street fictif
        street = Street("Main Street", 75000, 1, "mock_polyline")

        # Appeler la méthode delete
        street.delete()

        # Vérifier si la connexion à la base de données a été appelée
        mock_get_db.assert_called_once()

        # Vérifier si la requête de suppression a été exécutée correctement
        mock_db.execute.assert_called_once_with("DELETE FROM rue WHERE rue_id=?", (1,))

        # Vérifier si commit a été appelée
        mock_db.commit.assert_called_once()

    @patch('mobility.models.street_model.get_db')  # Remplacez 'your_module' par le nom réel du module contenant la classe
    def test_add(self, mock_get_db):
        # Simuler une connexion à la base de données et un curseur
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Créer un objet Street
        street = Street("Main Street", 75000, 1, "mock_polyline")

        # Appeler la méthode add
        street.add()

        # Vérifier si la connexion à la base de données a été appelée
        mock_get_db.assert_called_once()

        # Vérifier si l'instruction SQL a été exécutée correctement
        expected_sql = "INSERTINTOrue(rue_id,nom,code_postal,polyline)VALUES(?,?,?,?)"
        expected_params = (1, "Main Street", 75000, "mock_polyline")

        # Supprimer les espaces des deux côtés de la chaîne SQL attendue et réelle avant de comparer
        actual_sql = "".join(mock_db.execute.call_args[0][0].split())
        self.assertEqual(actual_sql, expected_sql)

        # Vérifier si les paramètres sont corrects
        self.assertEqual(mock_db.execute.call_args[0][1], expected_params)

    @patch('mobility.models.street_model.get_db')  # Remplacez 'your_module' par le nom réel du module contenant la classe
    def test_get_street_traffic_proportions_by_week_day(self, mock_get_db):
        # Simuler une connexion à la base de données et un curseur
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        # Simuler le résultat de la base de données
        mock_data = [
            {"date": "2024-04-21", "lourd": 10, "voiture": 20, "velo": 5, "pieton": 15},
            {"date": "2024-04-22", "lourd": 5, "voiture": 15, "velo": 10, "pieton": 20},
            {"date": "2024-04-23", "lourd": 15, "voiture": 25, "velo": 5, "pieton": 5},
            # Ajouter plus de données simulées selon le besoin pour différentes dates
        ]
        mock_db.execute.return_value.fetchall.return_value = mock_data

        # Créer une instance de Street
        street = Street("Main Street", 75000, 1, "mock_polyline")

        # Appeler la méthode
        result = street.get_street_traffic_proportions_by_week_day()

        # Vérifier si la connexion à la base de données a été appelée
        mock_get_db.assert_called_once()

        # Vérifier si la requête SQL a été exécutée correctement
        mock_db.execute.assert_called_once_with('SELECT * FROM traffic WHERE rue_id=?', (street.street_id,))

        # Vérifier si le résultat est conforme aux attentes
        expected_result = {'Lundi': {'lourd': 10.0, 'pieton': 40.0, 'velo': 20.0, 'voiture': 30.0},
                            'Dimanche': {'lourd': 20.0, 'pieton': 30.0, 'velo': 10.0, 'voiture': 40.0},
                            'Mardi': {'lourd': 30.0, 'pieton': 10.0, 'velo': 10.0, 'voiture': 50.0}}

        self.assertEqual(result, expected_result)

    @patch('mobility.models.street_model.requests.get')
    def test_set_street_polyline_latlng_success(self, mock_requests_get):
        # Simuler le JSON de réponse
        mock_json = [{"lat": "50.8503", "lon": "4.3517"}]
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = mock_json

        # Configurer mock_requests_get pour renvoyer la réponse fictive
        mock_requests_get.return_value.__enter__.return_value = mock_response

        # Créer une instance de Street
        street = Street("Main Street", "1000", "123")  # Ajustez avec le nom réel de la rue et le code postal

        # Appeler la méthode
        street.set_street_polyline_latlng()

        # Vérifier si l'URL a été correctement formée
        expected_url = "https://nominatim.openstreetmap.org/search?q=Main Street, 1000, Belgium&format=json"
        mock_requests_get.assert_called_once_with(url=expected_url, timeout=10)

        # Vérifier si la polyline a été définie correctement
        expected_polyline = "50.8503,4.3517"
        self.assertEqual(street.polyline, expected_polyline)

    @patch('mobility.models.street_model.requests.get')
    def test_set_street_polyline_latlng_exception(self, mock_requests_get):
        # Configurer mock_requests_get pour lever une exception
        mock_requests_get.side_effect = Exception("Erreur de connexion")

        # Créer une instance de Street
        street = Street("Main Street", "1000", "123")

        # Appeler la méthode
        street.set_street_polyline_latlng()

        # Vérifier si la polyline reste vide
        self.assertEqual(street.polyline, "")

    @patch('mobility.models.street_model.get_db')
    def test_get_amount_of_traffic_for_day(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        # Mocking database response
        mock_data = [
            {"lourd": 10, "voiture": 20, "velo": 5, "pieton": 15},
            {"lourd": 5, "voiture": 15, "velo": 10, "pieton": 25}
        ]
        mock_db.execute.return_value.fetchall.return_value = mock_data

        # Create street object
        street = Street("Test Street", "12345", 1)

        # Expected result
        expected_result = {"lourd": 15, "voiture": 35, "velo": 15, "pieton": 40}

        # Test
        result = street.get_amount_of_traffic_for_day("2024-01-05T15:00:00.000Z")
        self.assertEqual(result, expected_result)

    @patch("mobility.models.street_model.get_db")
    def test_get_street_traffic_proportions_for_period(self, mock_get_db):
        # Mocking database response
        mock_data = [
            {"lourd": 10, "voiture": 20, "velo": 5, "pieton": 15},
            {"lourd": 5, "voiture": 15, "velo": 10, "pieton": 25}
        ]
        mock_db = MagicMock()
        mock_db.execute.return_value.fetchall.return_value = mock_data
        mock_get_db.return_value = mock_db

        # Create street object
        street = Street("Test Street", "12345", 1)

        # Expected result
        expected_result = {"lourd": 14.29, "voiture": 33.33, "velo": 14.29, "pieton": 38.1}

        # Test
        result = street.get_street_traffic_proportions_for_period("2024-01-05", "2024-01-06")
        self.assertEqual(result, expected_result)

    @patch('mobility.models.street_model.get_db')
    def test_get_street_time_span(self, mock_get_db):
        # Mocking database response
        mock_data = {"start_date": "2024-01-05T10:00:00.000Z", "end_date": "2024-01-06T15:00:00.000Z"}
        mock_db = MagicMock()
        mock_db.execute.return_value.fetchone.return_value = mock_data
        mock_get_db.return_value = mock_db

        # Create street object
        street = Street("Test Street", "12345", 1)

        # Expected result
        expected_result = {"start_date": "2024-01-05T10:00:00.000Z", "end_date": "2024-01-06T15:00:00.000Z"}

        # Test
        result = street.get_street_time_span()
        self.assertEqual(result, expected_result)

    @patch('mobility.models.street_model.requests.get')
    def test_set_street_polyline_latlng(self, mock_requests_get):
        # Mocking response from requests.get
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"lat": 50.8503, "lon": 4.3517}  # Coordinates for Brussels, Belgium
        ]
        mock_requests_get.return_value.__enter__.return_value = mock_response

        # Create street object
        street = Street("Test Street", "12345", 1)

        # Call the method to set street polyline
        street.set_street_polyline_latlng()

        # Expected result
        expected_polyline = "50.8503,4.3517"

        # Test
        self.assertEqual(street.polyline, expected_polyline)

    @patch.object(Street, 'get_amount_of_traffic_for_day')
    def test_get_street_traffic_over_time(self, mock_get_amount_of_traffic_for_day):
        # Mocking response from get_amount_of_traffic_for_day
        mock_get_amount_of_traffic_for_day.return_value = {"lourd": 10, "voiture": 20, "velo": 5, "pieton": 15}

        # Create street object
        street = Street("Test Street", "12345", 1)

        # Call the method to get street traffic over time
        start_date = "2024-01-01T00:00:00.000Z"
        end_date = "2024-01-03T00:00:00.000Z"
        result = street.get_street_traffic_over_time(start_date, end_date)

        # Expected result
        expected_result = {
            "lourd": [10, 10, 10],
            "voiture": [20, 20, 20],
            "velo": [5, 5, 5],
            "pieton": [15, 15, 15],
            "labels": ["Lun 01-01-24", "Mar 02-01-24", "Mer 03-01-24"]
        }

        # Test
        self.assertEqual(result, expected_result)

    @patch.object(Street, 'get_amount_of_traffic_for_day')
    def test_get_cumulative_street_traffic_over_time(self, mock_get_amount_of_traffic_for_day):
        # Mocking response from get_amount_of_traffic_for_day
        mock_get_amount_of_traffic_for_day.return_value = {"lourd": 10, "voiture": 20, "velo": 5, "pieton": 15}

        # Create street object
        street = Street("Test Street", "12345", 1)

        # Call the method to get cumulative street traffic over time
        start_date = "2024-01-01T00:00:00.000Z"
        end_date = "2024-01-03T00:00:00.000Z"
        result = street.get_cumulative_street_traffic_over_time(start_date, end_date)

        # Expected result
        expected_result = {
            "lourd": [10, 20, 30],
            "voiture": [30, 60, 90],
            "velo": [35, 70, 105],
            "pieton": [50, 100, 150],
            "labels": ["Lun 01-01-24", "Mar 02-01-24", "Mer 03-01-24"]
        }

        # Test
        self.assertEqual(result, expected_result)

    @patch('mobility.models.street_model.get_db')
    def test_get_street_coordinates(self, mock_get_db):
        # Mocking database response
        mock_polyline = "50.8503,4.3517"  # Example polyline
        mock_data = {"polyline": mock_polyline}
        mock_db = MagicMock()
        mock_db.execute.return_value.fetchone.return_value = mock_data
        mock_get_db.return_value = mock_db

        # Create street object
        street = Street("Test Street", "12345", 1)

        # Call the method to get street coordinates
        result = street.get_street_coordinates()

        # Expected result
        expected_result = mock_polyline

        # Test
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
