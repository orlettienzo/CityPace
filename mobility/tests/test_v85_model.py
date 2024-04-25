import unittest
from unittest.mock import MagicMock, patch

# Import the class you want to test
from mobility.models.v85_model import v85

class TestV85(unittest.TestCase):
    def setUp(self):
        # Create a mock database
        self.db = MagicMock()

    @patch('mobility.models.v85_model.get_db')
    def test_get_v85(self, mock_get_db):
        # Set up the expected return from the database
        mock_execute = self.db.execute.return_value
        mock_execute.fetchone.return_value = {
            "rue_id": 1,
            "date": "2024-04-20",
            "v85_value": 60.5
        }

        # Set up the expected behavior for get_db()
        mock_get_db.return_value = self.db

        # Call the static method to fetch v85 data
        result = v85.get(rue_id=1, date="2024-04-20")

        # Verify if the returned data matches the expected one
        self.assertEqual(result.rue_id, 1)
        self.assertEqual(result.date, "2024-04-20")
        self.assertEqual(result.v85, 60.5)

    @patch('mobility.models.v85_model.get_db')
    def test_add_v85(self, mock_get_db):
        # Set up the expected behavior for get_db()
        mock_get_db.return_value = self.db

        # Create a fictitious v85 object
        v = v85(rue_id=1, date="2024-04-20", v85=60.5)

        # Call the add() method to save the v85 to the database
        v.add()

        # Verify if the execute() function of the database was called correctly
        self.db.execute.assert_called_once()

    @patch('mobility.models.v85_model.get_db')
    def test_delete_v85(self, mock_get_db):
        # Set up the expected behavior for get_db()
        mock_get_db.return_value = self.db

        # Create a fictitious v85 object
        v = v85(rue_id=1, date="2024-04-20", v85=60.5)

        # Call the delete() method to delete the v85 from the database
        v.delete()

        # Verify if the execute() function of the database was called correctly
        self.db.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()

