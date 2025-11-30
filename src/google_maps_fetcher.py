import requests
import pandas as pd

# load env
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
GOOGLE_MAPS_API_KEY = os.getenv(('maps_api_key'), 'ERROR_FETCHING_KEY')

class GoogleMapsFetcher:
    def __init__(self, latitude: float, longitude: float, distance: int = 2, included_types=None, api_key: str = GOOGLE_MAPS_API_KEY):
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.distance = distance # in km
        self.included_types = included_types if included_types is not None else ["restaurant"]

        self.dict_thing_to_label = {
            'restaurant' : 'Eat',
            'bar' : 'Drink'
        }

    def fetch(self) -> pd.DataFrame:
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
        
        url = 'https://places.googleapis.com/v1/places:searchNearby'
        
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': GOOGLE_MAPS_API_KEY,
            'X-Goog-FieldMask': 'places.displayName,places.rating,places.location,places.userRatingCount,places.priceLevel'
        }
        
        payload = {
            "includedTypes": self.included_types,
            "maxResultCount": 200000,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": self.latitude,
                        "longitude": self.longitude
                    },
                    "radius": self.distance * 1000  # Convert km to meters
                }
            }
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        df = self.create_dataframe_from_response(response.json())
        
        df = df[(df['rating'] >= 4.8) & (df['user_rating_count'] >= 500)]
        return df


    def create_dataframe_from_response(self, response_json):
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
                'itemLabel': place.get('displayName', {}).get('text', 'N/A'),
                'thingLabel': self.dict_thing_to_label.get(self.included_types[0], 'N/A') if self.included_types else 'N/A',
                'rating': place.get('rating', None),
                'user_rating_count': place.get('userRatingCount', None),
                'lat': place.get('location', {}).get('latitude', None),
                'lon': place.get('location', {}).get('longitude', None),
                'price_level': price_level_map.get(price_level, 'ERROR')
            })
        
        df = pd.DataFrame(data)

        return df


# Example usage:
if __name__ == "__main__":
    # Example coordinates (Nuremberg, Germany)
    test_latitude = 49.460983
    test_longitude = 11.061859
    test_distance = 2  # km
    # Test with restaurants
    print("Fetching restaurants...")
    restaurant_fetcher = GoogleMapsFetcher(
        latitude=test_latitude,
        longitude=test_longitude,
        distance=test_distance,
        included_types=["restaurant"]
    )
    restaurants_df = restaurant_fetcher.fetch()
    print("\nRestaurants DataFrame:")
    print(restaurants_df)
    print(f"\nFound {len(restaurants_df)} highly-rated restaurants")
    
    # Test with bars
    print("\n" + "="*50)
    print("Fetching bars...")
    bar_fetcher = GoogleMapsFetcher(
        latitude=test_latitude,
        longitude=test_longitude,
        distance=test_distance,
        included_types=["bar"]
    )
    bars_df = bar_fetcher.fetch()
    print("\nBars DataFrame:")
    print(bars_df)
    print(f"\nFound {len(bars_df)} highly-rated bars")



