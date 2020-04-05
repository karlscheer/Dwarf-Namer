"""
Module for generating non-name aspects of an NPC.
"""
import random
import json

GENDERS = ['female', 'non-binary', 'male']
AGES = ['young adult', 'adult', 'middle-aged', 'older', 'elderly']
ABILITY = ['fully able', 'leg injury', 'face injury', 'arm injury', 'head injury']

class AspectProfile:
    """
    For creating minor aspects of NPCs
    """
    def __init__(self, aspect_json):
        self.aspects = aspect_json

    def generate_all(self):
        """Generate all aspects as a dictionary"""
        aspects = {}
        for aspect in self.aspects:
            aspects[aspect] = self.generate(aspect)
        return aspects

    def generate(self, aspect):
        """Generate a random aspect"""
        profile = self.aspects[aspect]
        values = [item['content'] for item in profile['results']]
        weights = [item['weight'] for item in profile['results']]
        return random.choices(values, weights=weights, k=1).pop()

def main():
    """Just test the functions"""
    # path = "profiles/"
    file = "./profiles/aspects.json"
    print(file)
    with open(file, 'r') as infile:
        aspect_json = json.loads(infile.read())
        infile.close()
    new = AspectProfile(aspect_json)
    print(" ".join(new.generate_all()))

if __name__ == "__main__":
    main()
