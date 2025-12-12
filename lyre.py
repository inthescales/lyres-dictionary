import getopt
import random
import sys

import src.generate as generate
import src.utils.publish as publisher

from src.utils.logging import Logger

def test_with_count(count):
    print("")
    for i in range(0, count):
        print(generate.entry().text())
        print("")

# Process command line input
if __name__ == '__main__' and len(sys.argv) > 0:
    # Error cases
    def error_mode_conflict():
        print("> Error: enter only one mode. Modes: test, publish, analyze")
        sys.exit(1)
    
    # Get args
    try:
        opts, params = getopt.getopt(sys.argv[1:], "tpc:", ["test", "publish", "count="])
    except getopt.GetoptError:
        print('lyre.py requires a mode parameter: -t/--test or -p/--publish')
        sys.exit(2)

    mode = None
    count = None

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
    
    # Assign default values
    if mode == None:
        Logger.trace("defaulting to test mode")
        mode = "test"
    if mode == "test" and count == None:
        Logger.trace("defaulting to count 1")
        count = 1

    # Configure logger
    if mode == "test":
        Logger.configure("terminal", "error", 1)
    elif mode == "publish":
        Logger.configure("file", None, 2)

    # Generate output
    if mode == "publish":
        publisher.publish(generate.entry)
    elif mode == "test":
        test_with_count(count)
