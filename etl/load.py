from dao.sqlite3_db_connection import DBConnection
import pandas as pd
import json


class Load:
    '''
    Creates and fills the sql tables of the database from the transformed json file.
    '''
    def __init__(self, json_data):
        json_data = json.loads(json_data)

        self.df_data = pd.DataFrame(json_data)
        self.df_data['feat_id'] = self.df_data.index

        artist_name = pd.unique(pd.concat([self.df_data['primary_artist_name'],
                                            self.df_data['featured_artists_names'].explode()],
                                            axis=0, ignore_index=True))

        self.artist_id = dict(zip(artist_name, range(len(artist_name))))

    def init_database(self):
        with open('init_sqlite3_db.sql') as sql_file, DBConnection().connection as connection:
            cursor = connection.cursor()
            sql_script = sql_file.read()
            cursor.executescript(sql_script)
            connection.commit()

    def load_artist_table(self):
        artist = pd.DataFrame(self.artist_id.items(),
                              columns=['artist_name', 'artist_id'])

        with DBConnection().connection as connection:
            artist.to_sql('artist', con=connection,
                          if_exists='append', index=False)

    def load_feat_table(self):
        frame = {'feat_id': self.df_data['feat_id'],
                 'primary_artist_id': self.df_data['primary_artist_name'],
                 'feat_date': self.df_data['date']}
        feat = pd.DataFrame(frame)
        feat['primary_artist_id'] = feat['primary_artist_id'].apply(self.artist_id.get)

        with DBConnection().connection as connection:
            feat.to_sql('feat', con=connection,
                        if_exists='append', index=False)

    def load_featured_table(self):
        frame = {'feat_id': self.df_data['feat_id'],
                 'featured_artist_id': self.df_data['featured_artists_names']}
        featured = pd.DataFrame(frame).explode('featured_artist_id')
        featured['featured_artist_id'] = featured['featured_artist_id'].apply(self.artist_id.get)

        with DBConnection().connection as connection:
            featured.to_sql('featured', con=connection,
                            if_exists='append', index=False)

    def load(self):
        self.init_database()
        self.load_artist_table()
        self.load_feat_table()
        self.load_featured_table()
