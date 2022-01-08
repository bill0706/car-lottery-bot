import logging
from setting.function_wrapper import log_measure
from setting.log_handler import logger


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

    if bet_details.check_approach_flag:
        logger.info("計算號碼: %s ， 車道: %s" %
                    (bet_details.bet_num, bet_details.bet_position))
    else:
        logger.info("下標號碼: %s ， 車道: %s" %
                    (bet_details.bet_num, bet_details.bet_position))

    return bet_details


def check_win(bet_details):
    logger.debug("[DEBUG] In check_win")

    for position in bet_details.last_bet_position:
        # index = position number -1
        if bet_details.last_bet_num == int(bet_details.prize_numbers[position - 1]):
            if bet_details.check_approach_flag:
                logger.info("進場條件符合! 號碼 %s ， 第 %s 車道 " %
                            (bet_details.last_bet_num, position))

            else:
                logger.info("恭喜中獎! 號碼 %s ， 第 %s 車道 " %
                            (bet_details.last_bet_num, position))

            # win
            bet_details.last_win_flag = True

            # number only have one position
            return bet_details

    # lose
    bet_details.last_win_flag = False

    if bet_details.check_approach_flag:
        logger.info("進場條件不符合!")
    else:
        logger.info("尚未中獎!")

    return bet_details


def check_bet_result(bet_details):

    logger.debug("[DEBUG] last_bet_num: %s" % bet_details.last_bet_num)

    # first run can't check
    if bet_details.last_bet_num is None:
        return bet_details

    check_win(bet_details)

    # Need to Judge the approach requirement
    if bet_details.check_approach_flag:
        if bet_details.last_win_flag:
            logger.info("成功進場!")
            bet_details.check_approach_flag = False
            bet_details.start_bet_flag = True

    # had approached
    else:

        # win
        if bet_details.last_win_flag:
            bet_details.level_index = 0

            logger.info("關卡調整為第 %s 關" % (bet_details.level_index + 1))

        # lose
        else:
            bet_details.level_index += 1

            # Reset level requirement satisfy
            if bet_details.level_index == len(bet_details.level_list):
                bet_details.level_index = 0
                bet_details.check_approach_flag = True
                bet_details.start_bet_flag = False
                logger.info("關卡結束，等待重新進場...")

            else:
                logger.info("關卡調整為第 %s 關" % (bet_details.level_index + 1))

    return bet_details


def bet_formula(bet_details):
    logger.debug("[DEBUG] In bet_formula")

    bet_details = check_bet_result(bet_details)

    if bet_details.start_bet_flag:

        # bet_details.level_list is string type
        bet_details.bet_value = bet_details.point * \
            int(bet_details.level_list[bet_details.level_index])

        logger.info("起始積分: %s ， 倍率: %s" % (bet_details.point, int(
            bet_details.level_list[bet_details.level_index])))
        logger.info("下標積分: %s" % bet_details.bet_value)

    return bet_details


def round_setting(bet_details):
    bet_details.last_bet_num = bet_details.bet_num
    bet_details.last_bet_position = bet_details.bet_position
    bet_details.bet_num = None
    bet_details.bet_position = None

    return bet_details
