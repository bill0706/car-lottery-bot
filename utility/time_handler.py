from datetime import datetime

from setting.function_wrapper import log_measure


@log_measure
def check_service_time():
    datetime_now = datetime.now()
    hour_now = datetime_now.hour
    minute_now = datetime_now.minute
    mix_hours = hour_now + minute_now / 60

    # Unservice time: 04:01 ~ 08:30 
    if mix_hours > 4 and mix_hours <= 8.5:
        raise SystemExit('Not in service time')


