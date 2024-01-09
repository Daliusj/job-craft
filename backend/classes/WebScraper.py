from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import validators

# config
BEUTIFULSOUP_FEATURES = "html.parser"
TIMING_DEFAULT = 10
WEB_SCRAPPER_MESSAGES = {
    "url_list_set": "WebScraper.url_list.setter: urls_list set to",
    "url_list_invalid": "WebScraper.url_list.setter: Invalid urls_list",
    "timing_set": "WebScraper.timing.setter: Timing set to",
    "timing_invalid": "WebScraper.timing.setter: Invalid time value. Time set to default value",
    "scraper_get": "WebScraper.get_soup: Getting",
    "scraper_cant_run": "WebScraper.get_soup: Can not run due to invalid urls",
    "scraper_exception": "WebScraper.get_soup: ",
    "url_invalid": "WebScraper.is_valid_url: ",
}


class WebScrapper:
    """
    This module provides a simple web scraper using Selenium and BeautifulSoup.
    It allows to scrape content from a list of URLs, with customizable timing between requests.
    The 'scrape' method is wrapped in a try-except block to catch any exceptions that may occur during the scraping process.
    If an exception is caught, an error message is logged using the provided logger instance.
    You can retrieve errors from the logger for further analysis.
    """

    def __init__(self, logger):
        self.logger = logger
        self._urls_list = []
        self._timing = TIMING_DEFAULT
        self._soups_list = []

    @property
    def urls_list(self):
        return self._urls_list

    @urls_list.setter
    def urls_list(self, urls_list):
        if self.is_valid_urls(urls_list):
            self.logger.log(
                f"{WEB_SCRAPPER_MESSAGES['url_list_set']} {urls_list}",
                level="INFO",
            )
            self._urls_list = urls_list
        else:
            self.logger.log(WEB_SCRAPPER_MESSAGES["url_list_invalid"], level="WARNING")
            self._urls_list = []

    def is_valid_urls(self, urls_list):
        result = []
        for url in urls_list:
            if validators.url(url):
                result.append(validators.url(url))
            else:
                self.logger.log(
                    f"{WEB_SCRAPPER_MESSAGES['url_invalid']} {validators.url(url)}",
                    level="ERROR",
                )
                result.append(False)

        return all(result)

    @property
    def timing(self):
        return self._timing

    @timing.setter
    def timing(self, time):
        if self.is_valid_time(time):
            self.logger.log(
                f"{WEB_SCRAPPER_MESSAGES['timing_set']} {time}", level="INFO"
            )
            self._timing = time
        else:
            self.logger.log(WEB_SCRAPPER_MESSAGES["timing_invalid"], level="WARNING")
            self._timing = TIMING_DEFAULT

    def is_valid_time(self, time):
        try:
            if time > 0:
                return True
        except TypeError:
            return False
        else:
            return False

    @property
    def soups_list(self):
        return self._soups_list

    @soups_list.setter
    def soups_list(self, soups_list):
        self._soups_list = soups_list

    def scrape(self):
        if not self.urls_list:
            self.logger.log(WEB_SCRAPPER_MESSAGES["scraper_cant_run"], level="WARNING")
        else:
            soups = []
            try:
                for index, url in enumerate(self.urls_list):
                    self.logger.log(
                        f"{WEB_SCRAPPER_MESSAGES['scraper_get']} {index} {url}",
                        level="INFO",
                    )
                    time.sleep(self.timing)
                    driver = webdriver.Chrome()
                    driver.get(url)
                    content = driver.page_source
                    driver.quit()
                    soup = bs(content, features=BEUTIFULSOUP_FEATURES)
                    soups.append(soup)
            except Exception as e:
                self.logger.log(
                    f"{WEB_SCRAPPER_MESSAGES['scraper_exception']} {e}",
                    level="ERROR",
                )
            else:
                self.soups_list = soups
