import time
import random
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from abc import ABC, abstractmethod


class PostBot(ABC):
    def __init__(self,
                 url: str,
                 locator_dict: dict,
                 email: str,
                 story: str,
                 headless: bool = True):
        self._tracebacks = True

        logging.info(f"creating postbot with url: {url}, email: {email}, story: {story}")

        if url is None:
            raise PostBotError("url is None")
        else:
            self.url = url
        if email is None:
            raise PostBotError("email is None")
        else:
            self.email = email
        if story is None:
            raise PostBotError("story is None")
        else:
            self.story = story
        if locator_dict is None:
            self.locator_dict = {}
        else:
            self.locator_dictionary = dict(locator_dict)

        self.options = Options()

        self.options.add_argument("--disable-dev-shm-usage") #// overcome limited resource problems

        if headless:
            self.options.add_argument("--headless")

        # vary window size slightly to avoid obvious fingerprinting
        width, height = random.randint(1800,1920), random.randint(900, 1080)
        self.options.add_argument(f"--window-size={width},{height}")

        self.browser = webdriver.Chrome(ChromeDriverManager().install(),
                                        options = self.options)
        self.timeout = 5

        logging.info("Created webdriver, loading page...")

        self.browser.get(self.url)

        self.__postinit__()

    def __postinit__(self):
        """For subclasses"""
        pass

    @abstractmethod
    def post_story(self):
        """Abstract method to do the work"""
        
    def random_sleep(self, min=0.25, max=1):
        time.sleep(random.random()*(max-min)+min)

    def sleep_until_clickable(self, element:str, timeout:int=10):
        """Note, use the string name of the slement rather than the located self.element"""
        WebDriverWait(
            self.browser, timeout
        ).until(
            EC.element_to_be_clickable(
                self.locator_dictionary[element]
            )
        )

    def quit(self, leaveopen=False):
        if not leaveopen:
            self.browser.close()
        self.browser.quit()

    def _find_element(self, *loc):
        return self.browser.find_element(*loc)

    def __getattr__(self, what):
        try:
            locator = self.locator_dictionary.get(what, False)
            if locator:
                try:
                    element = WebDriverWait(self.browser, self.timeout).until(
                        EC.presence_of_element_located(locator)
                    )
                except(TimeoutException, StaleElementReferenceException):
                    if self._tracebacks:
                        traceback.print_exc()

                try:
                    element = WebDriverWait(self.browser, self.timeout).until(
                        EC.visibility_of_element_located(locator)
                    )
                except(TimeoutException, StaleElementReferenceException):
                    if self._tracebacks:
                        traceback.print_exc()
                # I could have returned element, however because of lazy loading, I am seeking the element before return
                return self._find_element(*locator)

        except AttributeError:
            super(PostBot, self).__getattribute__("method_missing")(what)


class PostBotError(ValueError):
    """Any error with PostBot"""
