import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from mobility.models.city_model import get_city_list, City

class TestGetCityList(unittest.TestCase):

    @patch('mobility.models.city_model.get_db')
    def test_get_city_list(self, mock_get_db):
        # Mocking database result
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_cursor.fetchall.return_value = [
            (1, "City1", 1000),
            (2, "City2", 2000),
            # Add more mock data as needed
        ]
        mock_db = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Call the function
        result = get_city_list()

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the SQL query is executed correctly
        mock_db.execute.assert_called_once_with('SELECT * FROM ville ORDER BY code_postal')

        # Check if the result is as expected
        expected_result = [
            (1, "City1", 1000),
            (2, "City2", 2000),
            # Add expected data as tuples in the same format
        ]
        self.assertEqual(result.fetchall(), expected_result)

class TestCity(unittest.TestCase):

    def test_city_creation(self):
        # Create an instance of City
        city = City("Paris", 2200000, "75000")

        # Check if attributes are set correctly
        self.assertEqual(city.name, "Paris")
        self.assertEqual(city.population, 2200000)
        self.assertEqual(city.postal_code, "75000")

    def test_city_creation_without_postal_code(self):
        # Create an instance of City without providing postal code
        city = City("London", 8900000)

        # Check if attributes are set correctly
        self.assertEqual(city.name, "London")
        self.assertEqual(city.population, 8900000)
        self.assertIsNone(city.postal_code)

    def test_str_with_postal_code(self):
        # Create a city object with postal code
        city = City("New York", 8000000, 10001)

        # Check the string representation
        expected_str = "New York (10001), 8000000 habitants"
        self.assertEqual(str(city), expected_str)

    def test_str_without_postal_code(self):
        # Create a city object without postal code
        city = City("Paris", 2000000)

        # Check the string representation
        expected_str = "Paris (None), 2000000 habitants"
        self.assertEqual(str(city), expected_str)

    @patch('mobility.models.city_model.get_db')
    def test_get_city(self, mock_get_db):
        # Mocking database result
        mock_data = (
        1, "CityName", 100000)  # Assuming the database returns a tuple with (postal_code, name, population)
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_data
        mock_db = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Call the get method
        result = City.get(12345)

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the SQL query is executed correctly
        mock_db.execute.assert_called_once_with('SELECT * FROM ville WHERE code_postal=?', (12345,))

        # Check if the result is as expected
        expected_result = City("CityName", 100000, 1)  # Assuming the database returns (1, "CityName", 100000)
        self.assertEqual(result.name, expected_result.name)
        self.assertEqual(result.population, expected_result.population)
        self.assertEqual(result.postal_code, expected_result.postal_code)

    @patch('mobility.models.city_model.get_db')
    def test_bulk_add(self, mock_get_db):
        # Mocking database connection and cursor
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        # Sample cities data
        cities_data = [
            (1000, "City1", 10000),
            (2000, "City2", 20000),
            # Add more cities as needed
        ]

        # Call the bulk_add method
        City.bulk_add(cities_data)

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the SQL statement is executed correctly
        expected_query = "INSERT INTO ville(code_postal,nom, population ) VALUES(?, ?, ?)"
        mock_db.executemany.assert_called_once_with(expected_query, cities_data)
        mock_db.commit.assert_called_once()

    @patch('mobility.models.city_model.get_db')
    def test_delete_city(self, mock_get_db):
        # Mocking database execution
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        # Create an instance of City
        city = City("Example City", 10000, "12345")

        # Call the delete method
        city.delete()

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the SQL statement is executed correctly
        mock_db.execute.assert_called_once_with("DELETE FROM ville WHERE code_postal=?", ("12345",))

        # Check if the commit method is called
        mock_db.commit.assert_called_once()

    @patch('mobility.models.city_model.get_db')
    def test_add(self, mock_get_db):
        # Mocking database connection and cursor
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        # Create an instance of City
        city = City("New York", 1000000, "10001")  # Adjust with actual city name, population, and postal code

        # Call the add method
        city.add()

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the SQL statement is executed correctly
        mock_db.execute.assert_called_once_with("INSERT INTO ville(code_postal,nom, population ) VALUES(?, ?, ?)",
                                                ("10001", "New York", 1000000))

        # Check if commit is called
        mock_db.commit.assert_called_once()

    @patch('mobility.models.city_model.get_db')
    def test_get_total_lourd(self, mock_get_db):
        # Mocking database response
        mock_streets = [
            {"rue_id": 1},  # Example street 1
            {"rue_id": 2}   # Example street 2
        ]
        mock_traffic_counts = [10, 20]  # Example traffic counts for streets 1 and 2
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = mock_traffic_counts
        mock_db = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Create city object
        city = City("Test City", 10000, "12345")

        # Call the method to get total lourd
        result = city.get_total_lourd()

        # Expected result
        expected_result = 0

        # Test
        self.assertEqual(result, expected_result)

    @patch('mobility.models.city_model.get_db')
    def test_get_total_voiture(self, mock_get_db):
        # Mocking database response
        mock_streets = [
            {"rue_id": 1},  # Example street 1
            {"rue_id": 2}  # Example street 2
        ]
        mock_traffic_counts = [10, 20]  # Example traffic counts for streets 1 and 2
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = mock_traffic_counts
        mock_db = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Create city object
        city = City("Test City", 10000, "12345")

        # Call the method to get total voiture
        result = city.get_total_voiture()

        # Expected result
        expected_result = 0

        # Test
        self.assertEqual(result, expected_result)

    @patch('mobility.models.city_model.get_db')
    def test_get_total_velo(self, mock_get_db):
        # Mocking database response
        mock_streets = [
            {"rue_id": 1},  # Example street 1
            {"rue_id": 2}  # Example street 2
        ]
        mock_traffic_counts = [5, 15]  # Example traffic counts for streets 1 and 2
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = mock_traffic_counts
        mock_db = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Create city object
        city = City("Test City", 10000, "12345")

        # Call the method to get total velo
        result = city.get_total_velo()

        # Expected result
        expected_result = 0

        # Test
        self.assertEqual(result, expected_result)

    @patch('mobility.models.city_model.get_db')
    def test_get_total_pieton(self, mock_get_db):
        # Mocking database response
        mock_streets = [
            {"rue_id": 1},  # Example street 1
            {"rue_id": 2}  # Example street 2
        ]
        mock_traffic_counts = [3, 7]  # Example traffic counts for streets 1 and 2
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = mock_traffic_counts
        mock_db = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Create city object
        city = City("Test City", 10000, "12345")

        # Call the method to get total pieton
        result = city.get_total_pieton()

        # Expected result
        expected_result = 0

        # Test
        self.assertEqual(result, expected_result)

    @patch('mobility.models.city_model.get_db')
    def test_get_city_traffic_proportions_for_period(self, mock_get_db):
        # Mocking database response
        mock_traffic_data = [
            {"rue_id": 1, "lourd": 10, "voiture": 20, "velo": 5, "pieton": 5},
            {"rue_id": 2, "lourd": 5, "voiture": 10, "velo": 8, "pieton": 3}
        ]  # Example traffic data for the city
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = mock_traffic_data
        mock_db = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Create city object
        city = City("Test City", 10000, "12345")

        # Define start and end dates for the period
        start_date = "2024-01-01"
        end_date = "2024-01-05"

        # Call the method to get city traffic proportions for the period
        result = city.get_city_traffic_proportions_for_period(start_date, end_date)

        # Expected result
        expected_result = {
            "lourd": 22.73,
            "voiture": 45.45,
            "velo": 19.7,
            "pieton": 12.12
        }

        # Test
        self.assertEqual(result, expected_result)

    @patch('mobility.models.city_model.get_db')
    def test_get_city_time_span(self, mock_get_db):
        # Mocking database response
        mock_time_span_data = {"start_date": "2024-01-01", "end_date": "2024-01-05"}  # Example time span data
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_time_span_data
        mock_db = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Create city object
        city = City("Test City", 10000, "12345")

        # Call the method to get city time span
        result = city.get_city_time_span()

        # Expected result
        expected_result = {"start_date": "2024-01-01", "end_date": "2024-01-05"}

        # Test
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()

