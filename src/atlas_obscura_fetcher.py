from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
import os

def setup_driver():
    """Setup Chrome driver with appropriate options"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def fetch_country(country_name: str):
    driver = setup_driver()
    
    try:
        df_complete = pd.DataFrame()
        
        for i in range(1, 100):
            time.sleep(5)  # Respectful delay between requests
            starting_point = f'https://www.atlasobscura.com/things-to-do/{country_name}/places?page={i}'
            print('This is the starting point URL:')
            print(starting_point)
            
            try:
                driver.get(starting_point)
                
                # Wait for the page to load and check for cards
                wait = WebDriverWait(driver, 10)
                cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.Card')))
                
                # If no cards found, we've reached the end
                if not cards:
                    print("No more cards found, ending scrape")
                    break
                
                print(f'Found {len(cards)} cards on page {i}')
                
                # Extract data from cards
                ao_links = []
                lats = []
                lons = []
                item_labels = []
                descriptions = []
                
                for card in cards:
                    try:
                        # Get link
                        href = card.get_attribute('href')
                        if href:
                            ao_links.append(href)
                        else:
                            ao_links.append('')
                        
                        # Get latitude and longitude
                        lat = card.get_attribute('data-lat')
                        lon = card.get_attribute('data-lng')
                        lats.append(lat if lat else '')
                        lons.append(lon if lon else '')
                        
                        # Get title
                        try:
                            title_element = card.find_element(By.CSS_SELECTOR, 'h3.Card__heading')
                            item_labels.append(title_element.text.strip())
                        except NoSuchElementException:
                            item_labels.append('')
                        
                        # Get description
                        try:
                            desc_element = card.find_element(By.CSS_SELECTOR, 'div.Card__content')
                            descriptions.append(desc_element.text.strip())
                        except NoSuchElementException:
                            descriptions.append('')
                            
                    except Exception as e:
                        print(f"Error processing card: {e}")
                        # Add empty values to maintain list consistency
                        ao_links.append('')
                        lats.append('')
                        lons.append('')
                        item_labels.append('')
                        descriptions.append('')
                
                # Create dataframe for this page
                df = pd.DataFrame({
                    'ao_link': ao_links,
                    'lat': lats,
                    'lon': lons,
                    'itemLabel': item_labels,
                    'description': descriptions
                })
                
                print('This is the atlas obscura df:')
                print(df)
                
                df_complete = pd.concat([df_complete, df], ignore_index=True)
                
            except TimeoutException:
                print(f"Timeout on page {i}, assuming we've reached the end")
                break
            except Exception as e:
                print(f"Error on page {i}: {e}")
                # Check if it's a 500 error or similar by looking at page content
                if "500" in driver.page_source or "error" in driver.title.lower():
                    print("Detected error page, stopping scrape")
                    break
                continue
        
        # Ensure data directory exists
        os.makedirs('data/ao_country_data', exist_ok=True)
        
        # Save the complete dataframe
        output_file = f'data/ao_country_data/ao_{country_name}.csv'
        df_complete.to_csv(output_file, index=False)
        print(f"Saved {len(df_complete)} records to {output_file}")
        
    finally:
        driver.quit()

if __name__ == '__main__':
    fetch_country('Germany')