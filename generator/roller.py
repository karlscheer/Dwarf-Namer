"""
Module for doing die rolls
"""
import random
from enum import Enum

FITD_FAILURE = range(1, 4)
FITD_PARTIAL = range(4, 6)
FITD_SUCCESS = [6]
FITD_CRITICAL = [7]

class RollResult(Enum):
    """
    For when results on a spectrum relating to categories, use these
    """
    CRITIAL_FAILURE = 0
    FAILURE = 1
    PARTIAL_SUCCESS = 2
    SUCCESS = 3
    CRITICAL_SUCCESSS = 4


def roll_sum(num, die):
    """Use the die and num properties in the table roller, generate a random result"""
    result = 0

    for _ in range(0, num):
        result += random.randint(1, die)
    return result

def roll_fitd(num):
    """
    Forged in the dark rolling: Roll xD6, keep the highest. Two sixes are are
    critical success.
    """
    result = 0
    rolled_die = 6
    print("Rolling ", num)
    for _ in range(0, num):
        die_res = random.randint(1, 6)
        if (die_res == rolled_die) and (result == rolled_die):
            result = FITD_CRITICAL[0]
        else:
            result = max(result, die_res)
    print(result)

    if result in FITD_FAILURE:
        return RollResult.FAILURE
    if result in FITD_PARTIAL:
        return RollResult.PARTIAL_SUCCESS
    if result in FITD_SUCCESS:
        return RollResult.SUCCESS
    if result in FITD_CRITICAL:
        return RollResult.CRITICAL_SUCCESSS

    return result

def roll_d66(num):
    """
    D66 roller, which is a 36-result table where one D6 is the 1s digit and
    the other is the 10s
    """
    result = 0
    rolled_die = 6

    for _ in range(0, num):
        result += random.randint(1, rolled_die)*10
        result += random.randint(1, rolled_die)
    return result
#
# test = TableRoller(roll="3D", table=["a", "b", "c", "d", "e", "f"])
# print(test.rollFitD())
