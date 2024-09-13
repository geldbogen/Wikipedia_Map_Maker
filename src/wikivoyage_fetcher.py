import requests
import wikitextparser as wtp
import pandas as pd
from geopy.geocoders import Nominatim

# 'https://en.wikipedia.org/wiki/Special:ApiSandbox#action=parse&format=json&page=house&prop=wikitext&section=3&disabletoc=1'


class WikivoyageFetcher():
    def __init__(self, to_fetch_place_name : str) -> None:
        self.to_fetch_place_name = to_fetch_place_name.lower()
        self.final_data_frame = pd.DataFrame()
        self.geolocator = Nominatim(user_agent="wikipedia-map-maker")
        pass

    def fetch(self) -> pd.DataFrame:
        return_frame = pd.DataFrame()
        content_dict = self.get_contents_of_wikivoyage_article()
        for index, line in content_dict.items():
            wikilist = self.get_wikilist_by_section_number(index)
            content_list = self.get_dictionary_list_of_wikitext(wikilist) 
            frame = self.get_dataframe_from_dictionary_list(content_list,line)
            self.fill_missing_coordinates_in_frame(frame)
            return_frame = pd.concat([return_frame,frame])
        

        return_frame['tier'] = return_frame.apply(lambda x : 'wikivoyage_' + x['description'], axis = 1)

        return return_frame

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

    def get_wikilist_by_section_number(self, section_number : int) -> wtp.WikiList | None:
        url_2 = 'https://en.wikivoyage.org/w/api.php'
        response = requests.get(url_2, params={
                                'action': 'parse', 'format': 'json',
                                'page': self.to_fetch_place_name, 'prop': 'wikitext',
                                'section' : str(section_number), 'disabletoc' : '1' })
        parsed = wtp.parse(response.json()['parse']['wikitext']['*'])
        try:
            wikilist = parsed.get_lists()[0]
        except IndexError:
            return None
        return wikilist

    def get_dictionary_list_of_wikitext(self, wikilist : wtp.WikiList | None) -> list[dict[str,str]]:
        
        if not wikilist:
            return [{}]

        dict_list : list[dict[str,str]] = []

        for entry in wikilist.items:
            print(entry)
            print(type(entry))
            my_dict : dict[str, str]= {}
            for thing in entry.split('|'):
                if not '=' in thing:
                    continue
                left_side = thing.split('=')[0].lstrip()
                right_side = thing.split('=')[1].replace('\n','').replace('}}','')
                my_dict[left_side] = right_side
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

        def help_function(pd_series : pd.Series):
            if (pd_series.at['lat'] == '' or pd_series.at['lon']) and pd_series.at['address'].lstrip() != '':
                location = self.geolocator.geocode(pd_series.at['address'] + ' ' + self.to_fetch_place_name)
                if location:
                    pd_series.at['lat'] = location.latitude
                    pd_series.at['lon'] = location.longitude

        df.apply(help_function,axis=1)

if __name__ == '__main__':
    my_voyage_fetcher = WikivoyageFetcher('Leipzig')
    df = my_voyage_fetcher.fetch()
    df.to_csv('test_wikivoyage_fetcher.csv')