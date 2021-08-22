from setting.function_wrapper import log_measure
from setting.log_handler import logger


@log_measure
def calculate_position(bet_details):

    # used in formula
    aggregation = 0
    count = 1
    bet_position = []

    prize_numbers = bet_details.prize_numbers

    champion = prize_numbers[0]
    
    if int(champion) % 2 == 1: 
        champion_state = 'singular'
    else:
        champion_state = 'plural'

    for number in prize_numbers:

        # singular
        if champion_state == 'singular':
            if count % 2 == 1:
                aggregation += int(number)
                bet_position.append(int(number))
    
        # double
        else:
            if count % 2 == 0:
                aggregation += int(number)
                bet_position.append(int(number))
        
        count += 1

    # int has no len() attribute
    while len(str(aggregation)) == 2:
        calculate = str(aggregation)
        aggregation = int(calculate[0]) + int(calculate[1])
    
    bet_num = aggregation
    
    bet_details.bet_num = bet_num
    bet_details.bet_position = bet_position

    return bet_details


@log_measure
def bet_formula(bet_details):
    pass


@log_measure
def check_win(bet_details):
    pass


