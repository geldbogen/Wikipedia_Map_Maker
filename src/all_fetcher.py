import os
import math

import pandas as pd
import geopy.distance
import simplekml

from cleaning import get_tier_and_color, check_if_unimportant_things_like_colleges_or_hotels
from wikidata_fetcher import WikidataFetcher
from kml_helper import KmlHelper

class AllFetcher():

    def __init__(self, place_name : str , country_name : str,  lat : float, lon : float) -> None:

        self.lat = lat
        self.lon = lon
        
        self.wikidata_fetcher = WikidataFetcher('queries/places_query.sparql','queries/graves_query.sparql',lat,lon)
        self.place_name = place_name
        self.country_name = country_name

    def go(self):
        places_df = self.wikidata_fetcher.fetch_table('places')
        graves_df = self.wikidata_fetcher.fetch_table('graves')
        relevant_ao_df = pd.read_csv(os.path.join('data', 'ao_country_data', f'ao_{self.country_name}.csv'.lower()))

        # cleaning
        relevant_ao_df = relevant_ao_df[relevant_ao_df.apply(lambda x : geopy.distance.distance((x['lat'],x['lon']),(self.lat, self.lon)).km < 50,axis = 1)]
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

        # now create a final, large file
        final_df = pd.concat([places_df, graves_df, relevant_ao_df])

        # google my maps has problems with reading float values

        def try_convert_to_int(value):
            try:
                return int(value)
            except ValueError:
                pass


        final_df['sitelinks'] = final_df['sitelinks'].apply(lambda x : try_convert_to_int(x))
        final_df.to_csv(os.path.join(folder_name,f'final_{self.place_name}.csv'))

        # create google maps kml file
        KmlHelper(final_df)

if __name__ == '__main__':
    my_all_fetcher = AllFetcher('Mumbai','India', 19.077511363070002, 72.92135126744137)
    my_all_fetcher.go()
    pass
