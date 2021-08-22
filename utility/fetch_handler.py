from datetime import datetime
import json
import logging
from queue import Queue
import time

from bs4 import BeautifulSoup
import requests

from utility.function_wrapper import log_measure
from utility.log_handler import logger
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
def start_processer(loop_queue, api_dic):
    # Used for first run
    queue_numbers = None

    # First run process
    prize_numbers, prize_issue = fetch_prize_details(api_dic)
    logger.debug("[DEBUG] First run, prize numbers: %s" %prize_numbers)

    while queue_numbers or api_dic is not None:
       
        # Enter in loop_queue.get() expression 
        if queue_numbers is not None:
            prize_numbers, prize_issue = queue_numbers
            logger.debug("[DEBUG] Run in while, prize numbers: %s" %prize_numbers)
        
        # Close the first run's door
        else:
            api_dic = None

        logger.info("第 %s 期 開獎號碼為 %s" %(prize_issue, prize_numbers))

        bet_num, bet_position = calculate_position(prize_numbers)
        logger.debug('[DEBUG] bet_num: %s, bet_position: %s ' %(bet_num, bet_position))

        # wait for the next prize numbers
        queue_numbers = loop_queue.get()



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
        start_processer(loop_queue, api_dic)

    # Wait next prize, sleep first(main and thread function)     
    else:

        # sleep in fetch_prize_loop function
        loop_thread.start()

        time.sleep(remaining_seconds + 5)
        start_processer(loop_queue, api_dic)
    
    

