from typing import Tuple

import sys, os, time

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import By
from selenium.webdriver.common.keys import Keys

from config.firefox import get_driver_config

from lib.constants import *

from lib.utils import sleep_random


class Service(object):
    def __init__(self, url, timeout):
        self.timeout = timeout
        self.url = url if url else USER_URL
        self.driver = get_driver_config()

    def load_page(self) -> None:
        self.driver.get(self.url)

    def handle_popup(self) -> None:
        # wait for pop-up to appear
        self.wait_element_present((By.XPATH, COOKIES_XPATH))

        button = self.driver.find_element_by_xpath(COOKIES_XPATH)
        button.click()

    def send_message(self, message: str) -> None:
        self.wait_element_present((By.NAME, TELL_NAME))

        message_box = self.driver.find_element_by_name(TELL_NAME)
        message_box.clear()
        message_box.send_keys(message)
        # Tell browser to hit `enter` key to submit message
        message_box.send_keys(Keys.CONTROL + Keys.ENTER)

    def validate_message(self) -> bool:
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(expected_conditions.title_is("Tellonym"))
        return True

    def wait_element_present(self, locator: Tuple[str, str]) -> None:
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(expected_conditions.presence_of_element_located(locator))

    def wait_element_visible(self, locator: Tuple[str, str]) -> None:
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(expected_conditions.visibility_of_element_located(locator))

    def search_by_xpath(self, locator: Tuple[str, str]) -> None:
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(expected_conditions.presence_of_element_located(locator))

    def close_browser_instance(self):
        if self.driver.service:
            self.driver.quit()
