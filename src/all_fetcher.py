import os
import math

import pandas as pd
import geopy.distance
from geopy.geocoders import Nominatim
import simplekml

from cleaning import get_tier_and_color, check_if_unimportant_things_like_colleges_or_hotels
from wikidata_fetcher import WikidataFetcher
from kml_helper import KmlHelper
from wikivoyage_fetcher import WikivoyageFetcher
import atlas_obscura_fetcher

class AllFetcher():

    def __init__(self, place_name : str, country_name : str = '',  lat : float = 0.0, lon : float = 0.0, distance : int = 45) -> None:
        if (lat, lon) == (0.0 , 0.0):
            value = Nominatim(user_agent="wikipedia-map-maker").geocode(place_name)
            if value:
                self.lat, self.lon = value.latitude, value.longitude
            else:
                self.lat, self.lon = 0.0, 0.0
        else:
            self.lat = lat
            self.lon = lon
        self.distance = distance
        
        self.wikidata_fetcher = WikidataFetcher('queries/places_query.sparql','queries/graves_query.sparql',self.lat,self.lon,distance)
        self.wikivoyage_fetcher = WikivoyageFetcher(place_name)
        self.place_name = place_name

        if country_name == '':
            value = Nominatim(user_agent="wikipedia-map-maker").reverse(f'{self.lat},{self.lon}').raw['address']['country']
            if value:
                self.country_name = value
        else:
            self.country_name = country_name

    def go(self):
        places_df = self.wikidata_fetcher.fetch_table('places')
        graves_df = self.wikidata_fetcher.fetch_table('graves')
        try:
            relevant_ao_df = pd.read_csv(os.path.join('data', 'ao_country_data', f'ao_{self.country_name}.csv'.lower()))
        except FileNotFoundError:
            atlas_obscura_fetcher.fetch_country(self.country_name)
            relevant_ao_df = pd.read_csv(os.path.join('data', 'ao_country_data', f'ao_{self.country_name}.csv'.lower()))

        wikivoyage_df = self.wikivoyage_fetcher.fetch()
        # wikivoyage_df = pd.DataFrame()
        


        # cleaning
        relevant_ao_df = relevant_ao_df[relevant_ao_df.apply(lambda x : geopy.distance.distance((x['lat'],x['lon']),(self.lat, self.lon)).km < self.distance, axis = 1)]
        places_df = places_df[places_df.apply(lambda x: not check_if_unimportant_things_like_colleges_or_hotels(x),axis=1)]

        # drop duplicates
        places_df.drop_duplicates(inplace=True,subset=['item'])
        graves_df.drop_duplicates(inplace=True,subset=['item'])


        # get tiers and colors for convenience
        places_df['tier'] = places_df.apply(lambda x : get_tier_and_color(x,'places')[0], axis=1)
        places_df['color'] = places_df.apply(lambda x : get_tier_and_color(x,'places')[1], axis=1)

        graves_df['tier'] = graves_df.apply(lambda x : get_tier_and_color(x,'graves')[0], axis=1)
        graves_df['color'] = graves_df.apply(lambda x : get_tier_and_color(x,'graves')[1], axis=1)

        relevant_ao_df['tier'] = relevant_ao_df.apply(lambda x : get_tier_and_color(x,'atlas_obscura')[0], axis=1)
        relevant_ao_df['color'] = relevant_ao_df.apply(lambda x : get_tier_and_color(x,'atlas_obscura')[1], axis=1)

        wikivoyage_df['tier'] = wikivoyage_df.apply(lambda x : get_tier_and_color(x,'wikivoyage')[0], axis=1)
        wikivoyage_df['color'] = wikivoyage_df.apply(lambda x : get_tier_and_color(x,'wikivoyage')[1], axis=1)



        # saving
        folder_name = os.path.join('data',self.place_name)
        try:
            os.mkdir(folder_name)
        except FileExistsError:
            pass

        # save single files
        places_df.to_csv(os.path.join(folder_name,f'{self.place_name}_places.csv'))
        graves_df.to_csv(os.path.join(folder_name,f'{self.place_name}_graves.csv'))
        relevant_ao_df.to_csv(os.path.join(folder_name,f'{self.place_name}_ao.csv'))
        wikivoyage_df.to_csv(os.path.join(folder_name,f'{self.place_name}_wikivoyage.csv'))

        # now create a final, large file
        final_df = pd.concat([places_df, graves_df, relevant_ao_df, wikivoyage_df])

        # google my maps has problems with reading float values

        def try_convert_to_int(value):
            try:
                return int(value)
            except ValueError:
                pass


        final_df['sitelinks'] = final_df['sitelinks'].apply(lambda x : try_convert_to_int(x))
        final_df.to_csv(os.path.join(folder_name,f'final_{self.place_name}.csv'))

        # disable D Tier because of limitations in google my maps (yet again) (optional)
        final_df = final_df[final_df['tier'] != 'D']

        # create google maps kml file
        KmlHelper(self.place_name, final_df)

if __name__ == '__main__':
    my_all_fetcher = AllFetcher('Kolkata', distance=5)
    my_all_fetcher.go()
