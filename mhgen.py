"""
Interface into rpg py gen. This is for generating RPG characters .

Currently supported traits:
  * Dwarf name
"""
import logging
import json
from pathlib import Path
# argparse for making this tool usable
import argparse

# Core name-making functionality
import generator.namegen as namegen

def main():
    """ Handles random generation arguments. This is the primary interface.
    Currently just takes in the -n number of dwarves you want
    """
    # Create object
    description = "MH Gen is my tool for generating dwarf names. It is steadily and "
    description += "regularly expanding to encompass more and more GM tools. Eventually, "
    description += "this will include the necessary tools for playing Mountain Home entirely."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "number", help="how many characters to generate", type=int)
    parser.add_argument("-v", "--verbose",
                        help="print debug info", action='store_true')
    parser.add_argument("-c", "--clean", help="Print each name cleanly on its own line",
                        action='store_true')
    parser.add_argument("-o", "--only", metavar="SEGMENT",
                        help="Only generate one name type", default=None)
    parser.add_argument("-j", "--json", help="For providing an overriding json file")
    parser.add_argument("-p", "--personal_aspects", help="""Also generate personal aspects about
                                                            the name such as gender identity""")

    # Finish it!
    args = parser.parse_args()

    # Print management
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    # Profile management
    generate = 'ALL'
    if args.only is not None:
        generate = args.only

    # Path/file handling
    path = "./generator/profiles/"
    file = "mh_dwarf.json"
    if args.json:
        file = args.json

    found = ""
    for test_file in (file, path+file):
        test = Path(test_file)
        if test.is_file():
            found = test_file
    with open(found, 'r') as infile:
        profile_data = json.loads(infile.read())
        infile.close()

    # Generate the names
    generator = namegen.NameAssembler(profile_json=profile_data)
    names = []
    for _ in range(0, args.number):
        if generate == 'ALL':
            name = generator.generate_all()
        else:
            name = generator.generate_name(generate)
        names.append(name)

    if args.clean:
        for name in names:
            print(name)
    else:
        print(names)


main()
