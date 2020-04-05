"""
Module for generating non-name aspects of an NPC.
"""
import random

GENDERS = ['female', 'non-binary', 'male']

def gender():
    """Generate a random gender"""
    return random.choices(GENDERS, weights=[1, .5, 1], k=1).pop()

def main():
    """Just test the functions"""
    print(gender())
if __name__ == "__main__":
    main()
