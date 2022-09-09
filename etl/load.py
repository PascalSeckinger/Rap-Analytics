from dao.sqlite3_db_connection import DBConnection
import pandas as pd
import json


class Load:
    '''
    Creates and fills the sql tables of the database from the transformed json file.
    '''
    def __init__(self, json_data):
        self.json_data = json.loads(json_data)

        self.df_data = pd.DataFrame(self.json_data)
        # add index as feat_id
        feat_id = pd.Series(list(range(len(self.df_data))))
        self.df_data.insert(0, 'feat_id', feat_id)

        # unique artist name list
        artist_name = pd.concat([self.df_data['primary_artist_name'],
                                self.df_data['featured_artists_names'].explode()],
                                axis=0, ignore_index=True)
        self.artist_name = list(pd.unique(artist_name))

        # artist_name: id correspondence
        self.name_to_id = dict(zip(self.artist_name,
                                   [i for i in range(len(self.artist_name))]))

    def init_database(self):
        with open('init_sqlite3_db.sql') as sql_file, DBConnection().connection as connection:
            cursor = connection.cursor()
            sql_script = sql_file.read()
            cursor.executescript(sql_script)
            connection.commit()

    def load_artist_table(self):
        artist = pd.DataFrame(
                        [[self.name_to_id.get(name), name]
                            for name in self.artist_name],
                        columns=['artist_id', 'artist_name']
                    )
        with DBConnection().connection as connection:
            artist.to_sql('artist', con=connection,
                          if_exists='append', index=False)

    def load_feat_table(self):
        frame = {'feat_id': self.df_data['feat_id'],
                 'primary_artist_id': self.df_data['primary_artist_name'],
                 'feat_date': self.df_data['date']}
        feat = pd.DataFrame(frame)
        feat['primary_artist_id'] = feat['primary_artist_id'].apply(self.name_to_id.get)

        with DBConnection().connection as connection:
            feat.to_sql('feat', con=connection,
                        if_exists='append', index=False)

    def load_featured_table(self):
        featured = []
        for index, row in self.df_data.iterrows():
            for featured_artist_name in row['featured_artists_names']:
                featured.append([row['feat_id'],
                                self.name_to_id.get(featured_artist_name)])

        df_featured = pd.DataFrame(
                            featured,
                            columns=['feat_id', 'featured_artist_id']
                        )

        with DBConnection().connection as connection:
            df_featured.to_sql('featured', con=connection,
                               if_exists='append', index=False)

    def load(self):
        self.init_database()
        self.load_artist_table()
        self.load_feat_table()
        self.load_featured_table()
