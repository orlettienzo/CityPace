import unittest
from mobility.models.speed_model import Speed  # Replace 'your_module' with the actual module name containing the class
from unittest.mock import patch, MagicMock
class TestSpeed(unittest.TestCase):

    def test_speed_initialization(self):
        # Create an instance of Speed
        speed = Speed(1, "2024-04-21", 2, 0.75)

        # Check if attributes are initialized correctly
        self.assertEqual(speed.rue_id, 1)
        self.assertEqual(speed.date, "2024-04-21")
        self.assertEqual(speed.tranche_de_vitesse, 2)
        self.assertEqual(speed.proportion, 0.75)

    @patch('mobility.models.speed_model.get_db')
    def test_delete(self, mock_get_db):
        # Mocking database connection and cursor
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        # Create an instance of Speed
        speed = Speed(1, "2024-04-24", 1, 0.5)

        # Call the delete method
        speed.delete()

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the SQL statement is executed correctly
        mock_db.execute.assert_called_once_with(
            "DELETE FROM vitesse WHERE rue_id=? AND date=? AND tranche_de_vitesse=?",
            (speed.rue_id, speed.date, speed.tranche_de_vitesse))

        # Check if the commit method is called
        mock_db.commit.assert_called_once()

    @patch('mobility.models.speed_model.get_db')
    def test_add(self, mock_get_db):
        # Mocking database connection and cursor
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        # Create an instance of Speed
        speed = Speed(1, "2024-04-24", 2, 0.5)  # Adjust with actual parameters

        # Call the add method
        speed.add()

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the SQL statement is executed correctly
        expected_sql = "INSERT INTO vitesse(rue_id, date, tranche_de_vitesse, proportion) VALUES(?, ?, ?, ?)"
        expected_values = (1, "2024-04-24", 2, 0.5)
        mock_db.execute.assert_called_once_with(expected_sql, expected_values)

        # Check if the commit method is called
        mock_db.commit.assert_called_once()

    @patch('mobility.models.speed_model.get_db')
    def test_bulk_add(self, mock_get_db):
        # Mocking database connection and cursor
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        # Create a list of speeds for testing
        speeds = [
            (1, "2024-04-21", 1, 0.1),
            (1, "2024-04-21", 2, 0.2),
            (2, "2024-04-21", 1, 0.3),
            # Add more test data as needed
        ]

        # Create an instance of Speed with mock arguments
        speed_instance = Speed(1, "2024-04-21", 1, 0.1)

        # Call the method
        speed_instance.bulk_add(speeds)

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the SQL statement is executed correctly
        expected_query = "INSERT INTO vitesse(rue_id, date, tranche_de_vitesse, proportion) VALUES(?, ?, ?, ?)"
        mock_db.executemany.assert_called_once_with(expected_query, speeds)

        # Check if the commit method is called
        mock_db.commit.assert_called_once()

    @patch('mobility.models.speed_model.get_db')
    def test_get_speed(self, mock_get_db):
        # Mocking database result
        mock_data = {"rue_id": 1, "date": "2024-04-21", "tranche_de_vitesse": 1, "proportion": 0.5}
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_data
        mock_db = MagicMock()
        mock_db.execute.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        # Call the get method
        result = Speed.get(1, "2024-04-21", 1)

        # Check if the database connection is called
        mock_get_db.assert_called_once()

        # Check if the SQL query is executed correctly
        mock_db.execute.assert_called_once_with(
            'SELECT * FROM vitesse WHERE rue_id=? AND date=? AND tranche_de_vitesse=?', (1, "2024-04-21", 1))

        # Check if the result is as expected
        expected_result = Speed(1, "2024-04-21", 1, 0.5)
        self.assertEqual(result.rue_id, expected_result.rue_id)
        self.assertEqual(result.date, expected_result.date)
        self.assertEqual(result.tranche_de_vitesse, expected_result.tranche_de_vitesse)
        self.assertEqual(result.proportion, expected_result.proportion)


if __name__ == '__main__':
    unittest.main()
