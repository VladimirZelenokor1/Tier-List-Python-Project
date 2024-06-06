import unittest
from unittest.mock import MagicMock

from backend.db import get_db, DBContext


class TestDB(unittest.TestCase):
    def test_get_db(self):
        with unittest.mock.patch("backend.db.DBContext") as mock_db_context:
            mock_db = MagicMock()

            mock_db_context.return_value.__enter__.return_value = mock_db

            actual_db = next(get_db())

            self.assertEqual(actual_db, mock_db)
            mock_db_context.assert_called_once()

    def test_db_context(self):
        with unittest.mock.patch("backend.db.db_session") as session_mock:
            db_mock = MagicMock()
            session_mock.return_value = db_mock

            with DBContext() as db_context:
                self.assertEqual(db_context, db_mock)

            session_mock.assert_called_once()
            db_mock.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
