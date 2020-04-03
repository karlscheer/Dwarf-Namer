"""
My custom name generator tool. It's fuzzy. There's no official algorithm
"""
import random
import logging
from . import genprofile
from . import tableroller

class NameAssembler:
    """ This uses a "gen profile" object to create names based off of the rules
    provided in the profile itself """
    def __init__(self, seed=None, profile=None):

        if profile is None:
            profile = genprofile.GenProfile()

        # self.syllables = 0
        self.name = ""
        self.seed = seed
        self.profile = profile

        # Keep the seed if you want to remember the dwarf you made and re-gen later
        random.seed(a=seed)

    def generate_name(self):
        """Using the profile provided, generate a fancy given name"""
        self.name = self.profile.select_prefix(self.name)
        suffix = self.profile.select_suffix(self.name)
        logging.info("initial %s suffix %s", self.name, suffix)

        # A certain number of names just get lenthened. Two letter names are not
        # accepted. Some number of <4 letter names are just cut out as well.
        while self.profile.determine_reroll(len(self.name)+len(suffix)):
            if self.name[-1] in self.profile.vowels_list():
                self.name += self.profile.select_joiner(self.name+suffix)
            else:
                self.name += self.profile.select_vowel(self.name+suffix)
                self.name += self.profile.select_joiner(self.name+suffix)

        if ((self.name[-1] not in self.profile.vowels_list()) and
                (suffix[0] not in self.profile.vowels_list())):
            self.name += self.profile.select_vowel(self.name+suffix)
            logging.info("%s suffix glue", self.name)
        self.name += suffix
        logging.info("pre-cleanup %s", self.name)

        # Put diacritics on the second of two vowels if there are two vowels in a row
        for i, char in enumerate(self.name):
            if ((char in self.profile.vowels_list()) and
                    (i + 1 < len(self.name)) and
                    (self.name[i + 1] in self.profile.vowels_list())):
                split = list(self.name)
                split[i + 1] = self.profile.alt_vowels[split[i + 1]]
                self.name = ''.join(split)

        # TODO Walk through and remove dupes
        # TODO Walk through and remove awkward letter combos

        self.name = self.name.lower().title()
        return self.name

def main():
    """Diagnostic runner thing"""
    name = NameAssembler()
    test = [name.generate_name() for _ in range(1, 25)]
    print(test)

if __name__ == "__main__":
    main()
