import unittest
from unittest.mock import patch
from mobility.models.appdata_model import db_populated


class TestDBPopulated(unittest.TestCase):

    @patch('mobility.models.appdata_model.get_db')  # Remplace la fonction get_db par un mock
    def test_db_populated_true(self, mock_get_db):
        # Mocke le comportement de get_db pour retourner un objet de base de données avec un résultat non nul
        mock_db = mock_get_db.return_value
        mock_db.execute.return_value.fetchone.return_value = ('some_data_value',)

        # Appelle la fonction db_populated et vérifie si elle retourne True
        self.assertTrue(db_populated())

    @patch('mobility.models.appdata_model.get_db')  # Remplace la fonction get_db par un mock
    def test_db_populated_false(self, mock_get_db):
        # Mocke le comportement de get_db pour retourner un objet de base de données avec un résultat nul
        mock_db = mock_get_db.return_value
        mock_db.execute.return_value.fetchone.return_value = None

        # Appelle la fonction db_populated et vérifie si elle retourne False
        self.assertFalse(db_populated())

if __name__ == '__main__':
    unittest.main()
