import sqlite3
import unittest
from unittest.mock import MagicMock, patch
from requests.models import Response

# Importe a função que você deseja testar
from mobility.models.street_model import get_street_list, get_street_list_for_city

class TestGetStreetList(unittest.TestCase):
    def setUp(self):
        # Crie um banco de dados fictício
        self.db = MagicMock()

    @patch('mobility.models.street_model.get_db')
    def test_get_street_list(self, mock_get_db):
        # Defina o retorno esperado do banco de dados
        expected_result = [
            (1, 'Rua A', '12345', 'Cidade A'),
            (2, 'Rua B', '54321', 'Cidade B')
            # Adicione mais tuplas conforme necessário para simular o retorno do banco de dados
        ]

        # Configure o comportamento de execute() para retornar o objeto MagicMock
        mock_execute = self.db.execute.return_value
        mock_execute.fetchall.return_value = expected_result

        # Defina o comportamento esperado para get_db()
        mock_get_db.return_value = self.db

        # Chame a função que você deseja testar
        result = get_street_list()

        # Verifique se a função chamou a função execute() corretamente
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

    @patch('mobility.models.street_model.get_db')  # Replace 'your_module' with the actual module name containing the class
    def test_get_existing_street(self, mock_get_db):
        # Mocking database connection and cursor
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Mocking database result for an existing street
        mock_data = (1, "Main Street", 75000, "12345", "mock_polyline")
        mock_cursor.fetchone.return_value = mock_data

        # Call the static method
        street = Street.get(1)

        # Print mock_data for investigation
        print("Mock data:", mock_data)

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the query is executed correctly
        mock_db.execute.assert_called_once_with('SELECT * FROM rue WHERE rue_id=?', (1,))

        # Check if the result is correct
        self.assertEqual(street.name, "Main Street")
        self.assertEqual(street.postal_code, 75000)
        self.assertEqual(street.street_id, 1)
        self.assertEqual(street.polyline, "12345")

    @patch('mobility.models.street_model.get_db')  # Replace 'your_module' with the actual module name containing the class
    def test_get_non_existing_street(self, mock_get_db):
        # Mocking database connection and cursor
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Mocking database result for a non-existing street
        mock_cursor.fetchone.return_value = None

        # Call the static method
        street = Street.get(100)

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the query is executed correctly
        mock_db.execute.assert_called_once_with('SELECT * FROM rue WHERE rue_id=?', (100,))

        # Check if the result is None
        self.assertIsNone(street)

    @patch('mobility.models.street_model.get_db')  # Replace 'your_module' with the actual module name containing the class
    def test_bulk_add(self, mock_get_db):
        # Mocking database connection and cursor
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Mocking list of streets
        streets = [
            (1, "Main Street", 75000, "mock_polyline1"),
            (2, "Broadway", 10001, "mock_polyline2"),
            (3, "Oak Street", 90210, "mock_polyline3")
        ]

        # Call the static method
        Street.bulk_add(streets)

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the SQL statement is executed correctly with the provided list of streets
        expected_query = "INSERT INTO rue(rue_id, nom, code_postal, polyline ) VALUES(?, ?, ?, ?)"
        mock_db.executemany.assert_called_once_with(expected_query, streets)

        # Check if the commit method is called
        mock_db.commit.assert_called_once()

    @patch('mobility.models.street_model.get_db')  # Replace 'your_module' with the actual module name containing the class
    def test_delete(self, mock_get_db):
        # Mocking database connection and cursor
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Create a mock Street object
        street = Street("Main Street", 75000, 1, "mock_polyline")

        # Call the delete method
        street.delete()

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the delete query is executed correctly
        mock_db.execute.assert_called_once_with("DELETE FROM rue WHERE rue_id=?", (1,))

        # Check if commit is called
        mock_db.commit.assert_called_once()

    @patch('mobility.models.street_model.get_db')  # Replace 'your_module' with the actual module name containing the class
    def test_add(self, mock_get_db):
        # Mocking database connection and cursor
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Create a Street object
        street = Street("Main Street", 75000, 1, "mock_polyline")

        # Call the add method
        street.add()

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the SQL statement is executed correctly
        expected_sql = "INSERTINTOrue(rue_id,nom,code_postal,polyline)VALUES(?,?,?,?)"
        expected_params = (1, "Main Street", 75000, "mock_polyline")
        # Remove whitespace from both expected and actual SQL statements before comparison
        actual_sql = "".join(mock_db.execute.call_args[0][0].split())
        self.assertEqual(actual_sql, expected_sql)

        # Check if the parameters are correct
        self.assertEqual(mock_db.execute.call_args[0][1], expected_params)

    @patch('mobility.models.street_model.get_db')
    def test_get_street_traffic_proportions_by_week_day(self, mock_get_db):
        # Mocking database connection and cursor
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        # Mocking database result
        mock_data = [
            {"date": "2024-04-21", "lourd": 10, "voiture": 20, "velo": 5, "pieton": 15},
            {"date": "2024-04-22", "lourd": 5, "voiture": 15, "velo": 10, "pieton": 20},
            {"date": "2024-04-23", "lourd": 15, "voiture": 25, "velo": 5, "pieton": 5},
            # Add more mock data as needed for different dates
        ]
        mock_db.execute.return_value.fetchall.return_value = mock_data

        # Create an instance of Street
        street = Street("Main Street", 75000, 1, "mock_polyline")

        # Call the method
        result = street.get_street_traffic_proportions_by_week_day()

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the SQL query is executed correctly
        mock_db.execute.assert_called_once_with('SELECT * FROM traffic WHERE rue_id=?', (street.street_id,))

        # Check if the result is as expected
        expected_result = {'Monday': {'lourd': 10.0, 'pieton': 40.0, 'velo': 20.0, 'voiture': 30.0},
                            'Sunday': {'lourd': 20.0, 'pieton': 30.0, 'velo': 10.0, 'voiture': 40.0},
                            'Tuesday': {'lourd': 30.0, 'pieton': 10.0, 'velo': 10.0, 'voiture': 50.0}}

        self.assertEqual(result, expected_result)

    @patch('mobility.models.street_model.requests.get')
    def test_set_street_polyline_latlng_success(self, mock_requests_get):
        # Mocking response JSON
        mock_json = [{"lat": "50.8503", "lon": "4.3517"}]
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = mock_json

        # Set up mock requests.get to return the mock response
        mock_requests_get.return_value.__enter__.return_value = mock_response

        # Create an instance of Street
        street = Street("Main Street", "1000", "123")  # Adjust with actual street name and postal code

        # Call the method
        street.set_street_polyline_latlng()

        # Check if the URL is formed correctly
        expected_url = "https://nominatim.openstreetmap.org/search?q=Main Street, 1000, Belgium&format=json"
        mock_requests_get.assert_called_once_with(url=expected_url, timeout=10)

        # Check if the polyline is set correctly
        expected_polyline = "50.8503,4.3517"
        self.assertEqual(street.polyline, expected_polyline)


    @patch('mobility.models.street_model.requests.get')
    def test_set_street_polyline_latlng_exception(self, mock_requests_get):
        # Set up mock requests.get to raise an exception
        mock_requests_get.side_effect = Exception("Connection error")

        # Create an instance of Street
        street = Street("Main Street", "1000", "123")

        # Call the method
        street.set_street_polyline_latlng()

        # Check if the polyline is set to empty string
        self.assertEqual(street.polyline, "")


if __name__ == '__main__':
    unittest.main()



