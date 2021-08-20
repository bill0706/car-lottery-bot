from functools import wraps
import sys
import time
import traceback

from utility.log_handler import logger

test_dict = {
    'set_level': '關卡設定錯誤',
    'open_browser': '開啟瀏覽器發生錯誤',
    'check_service_time': '非系統服務時間: 04:01 ~ 08:30'
}


def log_measure(func):
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
            logger.error(test_dict[func.__name__], extra=log_dict)
            sys.exit(1)
    
    return wrap