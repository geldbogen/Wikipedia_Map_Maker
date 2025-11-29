import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
import os

def setup_driver():
    """Setup Chrome driver with undetected_chromedriver"""
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    
    # Create driver with undetected_chromedriver
    driver = uc.Chrome(options=options, version_main=None)
    
    # Set timeouts
    driver.set_page_load_timeout(180)
    driver.implicitly_wait(15)
    
    return driver

def fetch_country(country_name: str):
    driver = setup_driver()
    
    df_complete = pd.DataFrame()
    try:
        for i in range(1, 100):
            time.sleep(8)  # Longer delay to appear more human-like
            starting_point = f'https://www.atlasobscura.com/things-to-do/{country_name}/places?page={i}'
            print('This is the starting point URL:')
            print(starting_point)
            
            retry_count = 0
            max_retries = 3
            page_success = False
            
            while retry_count < max_retries and not page_success:
                try:
                    driver.get(starting_point)
                    
                    # Wait for page to be ready
                    wait = WebDriverWait(driver, 40)
                    
                    # First wait for the page body to load
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    
                    # Give the page extra time to render JavaScript and bypass Cloudflare
                    time.sleep(5)
                    
                    # Check if we hit Cloudflare protection
                    page_source = driver.page_source.lower()
                    if "cloudflare" in page_source or "security" in page_source or "checking your browser" in page_source:
                        print("Detected Cloudflare protection, waiting longer...")
                        time.sleep(10)
                    
                    # Try to find cards with multiple possible selectors
                    cards = None
                    possible_selectors = [
                        'a.Card',
                        'a[class*="Card"]',
                        'div.content-card',
                        'article',
                        'a[href*="/places/"]'
                    ]
                    
                    for selector in possible_selectors:
                        try:
                            cards = driver.find_elements(By.CSS_SELECTOR, selector)
                            if cards and len(cards) > 0:
                                print(f'Found {len(cards)} elements with selector: {selector}')
                                break
                        except NoSuchElementException:
                            continue
                    
                    # If no cards found, we've reached the end
                    if not cards or len(cards) == 0:
                        print(f"No cards found on page {i}, ending scrape")
                        return df_complete
                    
                    print(f'Processing {len(cards)} cards on page {i}')
                    
                    # Extract data from cards
                    ao_links = []
                    lats = []
                    lons = []
                    item_labels = []
                    descriptions = []
                    
                    for card in cards:
                        try:
                            href = card.get_attribute('href')
                            ao_links.append(href if href else '')
                            
                            lat = card.get_attribute('data-lat')
                            lon = card.get_attribute('data-lng')
                            lats.append(lat if lat else '')
                            lons.append(lon if lon else '')
                            
                            # Get title
                            title_text = ''
                            title_selectors = ['h3.Card__heading', 'h3', '.Card__heading', '[class*="heading"]']
                            for title_sel in title_selectors:
                                try:
                                    title_element = card.find_element(By.CSS_SELECTOR, title_sel)
                                    title_text = title_element.text.strip()
                                    if title_text:
                                        break
                                except NoSuchElementException:
                                    continue
                            item_labels.append(title_text)
                            
                            # Get description
                            desc_text = ''
                            desc_selectors = ['div.Card__content', '.Card__content', 'p', '[class*="content"]']
                            for desc_sel in desc_selectors:
                                try:
                                    desc_element = card.find_element(By.CSS_SELECTOR, desc_sel)
                                    desc_text = desc_element.text.strip()
                                    if desc_text:
                                        break
                                except NoSuchElementException:
                                    continue
                            descriptions.append(desc_text)
                                
                        except Exception as e:
                            print(f"Error processing card: {e}")
                            ao_links.append('')
                            lats.append('')
                            lons.append('')
                            item_labels.append('')
                            descriptions.append('')
                    
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
                    page_success = True
                    
                except TimeoutException:
                    retry_count += 1
                    print(f"Timeout on page {i} (retry {retry_count}/{max_retries})")
                    if retry_count < max_retries:
                        print(f"Waiting 20 seconds before retry...")
                        time.sleep(20)
                        
                except Exception as e:
                    retry_count += 1
                    print(f"Error on page {i} (retry {retry_count}/{max_retries}): {e}")
                    
                    if retry_count < max_retries:
                        print(f"Waiting 20 seconds before retry...")
                        time.sleep(20)
                    else:
                        break
        
        os.makedirs('data/ao_country_data', exist_ok=True)
        output_file = f'data/ao_country_data/ao_{country_name}.csv'
        df_complete.to_csv(output_file, index=False)
        print(f"Saved {len(df_complete)} records to {output_file}")
        
        return df_complete
        
    finally:
        os.makedirs('data/ao_country_data', exist_ok=True)
        output_file = f'data/ao_country_data/ao_{country_name}.csv'
        df_complete.to_csv(output_file, index=False)
        print(f"Saved {len(df_complete)} records to {output_file}")
        
        try:
            driver.quit()
        except:
            pass

if __name__ == '__main__':
    fetch_country('Germany')