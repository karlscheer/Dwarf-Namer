"""
Interface into rpg py gen. This is for generating RPG characters .

Currently supported traits:
  * Dwarf name
"""
import logging
import json
# argparse for making this tool usable
import argparse

# Core name-making functionality
import generator.namegen as namegen
import generator.genprofile as genprofile

def main():
    """ Handles random generation arguments. This is the primary interface.
    Currently just takes in the -n number of dwarves you want
    """
    # Create object
    parser = argparse.ArgumentParser()
    parser.add_argument("number", help="how many characters to generate", type=int)
    parser.add_argument("-v", "--verbose", help="print debug info", action='store_true')
    parser.add_argument("-c", "--clean", help="Print each name cleanly on its own line",
                        action='store_true')

    # Finish it!
    args = parser.parse_args()

    # Print management
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    with open('mountain_home_dwarf.json', 'r') as infile:
        profile_data = json.loads(infile.read())
        infile.close()
    dwarf_name_generator = namegen.NameAssembler(profile=genprofile.GenProfile(profile_data))

    with open('mh_dwarf_surname.json', 'r') as infile:
        surname = json.loads(infile.read())
        infile.close()
    dwarf_surname_name_generator = namegen.NameAssembler(profile=genprofile.GenProfile(surname))

    names = []
    for _ in range(0, args.number):
        name = dwarf_name_generator.generate_name() + " "
        name += dwarf_surname_name_generator.generate_name()
        names.append(name)

    if args.clean:
        for name in names:
            print(name)
    else:
        print(names)

main()
