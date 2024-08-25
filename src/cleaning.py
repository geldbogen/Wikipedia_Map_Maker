from typing import Literal

import pandas as pd
import simplekml

with open('data/almost_unimportant_tags.txt', 'r') as f:
    set_of_almost_unimportant_tags = set(f.read().splitlines())

print(set_of_almost_unimportant_tags)

with open('data/really_unimportant_tags.txt', 'r') as f:
    set_of_really_unimportant_tags = set(f.read().splitlines())

def check_if_unimportant_things_like_colleges_or_hotels(pd_series : pd.Series) -> bool:
    sitelinks = pd_series['sitelinks']
    match pd_series['thingLabel']:
        case _ if pd_series.isna()['articleDE'].all() and pd_series.isna()['articleEN'].all():
            return True
        case _ if pd_series.at['thingLabel'] in set_of_really_unimportant_tags:
            return True
        case _ if pd_series.at['thingLabel'] in set_of_almost_unimportant_tags and sitelinks < 10:
            return True
        case _:
            return False

def create_styled_point(kml_folder : simplekml.Folder, coords : list[tuple], name : str, tier : str):
    
    kml_folder.newpoint(coords=coords, name=name)
    pass

def get_tier_and_color(pd_series : pd.Series, which_category : Literal['places','graves','atlas_obscura']) -> tuple[str,str]:

    match which_category:
        case 'places':
            match pd_series.get('sitelinks',-1):
                case _ if pd_series.get('sitelinks',-1) >= 20:
                    return ('S','orange')
                case _ if pd_series.get('sitelinks',-1) >= 10:
                    return ('A','green')
                case _ if pd_series.get('sitelinks',-1) >= 5:
                    return ('B','violet')
                case _ if pd_series.get('sitelinks',-1) >= 2:
                    return ('C','yellow')
                case _ if pd_series.get('sitelinks',-1) >= 2:
                    return ('C','yellow')
                case _ if pd_series.get('sitelinks',-1) == -1:
                    pass
                case _ :
                    return ('D','blue')
        case 'graves':
            return ('graves', 'black')
        case 'atlas_obscura':
            return ('atlas_obscura', 'gold')