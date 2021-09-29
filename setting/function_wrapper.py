from functools import wraps
import sys
import time
import traceback

from setting.log_handler import logger
from utility.thread_handler import close_thread, ThreadWithException, thread_list

driver_list = []
test_dict = {
    'set_level': '關卡設定錯誤',
    'open_browser': '開啟瀏覽器發生錯誤',
    'check_login_page': '錯誤，未開啟極速賽車後台頁面',
    'check_service_time': '錯誤，現在非系統服務時間: 04:01 ~ 08:30'

}


def log_measure(func):
    global thread_list, driver_list

    log_dict = {'orignal_func': func.__name__}

    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            # logger.warning(test_dict[func.__name__], extra=log_dict)
            
            return result
        except:
            # string traceback
            log_dict['traceback'] = traceback.format_exc()
            
            # Prevent no key error in logger print 
            if func.__name__ in test_dict.keys():
                logger.error(test_dict[func.__name__], extra=log_dict)
            else:
                logger.error('', extra=log_dict)

            # Close driver if existed
            for driver in driver_list:
                driver.quit()

            # Close threads if existed
            close_thread(func.__name__)

            sys.exit(1)
    
    return wrap