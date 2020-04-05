"""
Class for generating traditional RPG table results
"""
import re
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

class TableRoller:
    """
    This class is designed to look up table results based off of random internal rolls.

    To come in the future:
      * Nested tables.
      * 2D tables
      * JSON tables
    """
    def __init__(self, roll, table):
        if roll == 'd66':
            self.type = 'd66'
            self.num = 1
            self.die = 66
            assert self.num*self.die == len(table)
        elif re.match(r'(\d+)d(\d+)', roll):
            self.type = 'sum'
            assert re.search(r'^\d+d\d+$', roll)
            all_dice = re.search(r'(\d?)d(\d+)', roll)
            self.num = int(all_dice.group(1))
            self.die = int(all_dice.group(2))
        elif re.match(r'^(\d+)D$', roll):
            self.type = 'fitd'
            all_dice = re.search(r'^(\d+)D$', roll)
            self.num = int(all_dice.group(1))
            assert len(table) == 4
            self.die = 6
        else:
            raise "Couldn't match the die type"
        self.table = table

    def roll_sum(self):
        """Use the die and num properties in the table roller, generate a random result"""
        result = 0
        rolled_die = self.die

        if self.die == 66:
            rolled_die = 6

        for _ in range(0, self.num):
            if self.die == 66:
                result += random.randint(1, rolled_die)*10
                result += random.randint(1, rolled_die)
            else:
                result += random.randint(1, rolled_die)
        return result

    def roll_fitd(self):
        """
        Forged in the dark rolling: Roll xD6, keep the highest. Two sixes are are
        critical success.
        """
        result = 0
        print("Rolling ", self.num)
        for _ in range(0, self.num):
            die_res = random.randint(1, 6)
            print(die_res)
            if die_res == 6 and result == 6:
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

    def roll_d66(self):
        """
        D66 roller, which is a 36-result table where one D6 is the 1s digit and
        the other is the 10s
        """
        result = 0
        rolled_die = self.die

        if self.die == 66:
            rolled_die = 6

        for _ in range(0, self.num):
            if self.die == 66:
                result += random.randint(1, rolled_die)*10
                result += random.randint(1, rolled_die)
            else:
                result += random.randint(1, rolled_die)
        return result

    def lookup(self, entry=None):
        """Do an internal roll and provide a table entry back"""
        if entry is None:
            if self.type == 'fitd':
                entry = self.roll_fitd()
            elif self.type == 'd66':
                entry = self.roll_d66()
                raise "D66 table lookup doesn't work yet"
            elif self.type == 'sum':
                entry = self.roll_sum()
            else:
                raise "unable to identify roll type"

        return self.table[entry-1]
#
# test = TableRoller(roll="3D", table=["a", "b", "c", "d", "e", "f"])
# print(test.rollFitD())
