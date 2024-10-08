from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import scrapy
from scrapy_selenium import SeleniumRequest


class PlaystoreSpider(scrapy.Spider):
    name = "playstore"

    # allowed_domains = ['https://play.google.com']

    def start_requests(self):
        url = 'https://play.google.com'
        yield SeleniumRequest(url=url, callback=self.parse, wait_time=20)

    custom_settings = {'FEED_URI': "test-file-%(time)s.csv",
                       'FEED_FORMAT': 'csv'}

    xpath_string = None

    def parse(self, response):
        driver = webdriver.Chrome()  # To open a new browser window and navigate it
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

        # Opening the website
        driver.get('https://play.google.com/store/apps')
        driver.implicitly_wait(10)
        # driver.find_element(By.XPATH, '//*[@id="kO001e"]/header/nav/div/div[1]/button').click()

        # Explicit wait
        wait = WebDriverWait(driver, 1000000)
        search_button = driver.find_element(By.XPATH, '//*[@id="kO001e"]/header/nav/div/div[1]/button/i')
        search_button.click()
        text_input = driver.find_element(By.XPATH, '//*[@id="kO001e"]/header/nav/c-wiz/div/div/label/input')
        text_input.send_keys('Social Media')
        text_input.send_keys(Keys.ENTER)
        driver.get(driver.current_url)
        driver.implicitly_wait(10)
        first_result = driver.find_element(By.XPATH,
                                           '//*[@id="yDmH0d"]/c-wiz[2]/div/div/c-wiz/c-wiz/c-wiz/section/div/div/div/div[1]/div/div/div/a')
        first_result.click()
        driver.implicitly_wait(10)
        import time
        time.sleep(5)
        recommended_apps = 1
        dev_details = driver.find_element(By.XPATH, '//*[@id="developer-contacts-heading"]/div[2]')
        dev_details.click()
        website = driver.find_element(By.XPATH, '//*[@id="developer-contacts"]/div/div[1]/div/a/div/div[2]').text
        email = driver.find_element(By.XPATH, '//*[@id="developer-contacts"]/div/div[2]/div/a/div/div[2]').text
        yield self.yield_elements(website, email)
        import time
        time.sleep(5)

        pass

    def yield_elements(self, website, email):
        data = {
            'website': website,
            'email': email
        }
        return data