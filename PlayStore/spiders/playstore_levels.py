import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import scrapy
from scrapy_selenium import SeleniumRequest

class PlaystoreLevelsSpider(scrapy.Spider):
    name = "playstore_levels"

    # extra configuration
    allowed_domains = ["https://play.google.com/store/apps"]
    start_urls = ["https://playstore.com"]

    options = webdriver.ChromeOptions()

    # extra configuration
    options.binary_location = '/usr/bin/google-chrome'
    options.add_argument("headless")

    desired_capabilities = options.to_capabilities()
    driver = webdriver.Chrome(options=options)
    wait = 10
    first_page = None

    def start_requests(self):
        url = 'https://play.google.com'
        yield SeleniumRequest(url=url, callback=self.parse, wait_time=20)

    custom_settings = {'FEED_URI': "files/app-info-%(time)s.csv", 'FEED_FORMAT': 'csv'}

    xpath_string = None

    def parse(self, response):
        self.driver.get('https://play.google.com/store/apps')
        self.driver.implicitly_wait(self.wait)
        search_button = self.driver.find_element(By.XPATH, '//*[@id="kO001e"]/header/nav/div/div[1]/button/i')
        search_button.click()
        text_input = self.driver.find_element(By.XPATH, '//*[@id="kO001e"]/header/nav/c-wiz/div/div/label/input')
        text_input.send_keys(self.search_term)
        self.driver.find_element(By.CLASS_NAME, 'FfLSic').click()
        self.driver.implicitly_wait(self.wait)
        self.driver.get(self.driver.current_url)
        first_page_urls = self.search_urls()
        time.sleep(5)
        first_page_app_data = self.search_page_app_data(first_page_urls)
        return first_page_app_data


    def search_urls(self,):
        elements = self.driver.find_elements(By.CLASS_NAME, 'Si6A0c')
        urls = []
        for url in elements:
            urls.append(url.get_attribute('href'))
        return urls

    def yield_urls(self, url):
        data = {
            'url': url
        }
        return data
    def search_page_app_data(self, first_page_urls):
        length = len(first_page_urls)
        # time.sleep(2)
        try:
            for url in first_page_urls:
                self.driver.get(url)
                name = self.driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[5]/div/div/div[2]/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1').text
                dev_details = self.driver.find_element(By.XPATH, '//*[@id="developer-contacts-heading"]/div[2]/button/i')
                dev_details.click()
                try:
                    website = self.driver.find_element(By.XPATH, '//*[@id="developer-contacts"]/div/div[1]/div/a').get_attribute('href')
                    email = self.driver.find_element(By.XPATH, '//*[@id="developer-contacts"]/div/div[2]/div/a/div/div[2]').text
                except NoSuchElementException:
                    pass
                yield self.yield_elements(name, website, email)
        except Exception:
            pass
        return self.driver.close()

    def yield_elements(name, website, email):
        data = {
            'name': name,
            'website': website,
            'email': email,
            # 'link': link
        }
        return data

