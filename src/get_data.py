import requests
import pandas as pd

class wikidata_fetcher():
    def __init__(self, sparql_file_path: str, lat : float, lon : float) -> None:
        self.lat = lat
        self.lon = lon
        with open(sparql_file_path, 'r') as f:
            self.query = f.read()

    def get_value(self, x, key):
            try:
                return x[key]['value']
            except KeyError:
                return ''
     
    def get_wikidata_table(self) -> pd.DataFrame:
        old_coordinates_string: str = 'Point()'
        new_coordinate_string = f'Point({self.lon} {self.lat})'

        self.query = self.query.replace(old_coordinates_string,new_coordinate_string)

        url = "https://query.wikidata.org/sparql"
        headers = {
            "User-Agent":
            "geogame-image-fetcher/1.0 (juliusniemeyer1995@gmail.com) python requests"
        }
        r = requests.get(url,
                        params={
                            'format': 'json',
                            'query': self.query
                        },
                        headers=headers)
        r = r.json()
        bindings_list = r['results']['bindings']

        df = pd.DataFrame()
        for key in bindings_list[0].keys():
            print(key)
            df[key] = [self.get_value(x,key) for x in bindings_list]
        df['sitelinks'] = df['sitelinks'].apply(lambda x: int(x))
        df.to_csv(f'''data/{str(self.lat).replace('.','-')}_{str(self.lon).replace('.','-')}.csv''',index=False)
        return df