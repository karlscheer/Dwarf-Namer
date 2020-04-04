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
    description = "MH Gen is my tool for generating dwarf names. It is steadily and "
    description += "regularly expanding to encompass more and more GM tools. Eventually, "
    description += "this will include the necessary tools for playing Mountain Home entirely."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("number", help="how many characters to generate", type=int)
    parser.add_argument("-v", "--verbose", help="print debug info", action='store_true')
    parser.add_argument("-c", "--clean", help="Print each name cleanly on its own line",
                        action='store_true')
    parser.add_argument("-o", "--only", metavar="SEGMENT",
                        help="Only generate one name type", default=None)
    parser.add_argument("-j", "--json", help="Overriding json file")

    # Finish it!
    args = parser.parse_args()

    # Print management
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    generate = 'ALL'
    if args.only is not None:
        generate = args.only


    file = 'mh_dwarf.json'
    if args.json:
        file = args.json
    #     with
    # else:

    with open(file, 'r') as infile:
        profile_data = json.loads(infile.read())
        infile.close()

    dwarf_name_generator = namegen.NameAssembler(profile_json=profile_data)

    names = []
    for _ in range(0, args.number):
        if generate == 'ALL':
            name = dwarf_name_generator.generate_all()
        else:
            name = dwarf_name_generator.generate_name(generate)
        names.append(name)

    if args.clean:
        for name in names:
            print(name)
    else:
        print(names)

main()
