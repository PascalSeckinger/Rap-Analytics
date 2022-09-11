import json
import pandas as pd


class Transform:
    """
    Restructuring of the raw file obtained with extract.
    """
    def __init__(self, json_raw_data=None, json_path="data/raw_rapminerz.json"):
        self.json_path = json_path
        self.json_raw_data = json_raw_data

    def load_json_file(self):
        try:
            with open(self.json_path) as json_file:
                self.json_raw_data = json.load(json_file)
        except OSError as exception:
            print(exception)

    def clean_json(self):
        df_rapminerz = pd.DataFrame(self.json_raw_data)
        
        # clean date
        df_rapminerz['date'] = df_rapminerz['date'].apply(lambda date: date.split(" ")[0])
        
        # remove feat with empty featured_artists_names list
        df_rapminerz = df_rapminerz[df_rapminerz['featured_artists_names'].astype(bool)]
        
        # empty date
        
        
        self.json_transformed_data = df_rapminerz.to_json(orient="records")

    def save_transformed_data(self):
        try:
            with open('data/rapminerz.json', 'w') as f:
                json.dump(self.json_transformed_data, f)
        except OSError as exception:
            print(exception)

    def transform(self, save=True):
        if not self.json_raw_data:
            self.load_json_file()
        self.clean_json()
        if save:
            self.save_transformed_data()
        return self.json_transformed_data

if __name__=='__main__':
    transform = Transform()
    transform.transform()