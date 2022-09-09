import sqlite3 as sgbd
from utils.singleton import Singleton


class DBConnection(metaclass=Singleton):
    """
    Technical class to open only one connection to the DB.
    """
    def __init__(self):
        self.__connection = sgbd.connect('data/rapminerz.db')


    @property
    def connection(self):
        """
        return the opened connection.

        :return: the opened connection.
        """
        return self.__connection