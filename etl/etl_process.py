from etl.extract import Extract
from etl.transform import Transform
from etl.load import Load

def etl(save_raw=True, save_structured=True):
        '''
        Entire ETL process.
        '''
        extract = Extract(url="https://apps-dev.rapminerz.io/data-ensai/")
        raw_json = extract.extract(save=save_raw)
        transform = Transform(json_raw_data=raw_json)
        rapminerz_json = transform.transform(save=save_structured)
        load = Load(rapminerz_json)
        load.load()

if __name__ == '__main__':
    etl()