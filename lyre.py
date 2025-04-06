import getopt
import random
import sys

import botbuddy

import src.generation.entry as entry
import src.evolutor.evolutor as evolutor

from src.evolutor.engine.config import Config
from src.tools.analysis import analyze
from src.utils.logging import Logger

def test_with_count(count):
    print("")
    for i in range(0, count):
        print(entry.generate_entry()["content"])
        print("")

def test_with_keys(keys):
    print("")
    print(entry.entry_for_keys(keys))
    print("")

def test_evolution(form, language):
    print("")
    print(form + "\n")

    if language == "old-english":
        config = Config(verbose=True, locked=False, overrides=[])
        print(evolutor.oe_form_to_ne_form(form, config))
    else:
        print("error: unrecognized language '" + language + "'")
    
    print("")

# Process command line input
if __name__ == '__main__' and len(sys.argv) > 0:
        # Error cases
    def error_mode_conflict():
        print("> Error: enter only one mode. Modes: test, publish, analyze")
        sys.exit(1)
    
    # Get args
    try:
        opts, params = getopt.getopt(sys.argv[1:], "tpac:k:e:", ["test", "publish", "analyze", "count=", "keys=", "evolve="])
    except getopt.GetoptError:
        print('lyre.py requires a mode parameter: -t/--test, -p/--publish, or -a/--analyze')
        sys.exit(2)

    mode = None
    count = None
    keys = None
    
    evolution_config = None

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
        elif opt in ["-e", "--evolution"]:
            evolution_config = { "form": arg, "language": "old-english" }
    
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

    # Output
    if mode == "publish":
        botbuddy.post(generate_entry)

    elif mode == "test":
        if keys != None:
            test_with_keys(keys)
        elif evolution_config != None:
            test_evolution(evolution_config["form"], evolution_config["language"])
        else:
            test_with_count(count)

    elif mode == "analyze":
        analyze(count)
