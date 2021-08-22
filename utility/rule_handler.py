from utility.function_wrapper import log_measure
from utility.log_handler import logger


@log_measure
def calculate_position(prize_numbers):

    # used in formula
    aggregation = 0
    count = 1
    bet_position = []

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
    
    return bet_num, bet_position