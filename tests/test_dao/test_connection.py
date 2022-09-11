from dao.sqlite3_db_connection import DBConnection
import unittest


class TestConnection(unittest.TestCase):

    def test_connection(self):
        with DBConnection().connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 as test")
            res = cursor.fetchone()
        self.assertEqual(1, res[0])
