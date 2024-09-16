from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def fetch_country(country_name : str):

    df_complete = pd.DataFrame()
    for i in range(1,100):
        time.sleep(3)
        starting_point = f'https://www.atlasobscura.com/things-to-do/{country_name}/places?page={i}'
        response = requests.get(starting_point)
        if response.status_code == 500:
            break
        print(response)
        my_soup = BeautifulSoup(response.content, 'html.parser')
        found_all_list = my_soup.find_all('a', {'class' : 'Card'})

        # create dataframe
        df = pd.DataFrame()
        
        df['ao_link'] = ['https://www.atlasobscura.com' + x['href'] for x in found_all_list]
        df['lat'] = [x['data-lat'] for x in found_all_list]
        df['lon'] = [x['data-lng'] for x in found_all_list]
        df['itemLabel'] = [x.find('h3', {'class' : 'Card__heading'}, recursive = True).text for x in found_all_list]
        df['ao_description'] = [x.find('div', {'class' : 'Card__content'}, recursive = True).text for x in found_all_list]
        print(df)
        df_complete = pd.concat([df_complete, df])
        # df.to_csv('ao_test.csv', index=False)

        # for x in found_all_list:

        #     # link
        #     print(x['href'])

        #     # latitude
        #     print(x['data-lat'])

        #     # longitude
        #     print(x['data-lng'])

            
        #     a = x.find('h3', {'class' : 'Card__heading'}, recursive = True).text

        #     # description
        #     c = x.find('div', {'class' : 'Card__content'}, recursive = True).text
        #     print(a)
        #     break

    df_complete.to_csv(f'data/ao_country_data/ao_{country_name}.csv', index=False)