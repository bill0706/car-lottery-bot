import os

from selenium import webdriver


def init():
    folder_path = os.path.abspath(os.getcwd())
    browser_path = folder_path + r"\Application\chrome.exe"
    driver_path = folder_path + r"\Application\chromedriver"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.binary_location = browser_path
    
    driver = webdriver.Chrome(executable_path = driver_path, options = chrome_options)
    driver.implicitly_wait(3)
    return driver


if __name__ == '__main__':
    driver = init()