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
    def __init__(self, seed=None, profile_json=None):

        if profile_json is None:
            raise "Needs JSON profiles to work"

        self.profiles = {}
        for section in profile_json['sections']:
            self.profiles[section['section_name']] = genprofile.GenProfile(section)

        # self.syllables = 0
        self.name = profile_json['profile_name']
        self.seed = seed

        # Keep the seed if you want to remember the dwarf you made and re-gen later
        random.seed(a=seed)

    def generate_all(self):
        total = []
        for profile in self.profiles.keys():
            total.append(self.generate_name(profile))
        return " ".join(total)

    def generate_name(self, section):
        """Using the profile provided, generate a fancy given name"""
        profile = self.profiles[section]

        new_name = profile.select_prefix("")
        suffix = profile.select_suffix(new_name)
        logging.info("initial %s suffix %s", new_name, suffix)

        # A certain number of names just get lenthened. Two letter names are not
        # accepted. Some number of <4 letter names are just cut out as well.
        while profile.determine_reroll(len(new_name)+len(suffix)):
            if new_name[-1] in profile.vowels_list():
                new_name += profile.select_joiner(new_name+suffix)
            else:
                new_name += profile.select_vowel(new_name+suffix)
                new_name += profile.select_joiner(new_name+suffix)

        if ((new_name[-1] not in profile.vowels_list()) and
                (suffix[0] not in profile.vowels_list())):
            new_name += profile.select_vowel(new_name+suffix)
            logging.info("%s suffix glue", new_name)
        new_name += suffix
        logging.info("pre-cleanup %s", new_name)

        # Put diacritics on the second of two vowels if there are two vowels in a row
        for i, char in enumerate(new_name):
            if ((char in profile.vowels_list()) and
                    (i + 1 < len(new_name)) and
                    (new_name[i + 1] in profile.vowels_list())):
                split = list(new_name)
                split[i + 1] = profile.alt_vowels[split[i + 1]]
                new_name = ''.join(split)

        # TODO Walk through and remove dupes
        # TODO Walk through and remove awkward letter combos

        new_name = new_name.lower().title()
        return new_name

def main():
    """Diagnostic runner thing"""
    name = NameAssembler()
    test = [name.generate_name() for _ in range(1, 25)]
    print(test)

if __name__ == "__main__":
    main()
