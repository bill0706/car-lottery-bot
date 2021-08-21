from datetime import datetime
import json
import logging

from bs4 import BeautifulSoup
import requests

from utility.function_wrapper import log_measure
from utility.log_handler import logger

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
    # get next prize datetime
    datetime_str = api_dic['result']['data']['drawTime']
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    next_prize_unixtime = datetime_obj.timestamp()
    now_unixtime = datetime.now().timestamp()
    remaining_seconds = next_prize_unixtime - now_unixtime

    return remaining_seconds


@log_measure
def first_fetch():
    api_dic = fetch_prize_api()
    remaining_seconds = fetch_remaining_seconds(api_dic)
    logger.debug('[DEBUG] next prize remaining seconds: %s' %remaining_seconds)


@log_measure
def fetch_prize_numbers():
    response = requests.get("https://api.apiose122.com/pks/getPksDoubleCount.do?date=&lotCode=10037", headers=headers)
    api_dic = json.loads(response.text)

    # get prize number
    prize_str = api_dic['result']['data']['preDrawCode']
    prize_list = prize_str.split(',')

    return prize_list