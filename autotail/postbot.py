import time
import random
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from abc import ABC, abstractmethod
import traceback

import numpy as np
import scipy.interpolate as interp


class PostBot(ABC):
    def __init__(
        self,
        url: str,
        locator_dict: dict,
        email: str,
        story: str,
        headless: bool = True,
    ):
        self._tracebacks = True

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

        self.options.add_argument(
            "--disable-dev-shm-usage"
        )  # // overcome limited resource problems

        if headless:
            self.options.add_argument("--headless")

        # vary window size slightly to avoid obvious fingerprinting
        width, height = random.randint(1800, 1920), random.randint(900, 1080)
        self.options.add_argument(f"--window-size={width},{height}")

        self.browser = webdriver.Chrome(
            ChromeDriverManager().install(), options=self.options
        )
        self.random_sleep()
        self.browser.refresh()
        self.random_sleep()
        self.browser.get(self.browser.current_url)
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

    def random_sleep(self, min=0.25, max=1.0):
        time.sleep(random.random() * (max - min) + min)

    def random_mouse_jitter(self, target, minpx=10, maxpx=200):
        # dict of X, Y coordinates
        coords = target.location_once_scrolled_into_view
        self.browser.execute_script(f"window.scrollTo({coords['x']}, {coords['y']});")

        xs, ys = self._make_spline()

        logging.info(f"Doing mouse movement with spline length: {len(xs)}")
        x0, y0 = (random.randint(10, 100), random.randint(10, 100))
        logging.debug(f"Moving to {x0}, {y0}")
        ActionChains(self.browser).move_to_element_with_offset(target, x0, y0)
        for x, y in zip(xs, ys):
            ActionChains(self.browser).move_by_offset(x, y).perform()
            logging.debug(f"Moving by {x}, {y}")
        self.random_sleep()
        ActionChains(self.browser).move_to_element(target).perform()

    # stolen from https://stackoverflow.com/a/48690652
    def _make_spline(self):
        length = 50
        # Curve base:
        points = [[0, 0], [0, 2], [2, 3], [4, 0], [6, 3], [8, 2], [8, 0]]
        # points = [[0, 0], [0, 2], [8, 2], [8, 0]]
        points = np.array(points)

        x = points[:, 0]
        y = points[:, 1]

        t = range(len(points))
        ipl_t = np.linspace(0.0, len(points) - 1, length)

        x_tup = interp.splrep(t, x, k=3)
        y_tup = interp.splrep(t, y, k=3)

        x_list = list(x_tup)
        xl = x.tolist()
        x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        yl = y.tolist()
        y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

        x_i = interp.splev(ipl_t, x_list)
        y_i = interp.splev(ipl_t, y_list)

        return (x_i, y_i)

    def sleep_until_clickable(self, element: str, timeout: int = 10):
        """Note, use the string name of the slement rather than the located self.element"""
        WebDriverWait(self.browser, timeout).until(
            EC.element_to_be_clickable(self.locator_dictionary[element])
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
                    WebDriverWait(self.browser, self.timeout).until(
                        EC.visibility_of_element_located(locator)
                    )
                except (TimeoutException, StaleElementReferenceException):
                    if self._tracebacks:
                        traceback.print_exc()
                # I could have returned element, however because of lazy loading, I am seeking the element before return
                return self._find_element(*locator)

        except AttributeError:
            super(PostBot, self).__getattribute__("method_missing")(what)


class PostBotError(ValueError):
    """Any error with PostBot"""
