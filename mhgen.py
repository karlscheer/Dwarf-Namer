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
import generator.aspects as aspects

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
    parser.add_argument("-p", "--personal_aspects", action='store_true',
                        help="""Also generate personal aspects about
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

    if args.personal_aspects:
        file = "./generator/profiles/aspects.json"
        print(file)
        with open(file, 'r') as infile:
            aspect_json = json.loads(infile.read())
            infile.close()
        aspect_gen = aspects.AspectProfile(aspect_json)

    # Generate the names
    generator = namegen.NameAssembler(profile_json=profile_data)
    results = []
    for _ in range(0, args.number):
        char_aspects = {}
        if args.personal_aspects:
            char_aspects = aspect_gen.generate_all()

        if generate == 'ALL':
            char_aspects['name'] = generator.generate_all()
        else:
            char_aspects['name'] = generator.generate_name(generate)
        results.append(char_aspects)

    if args.clean:
        for result in results:
            print("{}".format(result['name']))
            _ = [print("\t{}: {}".format(key.title(), result[key])) for key in result if key != 'name']
    else:
        print(results)

if __name__ == "__main__":
    main()
