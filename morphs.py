import getopt
import os
import sys

from src.tools.morphs.morphs_format import format_morphs
from src.tools.morphs.morphs_validate import validate_morphs
from src.tools.morphs.morphs_modify import modify_morphs
from src.tools.morphs.morphs_merge import merge_morphs
from src.tools.morphs.morphs_search import search_morphs
from src.tools.morphs.morphs_split import split_morphs

import src.tools.morphs.morphs_files as file_tool

data_dir = "./data"
meta_dir = "./data/meta"

def command_format(args):
    try:
        opts, params = getopt.getopt(args, "t", ["test"])
    except getopt.GetoptError:
        print('getopt error')
        sys.exit(2)

    files = []
    test_mode = False

    # Process args
    for opt, arg in opts:
        if opt in ["-t", "--test"]:
            test_mode = True

    if len(params) > 1 and test_mode:
        print("ERROR: morph format can only take one file argument for test mode")
        sys.exit(0)

    if len(params) == 0:
        morphs_files = file_tool.all_morph_files(data_dir)
        print("Formatting " + str(len(morphs_files)) + " files")
    else:
        print("Formatting " + str(len(params)) + " files")
        files = params

    format_morphs(files, meta_dir, test_mode)

def command_validate(args):
    if len(args) == 0:
        morphs_files = file_tool.all_morph_files(data_dir)
        print("Validating " + str(len(morphs_files)) + " files")
    else:
        print("Validating " + str(len(args)) + " files")
        morphs_files = args

    validate_morphs(morphs_files, meta_dir)

def command_modify(args):
    if len(args) == 0:
        morphs_files = file_tool.all_morph_files(data_dir)
        print("Modifying " + str(len(morphs_files)) + " files")
    else:
        print("Modifying " + str(len(args)) + " files")
        morphs_files = args

    modify_morphs(morphs_files)

def command_merge(args):
    if len(args) < 2:
        print("ERROR: must merge at least 2 morph files")
    else:
        morphs_files = args

    merge_morphs(morphs_files)

def command_search(args):
    try:
        opts, params = getopt.getopt(args, "cl", ["count", "list"])
    except getopt.GetoptError:
        print('ERROR: getopt error')
        sys.exit(2)

    task = None
    files = []

    # Process args
    for opt, arg in opts:
        if opt in ["-c", "--count"]:
            task = "count"
        elif opt in ["-l", "--list"]:
            task = "list"

    if task == None:
        print("ERROR: must specify task. Available tasks: count, list")
        sys.exit(0)

    if len(params) == 0:
        files = file_tool.all_morph_files(data_dir)
        print("Searching " + str(len(files)) + " files")
    else:
        print("Searching " + str(len(params)) + " files")
        files = params

    search_morphs(files, task)

def command_split(args):
    if len(args) != 1:
        # TODO: Consider making it possible to split and re-group multiple files
        print("ERROR: must split exactly 1 file")
        sys.exit(0)
    else:
        file = args[0]

    split_morphs(file)

def command_help(args):
    if len(args) == 0:
        print()
        print("This program contains various tools for operating on the corpus of morphs.")
        print("To use it, include a command name and any necessary arguments.")
        print()
        print("Available commands:")
        command_list()
        print()
        print("For usage information, enter 'morphs help [command]'")
        print()
    else:
        input_command = args[0]

        print()
        if input_command in commands:
            print(commands[input_command][2])
        print()

commands = {
    "format": [
        command_format,
        "Format and sort morphs",
        "Usage: morphs format [-t/--test] [files]\n\nFormats the listed morph files in place, or all if none are given.\nIn [t]est mode, formatted data will be printed to stdout instead of modifying files."
    ],
    "validate": [
        command_validate,
        "Validate that morphs are properly formed",
        "Usage: morphs validate [files]\n\nValidates the given morph files, or all if none are given, printing any errors found."
    ],
    "modify": [
        command_modify,
        "Apply a change to all morphs",
        "Usage: morphs modify [files]\n\nModifies the given morph files, or all if none are given. Changes must be hard-coded."
    ],
    "search": [
        command_search,
        "Find all morphs satisfying certain conditions",
        "Usage: morphs search [-c/--count] [-l/--list] [files]\n\nSearches the given morph files, or all if none are given, for morphs matching hard-coded criteria.\nIn [c]ount mode, the number of matches only is printed.\nIn [l]ist mode, the full list of morphs is printed."
    ],
    "merge": [
        command_merge,
        "Merge two or more morph files into one",
        "Usage: morphs merge [files]\n\nMerges all morphs from the listed files into a single file, and prints it to stdout."
    ],
    "split": [
        command_split,
        "Split one morphs file into two or more",
        "Usage: morphs split [file]\n\nSplits morphs from the listed file into multiple files, according to hard-coded criteria."
    ],
    "help": [
        command_help,
        "Get information about a particular command",
        "Usage: morphs help [command]\n\nProvides information about the given command."
    ]
}

def command_list():
    for key, values in commands.items():
        print(" - " + key.ljust(5) + "\t" + values[1])

def input_error(message):
    print()
    print(message)
    command_list()
    print()
    exit(1)

# Process command line input
if __name__ == '__main__' and len(sys.argv) > 0:
    if len(sys.argv) == 1:
        input_error("Enter a command. Available commands:")

    command_input = sys.argv[1]
    args = sys.argv[2:]

    if command_input in commands:
        commands[command_input][0](args)
    else:
        input_error("Command '" + command_input + "' not recognized. Available commands:")
