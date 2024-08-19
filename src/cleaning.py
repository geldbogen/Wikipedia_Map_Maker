import pandas as pd

with open('data/almost_unimportant_tags.txt', 'r') as f:
    set_of_almost_unimportant_tags = set(f.read().splitlines())

print(set_of_almost_unimportant_tags)

with open('data/really_unimportant_tags.txt', 'r') as f:
    set_of_really_unimportant_tags = set(f.read().splitlines())

def check_if_unimportant_things_like_colleges_or_hotels(pd_series : pd.Series) -> bool:
    sitelinks = pd_series['sitelinks']
    match pd_series['thingLabel']:
        case _ if pd_series['articleDE'] == '' and pd_series['articleEN'] == '':
            return True
        case _ if pd_series['thingLabel'] in set_of_really_unimportant_tags:
            return True
        case _ if pd_series['thingLabel'] in set_of_almost_unimportant_tags and sitelinks < 10:
            return True
        case _:
            return False

def get_tier_and_color(sitelinks : int) -> tuple[str,str]:

    match sitelinks:
        case _ if sitelinks >= 20:
            return ('S','orange')
        case _ if sitelinks >= 10:
            return ('A','green')
        case _ if sitelinks >= 5:
            return ('B','violet')
        case _ if sitelinks >= 2:
            return ('C','yellow')
        case _ :
            return ('D','blue')