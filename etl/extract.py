import requests
from json import dump


class Extract:
    def __init__(self, url="https://apps-dev.rapminerz.io/data-ensai/"):
        self.url = url
        self.json_raw_data = None

    def get_data(self):
        try:
            resp = requests.get(url=self.url)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        self.json_raw_data = resp.json()

    def save_raw_data(self):
        with open('data/raw_rapminerz.json', 'w') as f:
            dump(self.json_raw_data, f)

    def extract(self, save=True):
        self.get_data()
        if save:
            self.save_raw_data()
        return self.json_raw_data


if __name__ == '__main__':
    extract = Extract()
    extract.get_data()
    extract.save_raw_data()