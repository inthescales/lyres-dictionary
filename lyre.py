import random
import getopt
import sys

from src.morphary import Morphary
from src.generator import generate_word
import src.validator as validator

def setup():
    global morphary
    
    morphary = Morphary(["data/morphs-latin.json"])

def needs_setup():
    return morphary == None

morphary = None
        
# Generating operations

def generate_entry():
    global morphary
    
    if needs_setup():
        setup()
    
    # Generate until we have a valid entry
    while True:
        word = generate_word(morphary)
        entry = word.entry()
        
        if validator.validate(entry):
            return entry

def entry_for_keys(keys):
    global morphary
    
    if needs_setup():
        setup()
        
    word = Word(morphary)
    word.set_keys(keys)
    
    return word.entry()

def test_with_count(count):
    
    print("")
    for i in range(0, count):
        print(generate_entry())
        print("")

def test_with_keys(keys):
    print("")
    print(entry_for_keys(keys))
    print("")

# Process command line input

if __name__ == '__main__' and len(sys.argv) > 0:
    
    mode = None
    count = None
    keys = None
    
    # Error cases
    def error_mode_conflict():
        print("> Error: cannot both publish and test at the same time")
        sys.exit(1)
    
    # Get args
    try:
        opts, params = getopt.getopt(sys.argv[1:], "tpc:k:", ["test", "publish", "count=", "keys="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    # Process args
    for opt, arg in opts:
        
        if opt in ["-t", "--test"]:
            if mode != None:
                error_mode_conflict()
            mode = "test"
        elif opt in ["-p", "--publish"]:
            if mode != None:
                error_mode_conflict()
            mode = "publish"
        elif opt in ["-c", "--count"]:
            count = int(arg)
        elif opt in ["-k", "--keys"]:
            keys = map(lambda key: key.strip(), arg.split(","))
    
    # Assign defaults
    
    if mode == None:
        print("> Defaulting to test mode")
        mode = "test"
        
    if keys == None and count == None:
        print("> Defaulting to count 1")
        count = 1
    
    if mode == "publish":
        print("-- publish --")
    elif mode == "test":
        if keys != None:
            test_with_keys(keys)
        else:
            test_with_count(count)
            
        print("")
