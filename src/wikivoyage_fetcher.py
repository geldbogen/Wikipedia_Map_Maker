import requests
import wikitextparser as wtp
import pandas as pd

# 'https://en.wikipedia.org/wiki/Special:ApiSandbox#action=parse&format=json&page=house&prop=wikitext&section=3&disabletoc=1'


class WikivoyageFetcher():
    def __init__(self, to_fetch_place_name : str) -> None:
        self.to_fetch_place_name = to_fetch_place_name
        self.final_data_frame = pd.DataFrame()
        pass

    def fetch(self) -> pd.DataFrame:
        content = self.get_contents_of_wikivoyage_article()
        


    def get_contents_of_wikivoyage_article(self):
        place_name = 'leipzig'
        url = f'https://en.wikivoyage.org/w/api.php?action=parse&format=json&page={place_name}&prop=sections&disabletoc=1'

        response = requests.get(url)
        r = response.json()
        response_list_sections = r['parse']['sections']

        number_to_whole_item_dict = dict()
        for _, entry in enumerate(response_list_sections):
        number_to_whole_item_dict[entry['number']] = entry.copy()
        for list_index, entry in enumerate(response_list_sections):
        number : str = entry['number']
        while '.' in number:
            to_add_number = (number.rsplit('.',1))[0]
            to_add_string = number_to_whole_item_dict.get(to_add_number).get('line')
            response_list_sections[list_index]['line'] = to_add_string + '_' + response_list_sections[list_index]['line']
            number = to_add_number
        
        return_frame = {x['index'] : x['line'] for x in response_list_sections}
        return return_frame

    def get_wikilist_by_section_number(self, section_number : int) -> wtp.WikiList:
        url_2 = 'https://en.wikivoyage.org/w/api.php'
        response = requests.get(url_2, params={
                                'action': 'parse', 'format': 'json',
                                'page': self.to_fetch_place_name, 'prop': 'wikitext',
                                'section' : str(section_number), 'disabletoc' : '1' })
        parsed = wtp.parse(response.json()['parse']['wikitext']['*'])
        wikilist = parsed.get_lists()[0]
        return wikilist

    def get_dictionary_list_of_wikitext(self, wikilist : wtp.WikiList) -> list[dict[str,str]]:

        dict_list : list[dict[str,str]] = []

        for entry in wikilist.items:
            print(entry)
            print(type(entry))
            my_dict : dict[str, str]= {}
            for thing in entry.split('|'):
                if not '=' in thing:
                    continue
                left_side = thing.split('=')[0].lstrip()
                right_side = thing.split('=')[1].replace('\n','')
                my_dict[left_side] = right_side
            dict_list.append(my_dict.copy())
        return dict_list

    def get_dataframe_from_dictionary_list(self, dict_list : list[dict[str,str]], category : str) -> pd.DataFrame:
        return_frame = pd.DataFrame()
        return_frame['name'] = [x.get('name', '--') for x in dict_list]
        return_frame['lat'] = [x.get('lat', '') for x in dict_list]
        return_frame['lon'] = [x.get('long', '') for x in dict_list]
        return_frame['address'] = [x.get('address', '') for x in dict_list]
        return_frame['description'] = [x.get('content', '') for x in dict_list]
        return_frame['url'] = [x.get('url', '') for x in dict_list]

        return_frame['category'] = [category] * len(return_frame.index.to_list())

        return return_frame