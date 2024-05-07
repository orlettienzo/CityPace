import unittest
from unittest.mock import MagicMock, patch

from mobility.models import get_stats
from mobility.models.get_stats import get_entry_list
from mobility.utils.moon_utils import MoonPhase

from mobility.models.get_stats import get_bike_ratio_on_full_moon_days


class TestGetEntryList(unittest.TestCase):

    @patch('mobility.models.get_stats.get_db')
    def test_get_entry_list(self, mock_get_db):
        # Mocking database cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('ville', 10), ('rue', 20), ('vitesse', 5), ('v85', 15), ('traffic', 30)]
        mock_db = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Call get_entry_list function
        result = get_entry_list()

        # Check if the execute method was called with the correct SQL query
        mock_db.execute.assert_called_once_with('''
                      SELECT "ville" AS table_name, COUNT(*) AS number_of_entries FROM ville UNION ALL 
                      SELECT "rue" AS table_name, COUNT(*) AS number_of_entries FROM rue UNION ALL 
                      SELECT "vitesse" AS table_name, COUNT(*) AS number_of_entries FROM vitesse UNION ALL 
                      SELECT "v85" AS table_name, COUNT(*) AS number_of_entries FROM v85 UNION ALL 
                      SELECT "traffic" AS table_name, COUNT(*) AS number_of_entries FROM traffic
                      ''')

        # Check if the fetchall method returns the expected result
        self.assertEqual(result.fetchall(), [('ville', 10), ('rue', 20), ('vitesse', 5), ('v85', 15), ('traffic', 30)])


class TestGetNumberOfStreetsByCity(unittest.TestCase):
    @patch('mobility.models.get_stats.get_db')
    def test_get_number_of_streets_by_city(self, mock_get_db):
        # Mocking database response
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [("City1", 10), ("City2", 8), ("City3", 6)]  # Example data
        mock_db = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Call the function to get number of streets by city
        result = get_stats.get_number_of_streets_by_city()

        # Expected result
        expected_result = [("City1", 10), ("City2", 8), ("City3", 6)]

        # Test
        self.assertEqual(result.fetchall(), expected_result)



class TestGetMostCyclableCities(unittest.TestCase):
    @patch('mobility.models.get_stats.get_db')
    def test_get_most_cyclable_cities(self, mock_get_db):
        # Mocking database response
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [("City1", 10000, 0.5, 500), ("City2", 20000, 0.4, 800), ("City3", 15000, 0.3, 450)]  # Example data
        mock_db = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Call the function to get most cyclable cities
        result = get_stats.get_most_cyclable_cities()

        # Expected result
        expected_result = [("City1", 10000, 0.5, 500), ("City2", 20000, 0.4, 800), ("City3", 15000, 0.3, 450)]

        # Test
        self.assertEqual(result.fetchall(), expected_result)

class TestGetMostTrafficStreets(unittest.TestCase):
    @patch('mobility.models.get_stats.get_db')
    def test_get_most_traffic_streets(self, mock_get_db):
            # Mocking database response
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [("City1", "Street1", 1000), ("City2", "Street2", 800),
                                                 ("City3", "Street3", 600)]  # Example data
            mock_db = MagicMock()
            mock_db.execute.return_value = mock_cursor
            mock_get_db.return_value = mock_db

            # Call the function to get most traffic streets
            result = get_stats.get_most_traffic_streets()

            # Expected result
            expected_result = [("City1", "Street1", 1000), ("City2", "Street2", 800), ("City3", "Street3", 600)]

            # Test
            self.assertEqual(result.fetchall(), expected_result)

class TestGetFastestStreets(unittest.TestCase):
    @patch('mobility.models.get_stats.get_db')
    def test_get_fastest_streets(self, mock_get_db):
        # Mocking database response
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1, "City1", "Street1", 120, 90), (2, "City2", "Street2", 120, 80),
                                             (3, "City3", "Street3", 120, 70)]  # Example data
        mock_db = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Call the function to get fastest streets
        result = get_stats.get_fastest_streets()

        # Expected result
        expected_result = [(1, "City1", "Street1", 120, 90), (2, "City2", "Street2", 120, 80),
                           (3, "City3", "Street3", 120, 70)]

        # Test
        self.assertEqual(result, expected_result)



if __name__ == '__main__':
    unittest.main()



