from functools import wraps
import time
import traceback
from utility.log_handler import logger

test_dict = {
    '1': 'This is a warning',
    '2': 'This is an error'
}


def log_measure(func):
    log_dict = {'orignal_func': func.__name__}

    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.warning(test_dict['1'], extra=log_dict)
            return result
        except:
            # string traceback
            log_dict['traceback'] = traceback.format_exc()
            logger.error(test_dict['2'], extra=log_dict)
    return wrap