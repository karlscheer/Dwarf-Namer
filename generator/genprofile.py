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
        # total = self.__gen_build_options_weight(options)
        self.gen_reduce_odds_from_string(options, current)
        weights = [item['weight'] for item in options]
        selection = random.choices(options, weights=weights, k=1).pop()
        return selection['content']

    def select_joiner(self, current):
        """
        This takes in the current string to allow for future weighting based
        off of existing use
        """
        if self.joiners is None:
            return ""
        options = self.__build_gen_choices(self.joiners)
        if len(options) == 0:
            return ""

        self.gen_reduce_odds_from_string(options, current)
        weights = [item['weight'] for item in options]
        selection = random.choices(options, weights=weights, k=1).pop()
        return selection['content']

    def select_suffix(self, current):
        """
        This takes in the current string to allow for future weighting based
        off of existing use
        """
        if self.suffixes is None:
            return ""
        options = self.__build_gen_choices(self.suffixes)
        if len(options) == 0:
            return ""

        self.gen_reduce_odds_from_string(options, current)
        weights = [item['weight'] for item in options]
        selection = random.choices(options, weights=weights, k=1).pop()
        return selection['content']

    def select_vowel(self, current):
        """
        This takes in the current string to allow for future weighting based
        off of existing use
        """
        if self.vowels is None:
            return ""
        options = self.__build_gen_choices(self.vowels)
        if len(options) == 0:
            return ""

        self.gen_reduce_odds_from_string(options, current)
        weights = [item['weight'] for item in options]
        selection = random.choices(options, weights=weights, k=1).pop()
        return selection['content']

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
