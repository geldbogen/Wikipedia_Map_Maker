import pandas as pd
import 

def check_if_unimportant_things_like_colleges_or_hotels(pd_series : pd.Series) -> bool:
    sitelinks = pd_series['sitelinks']
    match pd_series['thingLabel']:
        case 'hotel' if sitelinks < 10:
            return True
        case 'college' if sitelinks < 10:
            return True
        case _:
            return False