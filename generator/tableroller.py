"""
Class for generating traditional RPG table results
"""
import re
from . import roller

class TableRoller:
    """
    This class is designed to look up table results based off of random internal rolls.

    To come in the future:
      * Nested tables.
      * 2D tables
      * JSON tables
    """
    def __init__(self, roll, table=None, json_tables=None):
        if roll == 'd66':
            self.type = 'd66'
            self.num = 1
            self.die = 66
            assert self.num*self.die == len(table)
        elif re.match(r'^(\d+)d(\d+)', roll):
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

        if (table is not None and jsons_tables is not None):
            raise "cannot have both types of tables"

        if table is not None:
            self.tables = {}
            self.tables['main'] = {
                'results':table,
            }
        elif json_tables is not None:
            self.tables = json_tables

    def lookup(self, entry=None):
        """Do an internal roll and provide a table entry back"""
        if entry is None:
            if self.type == 'fitd':
                entry = roller.roll_fitd(self.num)
            elif self.type == 'd66':
                entry = roller.roll_d66()
                raise "D66 table lookup doesn't work yet"
            elif self.type == 'sum':
                entry = roller.roll_sum(self.num, self.die)
            else:
                raise "unable to identify roll type"

        return self.table[entry-1]
#
# test = TableRoller(roll="3D", table=["a", "b", "c", "d", "e", "f"])
# print(test.rollFitD())
