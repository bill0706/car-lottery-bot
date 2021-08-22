import logging
import os

from selenium import webdriver

from setting.function_wrapper import log_measure
from setting.log_handler import logger

folder_path = os.path.abspath(os.getcwd()) 


@log_measure
def set_level():
    level_path = folder_path + r"\data\關卡設定.txt"

    with open(level_path) as f:
        read_data = f.read()

    # Split default ignore '\n'
    level_list = read_data.split()

    # Check level 
    for level in level_list:
        int(level)
    
    logger.info("關卡規則: %s" %level_list)

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
    
    # Navigate to backend login web page
    driver.get("http://aabbcc24.com/")
    logger.info('請登入後台系統...')
    
    return driver


def user_login_prompt():
    logger.info("登入系統後，請開啟極速賽車後台頁面，再按下 'Enter' 鍵")
    
    while True:
        key_response = input('')
        
        if key_response == '':
            break
        else:
            logger.warning('輸入錯誤! 請重新輸入')
    
    logger.info("登入驗證成功!")


@log_measure
def check_login_page(driver):

    # Find tab in browser
    for window_id in driver.window_handles:
        driver.switch_to.window(window_id)

        if driver.title == '極速賽車':
            return driver
    
    # Close browser manually to prevent OSError
    driver.quit()

    raise SystemExit("driver.title == '極速賽車' not found")


@log_measure
def user_point_prompt(bet_details):
    while True:
        key_response = input('請輸入起始積分: ')
        
        try:
            point = int(key_response)
            if point >= 1:
                break
        
        except:
            logger.warning('輸入錯誤! 請重新輸入')
    
    bet_details.point = point

    logger.info('輸入成功，等待進場...')

    return bet_details