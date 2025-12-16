import getopt
import sys

from enum import Enum

import src.generate as generate
import src.utils.logging as log
import src.utils.publish as publisher

class RunMode(Enum):
    test = 0
    publish = 1

def test_with_count(count: int):
    print("")
    for i in range(0, count):
        print(generate.entry().text)
        print("")

# Read command line input
if __name__ == '__main__' and len(sys.argv) > 0:
    # Get args
    try:
        opts, params = getopt.getopt(sys.argv[1:], "tpc:", ["test", "publish", "count="])
    except getopt.GetoptError:
        print("ERROR: lyre.py requires a mode parameter: -t/--test or -p/--publish\n")
        sys.exit(2)

    # Check errors
    all_opts = [o[0] for o in opts]
    if ("-t" in all_opts or "--test" in all_opts) and ("-p" in all_opts or "--publish" in all_opts):
        print("Error: enter only one mode. Modes: test, publish\n")
        sys.exit(1)

    # Default arguments
    mode = RunMode.test
    count = 1

    # Read arguments
    for opt, arg in opts:
        if opt in ["-t", "--test"]:
            mode = RunMode.test
        elif opt in ["-p", "--publish"]:
            mode = RunMode.publish
        elif opt in ["-c", "--count"]:
            count = int(arg)

    # Configure logger
    if mode == RunMode.test:
        log.configure_for_test()
    elif mode == RunMode.publish:
        log.configure_for_publish()

    # Generate output
    if mode == RunMode.test:
        test_with_count(count)
    elif mode == RunMode.publish:
        publisher.publish(generate.entry)
