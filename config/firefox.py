from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

from fake_useragent import UserAgent


def get_driver_config() -> WebDriver:
    """
    Represents the default configuration for a Firefox webdriver
    :return: an instance of a Firefox WebDriver
    """
    options = webdriver.FirefoxOptions()
    # Create and use a random user agent to avoid detection
    user_agent = UserAgent().random
    options.add_argument(f'user-agent={user_agent}')
    # Run firefox driver in headless mode so no browser window opens
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    return driver
