from datetime import datetime
import json
import logging
from queue import Queue
import time

from bs4 import BeautifulSoup
import requests

from setting.function_wrapper import log_measure
from setting.log_handler import logger
from utility.rule_handler import calculate_position
from utility.thread_handler import close_thread, ThreadWithException, thread_list 


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'api.apiose122.com',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}


@log_measure
def fetch_prize_api():
    response = requests.get("https://api.apiose122.com/pks/getPksDoubleCount.do?date=&lotCode=10037", headers=headers)
    api_dic = json.loads(response.text)

    return api_dic


@log_measure
def fetch_remaining_seconds(api_dic):

    # Get next prize datetime
    datetime_str = api_dic['result']['data']['drawTime']
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    next_prize_unixtime = datetime_obj.timestamp()
    now_unixtime = datetime.now().timestamp()
    remaining_seconds = next_prize_unixtime - now_unixtime

    return remaining_seconds


@log_measure
def fetch_prize_details(api_dic):

    # Get prize number
    prize_issue = api_dic['result']['data']['preDrawIssue']
    prize_str = api_dic['result']['data']['preDrawCode']
    prize_numbers = prize_str.split(',')

    return prize_numbers, prize_issue


@log_measure
def fetch_prize_loop(loop_queue, remaining_seconds):
    
    # First fetch, sleep first, then get next prize details
    logger.debug('[DEBUG] next prize remaining seconds: %s' %remaining_seconds)
    time.sleep(remaining_seconds + 5)

    while True:
        api_dic = fetch_prize_api()
        prize_numbers = fetch_prize_details(api_dic)
        
        # Put numbers first, then sleep to wait for next prize
        loop_queue.put(prize_numbers)

        remaining_seconds = fetch_remaining_seconds(api_dic)
        logger.debug('[DEBUG] next prize remaining seconds: %s' %remaining_seconds)
        time.sleep(remaining_seconds + 5)


@log_measure
def first_fetch():
    global thread_list

    api_dic = fetch_prize_api()
    remaining_seconds = fetch_remaining_seconds(api_dic)

    loop_queue = Queue()
    loop_thread = ThreadWithException(target=fetch_prize_loop, args=(loop_queue, remaining_seconds))
    thread_list.append(loop_thread)

    if remaining_seconds > 30:    
        loop_thread.start()

    # Wait next prize, sleep first(main and thread function)     
    else:
        # Remove the price details, wait for next prize in start_processer function
        api_dic = None

        # sleep in fetch_prize_loop function
        loop_thread.start()

        time.sleep(remaining_seconds + 5)
    
    return loop_queue, api_dic

