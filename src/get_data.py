import requests
import pandas as pd

bangalore_coordinates_string: str = '''"Point(77.55273 12.98313)"'''

with open('queries/bangalore_query.sparql', 'r') as f:
    query = f.read()
print(query)

url = "https://query.wikidata.org/sparql"
headers = {
    "User-Agent":
    "geogame-image-fetcher/1.0 (juliusniemeyer1995@gmail.com) python requests"
}
r = requests.get(url,
                 params={
                     'format': 'json',
                     'query': query
                 },
                 headers=headers)
r = r.json()
bindings_list = r['results']['bindings']

def get_value(x, key):
    try:
        return x[key]['value']
    except KeyError:
        return ''
df = pd.DataFrame()
for key in bindings_list[0].keys():
    print(key)
    df[key] = [get_value(x,key) for x in bindings_list]
df.to_csv('data/bengaluru_test.csv',index=False)


# item_list = [x['itemLabel']['value'] for x in bindings_list]
# article_en_list = [x['articleEN']['value'] for x in bindings_list]
# article_de_list = [x['articleDE']['value'] for x in bindings_list]
# lat_list = [x['lat']['value'] for x in bindings_list]
# lon_list = [x['lon']['value'] for x in bindings_list]
# sitelinks_list = [x['sitelinks']['value'] for x in bindings_list]
# thing_list = [x['thingLabel']['value'] for x in bindings_list]


# item,itemLabel,lat,lon,location,distance,sitelinks,thingLabel,thing,articleEN,articleDE
