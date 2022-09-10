from utils.singleton import Singleton
from dao.sqlite3_db_connection import DBConnection


class FeatDao(metaclass=Singleton):
    
    def count_primary_artist(self):
        """
        Get all artist name with the number of feat as primary artist.
        """
        query = "SELECT artist_name, COUNT(artist_id) AS count_feat "\
                "FROM artist JOIN feat "\
                "ON artist.artist_id = feat.primary_artist_id "\
                "GROUP BY artist_name "\
                "ORDER BY count_feat DESC;"
                
        with DBConnection().connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            res = cursor.fetchall()
            
        return res
        
    def count_featured_artist(self):
        """
        Get all artist name with the number of feat as featured artist.
        """
        query = "SELECT artist.artist_name AS featured_artist_name, "\
                "COUNT(artist_id) AS count_feat "\
                "FROM artist "\
                "JOIN featured ON artist.artist_id = featured.featured_artist_id "\
                "JOIN feat ON featured.feat_id = feat.feat_id "\
                "GROUP BY artist_name "\
                "ORDER BY count_feat DESC;"
                
        with DBConnection().connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            res = cursor.fetchall()
            
        return res
    
    def date_count(self):
        """
        Get all date with the cooresponding number of feat.
        """
        query = "SELECT feat_date, COUNT(*) FROM feat "\
                "JOIN artist ON artist.artist_id = feat.primary_artist_id "\
                "GROUP BY feat_date "\
                "ORDER BY feat_date DESC;"

        with DBConnection().connection as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            res = cursor.fetchall()
            
        return res
