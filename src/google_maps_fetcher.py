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
        Fetches all available results using pagination.
        
        Returns:
            pandas DataFrame with place information
        """
        
        url = 'https://places.googleapis.com/v1/places:searchNearby'
        
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': 'places.displayName,places.rating,places.location,places.userRatingCount,places.priceLevel'  # Removed nextPageToken
        }
        
        payload = {
            "includedTypes": self.included_types,
            "maxResultCount": 20,  # Maximum per request
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": self.latitude,
                        "longitude": self.longitude
                    },
                    "radius": self.distance * 1000.0  # Convert km to meters
                }
            }
        }
        
        all_dataframes = []
        next_page_token = None
        
        while True:
            # Add pageToken to payload if we have one
            if next_page_token:
                payload["pageToken"] = next_page_token
            
            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(f"HTTP Error: {e}")
                print(f"Response: {response.text}")
                raise
            
            response_json = response.json()
            
            # Convert current page to dataframe
            df = self.create_dataframe_from_response(response_json)
            if not df.empty:
                all_dataframes.append(df)
            
            # Check for next page - nextPageToken is automatically included in response
            next_page_token = response_json.get('nextPageToken')
            if not next_page_token:
                break  # No more pages
            
            # Add a small delay between requests
            import time
            time.sleep(0.5)
        
        # Combine all pages
        if all_dataframes:
            df_combined = pd.concat(all_dataframes, ignore_index=True)
        else:
            df_combined = pd.DataFrame()
        
        # Apply filters
        df_filtered = df_combined[(df_combined['rating'] >= 4.8) & (df_combined['user_rating_count'] >= 500)]
        return df_filtered


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
        print(df)
        return df


# Example usage:
if __name__ == "__main__":
    # Example coordinates (Nuremberg, Germany)
    test_latitude = 49.460983
    test_longitude = 11.061859
    test_distance = 20  # km
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



