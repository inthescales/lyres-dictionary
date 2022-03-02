import random
import getopt
import sys

import botbuddy

from src.morphothec import Morphothec
from src.generator import generate_word, word_for_keys
from src.logging import Logger
from src.analysis import Analyst

import src.composer as composer
import src.validator as validator

morphothec = None

def setup():
    global morphothec
    
    morphothec = Morphothec("data/")

def needs_setup():
    return morphothec == None
        
# Generating operations

def generate_entry():
    global morphothec
    
    if needs_setup():
        setup()
    
    # Generate until we have a valid entry
    while True:
        word = generate_word(morphothec)
        entry = composer.entry(word)
        
        if validator.validate(entry):
            return entry

def entry_for_keys(keys):
    global morphothec, composer
    
    if needs_setup():
        setup()
        
    word = word_for_keys(keys, morphothec)
    
    return composer.entry(word)

def test_with_count(count):
    
    print("")
    for i in range(0, count):
        print(generate_entry())
        print("")

def test_with_keys(keys):
    print("")
    print(entry_for_keys(keys))
    print("")

def analyze():

    if needs_setup():
        setup()

    print("Analyzing...")

    analyst = Analyst()
    for i in range(0, count):
        word = generate_word(morphothec)
        analyst.register(word)
        print(f"Analyzed: {i}/{count}", end="\r")

    print("Analysis complete")
    analyst.print_results(log=True)

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
        opts, params = getopt.getopt(sys.argv[1:], "tpac:k:", ["test", "publish", "analyze", "count=", "keys="])
    except getopt.GetoptError:
        print('lyre.py requires a mode parameter: -t/--test, -p/--publish, or -a/--analyze')
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
        elif opt in ["-a", "--analyze"]:
            if mode != None:
                error_mode_conflict()
            mode = "analyze"
        elif opt in ["-c", "--count"]:
            count = int(arg)
        elif opt in ["-k", "--keys"]:
            keys = map(lambda key: key.strip(), arg.split(","))
    
    # Assign defaults
    if mode == None:
        Logger.trace("defaulting to test mode")
        mode = "test"
        
    if mode == "test" and keys == None and count == None:
        Logger.trace("defaulting to count 1")
        count = 1

    if mode == "analyze":
        count = 1000000
    
    # Configure logger
    if mode == "test" or mode == "analyze":
        Logger.configure("terminal", "error", 1)
    elif mode == "publish":
        Logger.configure("file", None, 2)

    # Print output
    if mode == "publish":
        botbuddy.post(generate_entry)
    elif mode == "test":
        if keys != None:
            test_with_keys(keys)
        else:
            test_with_count(count)
            
        print("")
    elif mode == "analyze":
        analyze()
