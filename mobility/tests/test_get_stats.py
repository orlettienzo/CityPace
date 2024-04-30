import unittest
from unittest.mock import MagicMock, patch
from mobility.models.get_stats import get_entry_list, get_number_of_streets_by_city


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


if __name__ == '__main__':
    unittest.main()



