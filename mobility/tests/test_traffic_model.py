import unittest
from unittest.mock import MagicMock, patch

# Import the class you want to test
from mobility.models.traffic_model import Traffic

class TestTraffic(unittest.TestCase):
    def setUp(self):
        # Create a mock database
        self.db = MagicMock()

    @patch('mobility.models.traffic_model.get_db')
    def test_get_traffic(self, mock_get_db):
        # Set up the expected return from the database
        mock_execute = self.db.execute.return_value
        mock_execute.fetchone.return_value = {
            "rue_id": 1,
            "code_postal": 12345,
            "date": "2024-04-20",
            "lourd": 10,
            "voiture": 20,
            "velo": 30,
            "pieton": 40
        }

        # Set up the expected behavior for get_db()
        mock_get_db.return_value = self.db

        # Call the static method to fetch traffic data
        result = Traffic.get(rue_id=1, date="2024-04-20")

        # Check if the returned data matches the expected
        self.assertEqual(result.rue_id, 1)
        self.assertEqual(result.code_postal, 12345)
        self.assertEqual(result.date, "2024-04-20")
        self.assertEqual(result.lourd, 10)
        self.assertEqual(result.voiture, 20)
        self.assertEqual(result.velo, 30)
        self.assertEqual(result.pieton, 40)

    @patch('mobility.models.traffic_model.get_db')
    def test_add_traffic(self, mock_get_db):
        # Set up the expected behavior for get_db()
        mock_get_db.return_value = self.db

        # Create a mock traffic object
        traffic = Traffic(rue_id=1, code_postal=12345, date="2024-04-20", lourd=10, voiture=20, velo=30, pieton=40)

        # Call the add() method to save the traffic to the database
        traffic.add()

        # Check if the execute() function of the database was called correctly
        self.db.execute.assert_called_once()

    @patch('mobility.models.traffic_model.get_db')
    def test_delete_traffic(self, mock_get_db):
        # Set up the expected behavior for get_db()
        mock_get_db.return_value = self.db

        # Create a mock traffic object
        traffic = Traffic(rue_id=1, code_postal=12345, date="2024-04-20", lourd=10, voiture=20, velo=30, pieton=40)

        # Call the delete() method to delete the traffic from the database
        traffic.delete()

        # Check if the execute() function of the database was called correctly
        self.db.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()
