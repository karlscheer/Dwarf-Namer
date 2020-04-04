"""
Generator profile. This is used for providing lists of GenItem tuples in various
configurations for the purpose of generating words.
"""
import collections
import random
import logging

DEFAULT_WEIGHT = 1
MIN_WEIGHT = 0
MAX_WEIGHT = 5

GenItem = collections.namedtuple('GenItem', 'contents weight')

class GenProfile:
    """
    Gen profile used to provide information on how to generate name
    """
    def __init__(self, generator_json):
        self.title = generator_json['section_name']
        self.remove_dupe_letters = generator_json['remove_dup_letters']
        self.weight_letters = generator_json['weight_letters']
        self.prefixes = generator_json['prefixes']
        self.suffixes = generator_json['suffixes']

        self.vowels = {}
        if 'vowels' in generator_json:
            self.vowels = generator_json['vowels']

        self.alt_vowels = {}
        if 'alt_vowels' in generator_json:
            self.alt_vowels = generator_json['alt_vowels']

        self.joiners = {}
        if 'joiners' in generator_json:
            self.joiners = generator_json['joiners']

        self.reroll_chance = {}
        if 'reroll_by_lenth' in generator_json:
            self.reroll_chance = generator_json['reroll_by_lenth']

    def determine_reroll(self, length):
        """
        Based off of length of the current name, determine if it needs to be
        continued
        """
        if len(self.reroll_chance) == 0:
            return False

        chance = self.reroll_chance['other']
        key = str(length)
        if key in self.reroll_chance:
            chance = self.reroll_chance[key]

        # Res is from 0.0 to 1.0
        res = random.random()

        logging.info("checking chance odds %s got %s", chance, res)

        if  res <= chance:
            logging.info("Length %s odds %s and True", length, chance, )
            return True
        logging.info("Length %s odds %s and False", length, chance, )
        return False

    def select_prefix(self, current):
        """
        This takes in the current string to allow for future weighting based
        off of existing use
        """

        options = self.__build_gen_choices(self.prefixes, self.joiners)
        total = self.__gen_build_options_weight(options)

        selection = random.uniform(0, total)
        logging.info("Total possible %s selected %s", total, selection)
        logging.info("Options %s", options)

        for item in options:
            selection -= item['weight']
            logging.info("At %s Total possible %s selected %s", item['content'], total, selection)
            if selection <= 0:
                return item['content']

        raise "I must have selected something"

    def select_joiner(self, current):
        """
        This takes in the current string to allow for future weighting based
        off of existing use
        """
        if self.joiners is None:
            return ""

        total = 0
        options = self.__build_gen_choices(self.joiners)
        self.gen_reduce_odds_from_string(options, current)

        for item in options:
            found = current.count(item['content'])
            if found:
                logging.info("In name %s found %s", current, item['content'])
                item = {'content':item['content'], 'weight':min(0, (item['weight']/found))}
            total += item['weight']

        selection = random.uniform(0, total)

        for item in self.joiners:
            selection -= item['weight']
            if selection <= 0:
                return item['content']
        raise "All generators should return something"

    def select_suffix(self, current):
        """
        This takes in the current string to allow for future weighting based
        off of existing use
        """
        total = 0
        options = self.__build_gen_choices(self.suffixes)

        if len(options) == 0:
            return ""

        self.gen_reduce_odds_from_string(options, current)
        total = self.__gen_build_options_weight(options)

        selection = random.uniform(0, total)

        for item in options:
            selection -= item['weight']
            if selection <= 0:
                return item['content']
        raise "I must have selected something"

    def select_vowel(self, current):
        """
        This takes in the current string to allow for future weighting based
        off of existing use
        """
        if self.vowels is None:
            return ""

        total = 0
        options = self.__build_gen_choices(self.vowels)
        if len(options) == 0:
            return ""

        for item in options:
            found = current.count(item['content'])
            if found:
                logging.info("In name %s found %s", current, item['content'])
                item = {'content':item['content'], 'weight':min(0, (item['weight']/found))}
            total += item['weight']

        selection = random.uniform(0, total)

        for item in options:
            selection -= item['weight']
            if selection <= 0:
                return item['content']
        raise "I must have selected something"

    def vowels_list(self):
        """ Create a list of vowels for comparison reasons """
        vowels = []
        for item in self.vowels:
            vowels.append(item['content'])
        return vowels

    def gen_reduce_odds_from_string(self, options, string):
        """
        If the generator wants to make repeat letters less likely, reduce
        the weight based off of frequency
        """
        if self.weight_letters:
            for entry in options:
                count = string.count(entry['content'])
                if count:
                    logging.info("In name %s found %s", string, entry['content'])
                    entry = GenItem(entry['content'], min(0, (entry['weight']/count)))

    @staticmethod
    def __build_gen_choices(*all_lists):
        options = []
        for gen_list in all_lists:
            for entry in gen_list:
                options.append(entry)
        return options

    @staticmethod
    def __gen_build_options_weight(options):
        total = 0
        for entry in options:
            total += entry['weight']
        return total

#Here's a scrap about profile writing
    # prefixes = [{'content':'ur', 'weight':.5}, {'content':'er', 'weight':.5},
    #             {'content':'do', 'weight':1}, {'content':'ba', 'weight':1},
    #             {'content':'ka', 'weight':1}]
    # vowels = [{'content':'a', 'weight':.5}, {'content':'e', 'weight':.25},
    #           {'content':'i', 'weight':.5}, {'content':'o', 'weight':1.5},
    #           {'content':'u', 'weight':1.5}]
    # alt_vowels = {'a': "á", "e": "é", "i": "í", "o": "ó", "u": "ú"}
    # joiners = [{'content':'k', 'weight':1}, {'content':'d', 'weight':1},
    #            {'content':'b', 'weight':1}, {'content':'r', 'weight':1},
    #            {'content':'th', 'weight':1.25}, {'content':'g', 'weight':1},
    #            {'content':'r', 'weight':1}, {'content':'m', 'weight':1},
    #            {'content':'t', 'weight':1}, {'content':'z', 'weight':.25},
    #            {'content':'l', 'weight':1}, {'content':'sh', 'weight':.8}]
    # suffixes = [{'content':'li', 'weight':1.25}, {'content':'z', 'weight':.2},
    #             {'content':'ro', 'weight':.5}, {'content':'in', 'weight':1.25},
    #             {'content':'da', 'weight':1}, {'content':'st', 'weight':1},
    #             {'content':'sh', 'weight':.8}, {'content':'ng', 'weight':.5},
    #             {'content':'ch', 'weight':.5}]
    # reroll_by_lenth = {'other':.05, 0:1, 1:1, 2:1, 3:.75, 4:.60, 5:.1, 6:.075 }
    # dwarf_profile = {
    #     'profile_name':"Mountain Home Dwarf",
    #     'remove_dup_letters':True,
    #     'prefixes':prefixes,
    #     'vowels':vowels,
    #     'joiners':joiners,
    #     'alt_vowels':alt_vowels,
    #     'suffixes':suffixes,
    #     'reroll_by_lenth':reroll_by_lenth,
    # }
    #
    # with open('mountain_home_dwarf.json', 'w') as outfile:
    #     json.dump(dwarf_profile, indent=4, fp=outfile)
    # return
