from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from fake_useragent import UserAgent


def get_driver_config() -> WebDriver:
    """
    Represents the default configuration for a Chrome webdriver
    :return: an instance of a Chrome WebDriver
    """
    options = webdriver.ChromeOptions()
    # Create and use a random user agent to avoid detection
    user_agent = UserAgent().random
    options.add_argument(f'user-agent={user_agent}')
    # Run chrome driver in headless mode so no browser window opens
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver