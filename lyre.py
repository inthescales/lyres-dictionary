import getopt
import sys

from enum import Enum
from textwrap import dedent

import src.generate as generate
import src.utils.logging as log
import src.utils.publish as publisher

class RunMode(Enum):
    """The execution mode to use. Determines output method and error behavior."""
    test = 0
    publish = 1

def test_with_count(count: int):
    """Generate entries for 'count' words and print them to the terminal."""
    print("")
    for i in range(0, count):
        print(generate.entry().text)
        print("")

# Help text to display when requested or when parameters are invalid
help_text: str = (
    dedent(f"""\
        usage: lyre [options]
          options:
            -t, --test           Print output to terminal
            -p, --publish        Publish output to web
            -c, --count     i    Generate "i" entries (test mode only)      default: 1
            -v, --verbose        Log verbose output
            -h, --help           Display this help text
          
          notes:
            - Defaults to test mode
            - Cannot use --test and --publish simultaneously
            - Log location: {log.log_dir}
    """))

def show_help(error: bool = False):
    """
    Print help text, then halt.
    :param error: bool, whether to exit with an error code
    """
    print(help_text)
    exit(0 if not error else 1)

# Read command line input
if __name__ == '__main__' and len(sys.argv) > 0:
    # Get args
    try:
        opts, params = getopt.getopt(sys.argv[1:], "tpc:vh", ["test", "publish", "count=", "verbose", "help"])
    except getopt.GetoptError:
        show_help(error=True)
        exit(1)
    
    all_flags = [opt[0] for opt in opts]

    # If help flag was set, print help text and exit
    if "-h" in all_flags or ["--help"] in all_flags:
        show_help(error=False)

    # Check for flag errors
    if ("-t" in all_flags or "--test" in all_flags) and ("-p" in all_flags or "--publish" in all_flags):
        show_help(error=True)

    # Default configuration values
    mode = RunMode.test
    count = 1
    verbose = False

    # Read arguments
    for opt, arg in opts:
        if opt in ["-t", "--test"]:
            mode = RunMode.test
        elif opt in ["-p", "--publish"]:
            mode = RunMode.publish
        elif opt in ["-c", "--count"]:
            count = int(arg)
        elif opt in ["-v", "--verbose"]:
            verbose = True

    # Configure logger
    if mode == RunMode.test:
        log.configure_for_test(verbose)
    elif mode == RunMode.publish:
        log.configure_for_publish()

    # Generate output
    if mode == RunMode.test:
        test_with_count(count)
    elif mode == RunMode.publish:
        publisher.publish(generate.entry)
