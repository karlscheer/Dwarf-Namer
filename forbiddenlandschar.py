"""
Just a simple dice-roller test
"""
import generator.tableroller as tableroller

def main():
    """ Test function runner for laziness """
    print("Forbidden Lands Random Character Starter:")

    kin = tableroller.TableRoller("1d6", ["Human", "Elf", "Half-elf", "Dwarf",
                                          "Halfling", "Wolfkin"])
    print("Kin:", kin.lookup('main'))

    profession = tableroller.TableRoller("1d8", ["Druid", "Fighter", "Hunter", "Minstrel",
                                                 "Peddler", "Rider", "Rogue", "Sorcerer"])
    print("Profession:", profession.lookup('main'))

    age = tableroller.TableRoller("1d3",
                                  ["Young (Attributes 15, Skills 8, General Talents 1, Rep 0)",
                                   "Adult (Attributes 14, Skills 10, Talents 2, Rep 1)",
                                   "Old (Attributes 13, Skills 12, Talents 3, Rep 2)"])
    print("Age:", age.lookup('main'))

if __name__ == "__main__":
    main()
