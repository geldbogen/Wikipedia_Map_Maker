from typing import Literal

import requests
import pandas as pd



class WikidataFetcher():
    def __init__(self, places_query_file_path: str, grave_query_file_path : str, lat : float, lon : float, distance : int = 45) -> None:
        self.lat = lat
        self.lon = lon
        self.distance = distance
        with open(places_query_file_path, 'r') as f:
            self.places_query = f.read()
        with open(grave_query_file_path, 'r') as f:
            self.grave_query = f.read()

    def get_value(self, x, key):
            try:
                return x[key]['value']
            except KeyError:
                return ''
     
    def fetch_table(self, what_to_fetch : Literal['places', 'graves']) -> pd.DataFrame:
        old_coordinates_string: str = 'Point()'
        new_coordinate_string = f'Point({self.lon} {self.lat})'

        new_distance_string = f'wikibase:radius "{self.distance}"'
        old_distance_string = 'wikibase:radius ""'
        match what_to_fetch:
            case  'places':
                self.query = self.places_query.replace(old_coordinates_string,new_coordinate_string)
                self.query = self.query.replace(old_distance_string,new_distance_string)
                print(self.query)
                
            case  'graves':
                self.query = self.grave_query.replace(old_coordinates_string,new_coordinate_string)
                self.query = self.query.replace(old_distance_string,new_distance_string)
            case _:
                raise KeyError

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
        if bindings_list != []:
            for key in bindings_list[0].keys():
                print(key)
                df[key] = [self.get_value(x,key) for x in bindings_list]
            df['sitelinks'] = df['sitelinks'].apply(lambda x : int(x))
            df.to_csv(f'''data/{str(self.lat).replace('.','-')}_{str(self.lon).replace('.','-')}.csv''',index=False)
        return df