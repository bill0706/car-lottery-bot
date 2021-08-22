from setting.function_wrapper import log_measure
from setting.log_handler import logger
from utility.fetch_handler import fetch_prize_details
from utility.rule_handler import calculate_position, bet_formula, round_setting


@log_measure
def start_bet(bet_details, driver):
    logger.info("開始下標")

    # Make Sure in default_frame
    driver.switch_to.default_content()

    remaining_score = driver.find_element_by_id("usableCreditSpan").text
    
    if bet_details.bet_value > int(remaining_score):
        raise SystemExit("錯誤! 餘額不足，無法下標")

    # Switch to iframe
    driver.switch_to.frame("mainIframe")

    inputs_block = driver.find_element_by_css_selector("div.game_item")
    ranking_elements = inputs_block.find_elements_by_tag_name("ul")

    # Switch lane to position index, write it
    lane = bet_details.bet_position - 1
    lanes = ranking_elements[lane].find_elements_by_tag_name('li')

    # switch to rank number position index
    rank_index = bet_details.bet_num - 1
    lane = lanes[rank_index].find_element_by_tag_name('input')

    # write bet value
    # Support string and int type
    lane.send_keys(bet_details.bet_value)

    # Find options element
    confirm_block = driver.find_element_by_css_selector('div.t_right')
    options = confirm_block.find_elements_by_css_selector('input')

    # Make Sure in default_frame
    driver.switch_to.default_content()
    # Scroll down to make sure click summit successfully
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Switch to iframe
    driver.switch_to.frame("mainIframe")

    # First summit
    for option in options:
        # change value to "提交" when aggreagate the code
        print(option.get_attribute('value'))
        if option.get_attribute('value') == "提交":
            option.click()
            break

    final_options_block = driver.find_element_by_css_selector("div.myLayerFooter")
    options = final_options_block.find_elements_by_css_selector('a')

    # Final summit
    # options[0] is cancel
    # popup prompt Need to show on the screen
    options[1].click()

    logger.info("下標成功!")


@log_measure
def start_processer(loop_queue, api_dic, bet_details, driver):
    
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
        if bet_details.start_bet_flag:
            start_bet(bet_details, driver)

        bet_details = round_setting(bet_details)    

        # wait for the next prize numbers
        queue_numbers = loop_queue.get()

