import datetime
import logging
import os
import sys

console_level = logging.INFO
file_level = logging.ERROR

absPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
file_formatter = logging.Formatter('%(asctime)s\n%(filename)s:%(lineno)s - %(orignal_func)s()\n%(traceback)s')
stream_formatter = logging.Formatter('%(message)s')

today = datetime.datetime.now()
stf_date = today.strftime("%Y_%m_%d")

logFile_name = '{}.log'.format(stf_date)
folder_name = 'log'

if folder_name not in os.listdir(absPath):
    os.mkdir(os.path.join(absPath,folder_name))

folder_path = os.path.join(absPath, folder_name)
logFile = os.path.join(folder_path, logFile_name)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(logFile, 'a', 'utf-8')
file_handler.setLevel(level=file_level)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level=console_level)
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)
