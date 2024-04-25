from flask import app

from mobility.utils.db_requests import request_page
import unittest
from unittest.mock import patch, MagicMock


class TestRequestPage(unittest.TestCase):
    @patch('mobility.utils.db_requests.db_populated')
    @patch('mobility.utils.db_requests.render_template')
    @patch('mobility.utils.db_requests.get_city_list')
    def test_request_page_db_populated(self, mock_get_city_list, mock_render_template, mock_db_populated):
        """Test request page when the database is populated."""
        # Mocking the return values
        mock_db_populated.return_value = True
        mock_get_city_list.return_value = ['City1', 'City2']  # Example city list

        # Calling the function
        result = request_page()

        # Assertions
        mock_render_template.assert_called_with("db_request.html", done=True, cities=['City1', 'City2'])
        self.assertEqual(result, mock_render_template.return_value)

    @patch('mobility.utils.db_requests.db_populated')
    @patch('mobility.utils.db_requests.render_template')
    @patch('mobility.utils.db_requests.get_city_list')
    def test_request_page_db_not_populated(self, mock_get_city_list, mock_render_template, mock_db_populated):
        """Test request page when the database is not populated."""
        # Mocking the return values
        mock_db_populated.return_value = False

        # Calling the function
        result = request_page()

        # Assertions
        mock_render_template.assert_called_with("db_request.html", done=False)
        self.assertEqual(result, mock_render_template.return_value)

if __name__ == '__main__':
    unittest.main()





