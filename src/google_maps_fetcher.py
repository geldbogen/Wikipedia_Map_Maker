import requests
import pandas as pd

# load env
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
GOOGLE_MAPS_API_KEY = os.getenv(('maps_api_key'), 'ERROR_FETCHING_KEY')

class GoogleMapsFetcher:
    def __init__(self, api_key: str = GOOGLE_MAPS_API_KEY):
        self.api_key = api_key
    def search_nearby_places(self, latitude, longitude, radius=2000.0, included_types=None) -> pd.DataFrame:
        """
        Search for nearby places using Google Maps Places API (New).
        
        Args:
        latitude: Center point latitude
        longitude: Center point longitude
        radius: Search radius in meters (default: 2000.0)
        included_types: List of place types to include (default: ["restaurant"])
    
    Returns:
        pandas DataFrame with place information
        with the following columns:
            - name
            - rating
            - user_rating_count
            - latitude
            - longitude
            - price_level
    """
        if included_types is None:
            included_types = ["restaurant"]
        
        url = 'https://places.googleapis.com/v1/places:searchNearby'
        
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': GOOGLE_MAPS_API_KEY,
            'X-Goog-FieldMask': 'places.displayName,places.rating,places.location,places.userRatingCount,places.priceLevel'
        }
        
        payload = {
            "includedTypes": included_types,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": latitude,
                        "longitude": longitude
                    },
                    "radius": radius
                }
            }
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        df = create_dataframe_from_response(response.json())
        
        df = df[(df['rating'] >= 4.8) & (df['user_rating_count'] >= 500)]
        return df


def create_dataframe_from_response(response_json):
    """
    Convert Google Maps API response to a pandas DataFrame.
    
    Args:
        response_json: JSON response from the API
    
    Returns:
        pandas DataFrame with place information
    """
    # Price level mapping (Google uses PRICE_LEVEL_FREE to PRICE_LEVEL_VERY_EXPENSIVE)
    price_level_map = {
        'PRICE_LEVEL_FREE': 'Free',
        'PRICE_LEVEL_INEXPENSIVE': '€',
        'PRICE_LEVEL_MODERATE': '€€',
        'PRICE_LEVEL_EXPENSIVE': '€€€',
        'PRICE_LEVEL_VERY_EXPENSIVE': '€€€€',
        'PRICE_LEVEL_UNSPECIFIED': 'N/A'
    }
    
    places = response_json.get('places', [])
    
    data = []
    for place in places:
        price_level = place.get('priceLevel', 'PRICE_LEVEL_UNSPECIFIED')
        data.append({
            'name': place.get('displayName', {}).get('text', 'N/A'),
            'rating': place.get('rating', None),
            'user_rating_count': place.get('userRatingCount', None),
            'latitude': place.get('location', {}).get('latitude', None),
            'longitude': place.get('location', {}).get('longitude', None),
            'price_level': price_level_map.get(price_level, 'ERROR')
        })
    
    return pd.DataFrame(data)


# # Example usage:
# if __name__ == "__main__":
#     result = search_nearby_places(49.460983, 11.061859)
#     print(result)
    
#     df = create_dataframe_from_response(result)
#     print("\nDataFrame:")
#     print(df)



