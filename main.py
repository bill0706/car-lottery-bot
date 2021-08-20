from utility.settings_handler import set_level, open_browser
from utility.time_handler import check_service_time


def init():
    level_list = set_level()
    driver = open_browser()
    check_service_time()
    driver.quit()


if __name__ == '__main__':
    init()