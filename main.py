from setting.bet import BetDetails
from utility.fetch_handler import first_fetch
from utility.settings_handler import set_level, open_browser, user_login_prompt, check_login_page, set_backend_page, user_point_prompt
from utility.time_handler import check_service_time
from utility.processer_handler import start_processer

def init():
    bet_details = BetDetails()
    bet_details.level_list = set_level()
    
    driver = open_browser()
    user_login_prompt()
    check_login_page(driver)
    set_backend_page(driver)
    
    bet_details = user_point_prompt(bet_details)
    check_service_time()

    return bet_details, driver

if __name__ == '__main__':
    bet_details, driver = init()
    loop_queue, api_dic = first_fetch()
    start_processer(loop_queue, api_dic, bet_details, driver)
    
    driver.quit()