from setting.function_wrapper import log_measure
from setting.log_handler import logger
from utility.fetch_handler import fetch_prize_details
from utility.rule_handler import calculate_position, bet_formula, round_setting


@log_measure
def start_processer(loop_queue, api_dic, bet_details):
    
    # Used for first run
    queue_numbers = None

    # First run, and remaing seconds <= 30
    if api_dic is None:
        
        # wait for the next prize numbers
        queue_numbers = loop_queue.get()
    
    # First run, and remaing seconds > 30
    else:
        prize_numbers, prize_issue = fetch_prize_details(api_dic)
        
        logger.debug("[DEBUG] First run, prize numbers: %s" %prize_numbers)


    while queue_numbers or api_dic is not None:
       
        # Enter in loop_queue.get() expression 
        if queue_numbers is not None:
            prize_numbers, prize_issue = queue_numbers
            
            logger.debug("[DEBUG] Run in while, prize numbers: %s" %prize_numbers)
        
        # Close the first run and remaing seconds > 30 's door
        else:
            api_dic = None
        
        bet_details.prize_numbers = prize_numbers

        logger.info("第 %s 期 開獎號碼為 %s" %(prize_issue, prize_numbers))
            
        # Start the bet rule
        bet_details = bet_formula(bet_details)
        bet_details = calculate_position(bet_details)

        # Run bet

        bet_details = round_setting(bet_details)    

        # wait for the next prize numbers
        queue_numbers = loop_queue.get()
