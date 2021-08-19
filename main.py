import os

from selenium import webdriver

from utility.function_wrapper import log_measure

folder_path = os.path.abspath(os.getcwd()) 


@log_measure
def set_level():
    level_path = folder_path + r"\data\關卡設定.txt"

    with open(level_path) as f:
        read_data = f.read()

    # split default ignore '\n'
    level_list = read_data.split()

    # check level 
    for level in level_list:
        int(level)

    return level_list


@log_measure
def open_browser():
    browser_path = folder_path + r"\Application\chrome.exe"
    driver_path = folder_path + r"\Application\chromedriver"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.binary_location = browser_path
    
    driver = webdriver.Chrome(executable_path = driver_path, options = chrome_options)
    driver.implicitly_wait(3)
    
    return driver


def init():
    level_list = set_level()
    driver = open_browser()


if __name__ == '__main__':
    init()