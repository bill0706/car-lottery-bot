from setting.bet import BetDetails
from setting.function_wrapper import log_measure
from setting.log_handler import logger
from utility.fetch_handler import fetch_prize_details
from utility.rule_handler import calculate_position


@log_measure
def start_processer(loop_queue, api_dic):
    # Used for first run
    queue_numbers = None
    bet_details = BetDetails()

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

        bet_details = calculate_position(bet_details, prize_numbers)
        logger.debug('[DEBUG] bet_num: %s, bet_position: %s ' %(bet_details.bet_num, bet_details.bet_position))

        # wait for the next prize numbers
        queue_numbers = loop_queue.get()
