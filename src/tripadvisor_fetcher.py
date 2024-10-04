# later later

import selenium
import selenium.webdriver
import selenium.webdriver.firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


class TripAdvisorFetcher():
    def __init__(self) -> None:
        pass
        self.driver = uc.Chrome()

    def find_top_attractions(self, place_name : str, number : int = 15, ):
        self.driver.get('https://www.tripadvisor.com/')
        # self.driver.get(f'https://www.tripadvisor.com/Search?q={place_name}&geo=1&ssrc=a&searchNearby=false&searchSessionId=00173b91c768d120.ssid&blockRedirect=true&offset=0')


if __name__ == '__main__':
    my_tripadvisor_fetcher = TripAdvisorFetcher()
    my_tripadvisor_fetcher.find_top_attractions('Munich')
    
    pass

