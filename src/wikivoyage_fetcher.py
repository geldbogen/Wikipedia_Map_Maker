import re
from typing import Literal

import requests
import wikitextparser as wtp
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# 'https://en.wikipedia.org/wiki/Special:ApiSandbox#action=parse&format=json&page=house&prop=wikitext&section=3&disabletoc=1'


class WikivoyageFetcher():
    def __init__(self, to_fetch_place_name : str) -> None:
        print(to_fetch_place_name)
        self.to_fetch_place_name = to_fetch_place_name.replace(' ', '_')
        self.final_data_frame = pd.DataFrame()
        self.geolocator = Nominatim(user_agent="wikipedia-map-maker")
        self.geolocator.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds = 1)
        self.return_frame = pd.DataFrame()
        pass

    def fetch(self) -> pd.DataFrame:
        # self.return_frame = pd.DataFrame()
        content_dict = self.get_contents_of_wikivoyage_article()
        for index, line in content_dict.items():
            if line != 'Go next':
                pass
            if line == 'Districts':
                self.fetch_the_districts(index)
            list_of_wikilists = self.get_list_of_wikilists_by_section_number(index)
            for wikilist in list_of_wikilists:
                content_list = self.get_dictionary_list_of_wikitext(wikilist,headline='Go next') 
                frame = self.get_dataframe_from_dictionary_list(content_list,line)
                self.fill_missing_coordinates_in_frame(frame)
                self.return_frame = pd.concat([self.return_frame,frame])
        
        self.replace_duplicates_in_wikivoyage_frame(self.return_frame)

        self.return_frame['tier'] = self.return_frame.apply(lambda x : 'wikivoyage_' + x['description'], axis = 1)

        return self.return_frame

    def get_contents_of_wikivoyage_article(self) -> dict[str,str]:
        url = f'https://en.wikivoyage.org/w/api.php?action=parse&format=json&page={self.to_fetch_place_name}&prop=sections&disabletoc=1'

        response = requests.get(url)
        r = response.json()
        response_list_sections = r['parse']['sections']

        number_to_whole_item_dict = dict()
        for _ , entry in enumerate(response_list_sections):
            number_to_whole_item_dict[entry['number']] = entry.copy()
        
        for list_index, entry in enumerate(response_list_sections):
            number : str = entry['number']
        
            while '.' in number:
                to_add_number = (number.rsplit('.',1))[0]
                to_add_string = number_to_whole_item_dict.get(to_add_number).get('line')
                response_list_sections[list_index]['line'] = to_add_string + '_' + response_list_sections[list_index]['line']
                number = to_add_number
        
        return_dict = {x['index'] : x['line'] for x in response_list_sections}
        return return_dict

    def get_list_of_wikilists_by_section_number(self, section_number : int) -> list[wtp.WikiList] | None:
        url_2 = 'https://en.wikivoyage.org/w/api.php'
        response = requests.get(url_2, params={
                                'action': 'parse', 'format': 'json',
                                'page': self.to_fetch_place_name, 'prop': 'wikitext',
                                'section' : str(section_number), 'disabletoc' : '1' })
        parsed = wtp.parse(response.json()['parse']['wikitext']['*'])
        try:
            wikilist = parsed.get_lists()
        except IndexError:
            return None
        return wikilist

    def get_dictionary_list_of_wikitext(self, wikilist : wtp.WikiList | None, headline : Literal['Go next', ''] = '') -> list[dict[str,str]]:
        
        if not wikilist:
            return [{}]

        dict_list : list[dict[str,str]] = []

        for entry in wikilist.items:
            
            print(entry)
            print(type(entry))

            my_dict : dict[str, str]= {}
            
            # check the case for an ordinary wikivoyage item:
            if entry.strip().startswith('{{'):
                for thing in entry.split('|'):
                    if not '=' in thing:
                        continue
                    left_side = thing.split('=')[0].lstrip()
                    right_side = thing.split('=')[1].replace('\n','').replace('}}','')
                    my_dict[left_side] = right_side
            elif '[[' in entry:
                my_dict['name'] = re.findall(r'[^\[\]]*', entry)[3]
                print(re.findall(r'[^\[\]]*', entry))
                my_dict['content'] = entry.strip().replace('[[','').replace(']]','')

            dict_list.append(my_dict.copy())
        return dict_list

    def get_dataframe_from_dictionary_list(self, dict_list : list[dict[str,str]], category : str) -> pd.DataFrame:
        return_frame = pd.DataFrame()
        return_frame['itemLabel'] = [x.get('name', '--') for x in dict_list]
        return_frame['lat'] = [x.get('lat', '') for x in dict_list]
        return_frame['lon'] = [x.get('long', '') for x in dict_list]
        return_frame['address'] = [x.get('address', '') for x in dict_list]
        return_frame['url'] = [x.get('url', '') for x in dict_list]
        return_frame['thingLabel'] = [category] * len(return_frame.index.to_list())
        return_frame['description'] = [x.get('content', '') for x in dict_list]

        return return_frame

    def fill_missing_coordinates_in_frame(self, df : pd.DataFrame):
    # TODO add Geoogle Maps support if ordinary lookup fails
    
        def help_function(pd_series : pd.Series):
            if (pd_series.at['lat'].strip() == '' or pd_series.at['lon'].strip() == ''):
                
                if pd_series.at['address'].strip() == '':
                    
                    if 'Go next' in pd_series.at['thingLabel']:
                        location = self.geolocator.geocode(self.prepare_address_string_for_geocode(pd_series.at['itemLabel']))
                    else:
                        location = self.geolocator.geocode(self.prepare_address_string_for_geocode(pd_series.at['itemLabel']) + ' ' + self.to_fetch_place_name)
                    
                    
                    if not location:
                        location = self.geolocator.geocode(pd_series.at['itemLabel'])
                else:
                    location = self.geolocator.geocode(self.prepare_address_string_for_geocode(pd_series.at['address']) + ' ' + self.to_fetch_place_name)
                
                if location:
                    x = location.latitude
                    y = location.longitude
                else:
                    x, y = 0, 0

            else:
                try:

                    x = float(pd_series.at['lat'].strip())
                    y = float(pd_series.at['lon'].strip())
                except ValueError:
                    x, y = 0, 0
                
            return (x,y)
        df['fetched_coordinates'] = df.apply(help_function,axis=1)
        df['lat'] = df.apply(lambda x : x.at['fetched_coordinates'][0],axis=1)
        df['lon'] = df.apply(lambda x : x.at['fetched_coordinates'][1],axis=1)
    
    def prepare_address_string_for_geocode(self, address_string : str) -> str:
        address_string = address_string.strip()
        address_string = address_string.lstrip('ul. ')
        address_string = address_string.strip('"')
        # address_string = address_string.strip('ul. ')
        return address_string
    
    def replace_duplicates_in_wikivoyage_frame(self, wikivoyage_frame : pd.DataFrame):
        wikivoyage_frame = wikivoyage_frame.iloc[::-1]
        wikivoyage_frame = wikivoyage_frame.drop_duplicates(subset=['fetched_coordinates'])
    
    def fetch_the_districts(self, section_number : int):
        url_2 = 'https://en.wikivoyage.org/w/api.php'
        response = requests.get(url_2, params={
                                'action': 'parse', 'format': 'json',
                                'page': self.to_fetch_place_name, 'prop': 'wikitext',
                                'section' : str(section_number), 'disabletoc' : '1' })
        parsed = wtp.parse(response.json()['parse']['wikitext']['*'])
        for link in parsed.wikilinks:
            district_name = link.target
            new_fetcher = WikivoyageFetcher(district_name)
            self.return_frame = pd.concat([self.return_frame,new_fetcher.fetch()])

        
if __name__ == '__main__':
    my_voyage_fetcher = WikivoyageFetcher('Lucknow')
    df = my_voyage_fetcher.fetch()
    df.to_csv('test_wikivoyage_fetcher.csv')