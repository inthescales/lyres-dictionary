import getopt
import os
import sys

from src.tools.morphs.morphs_format import format_morphs
from src.tools.morphs.morphs_validate import validate_morphs
from src.tools.morphs.morphs_modify import modify_morphs
from src.tools.morphs.morphs_merge import merge_morphs
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

# Process command line input
if __name__ == '__main__' and len(sys.argv) > 0:
    
    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "format":
        command_format(args)
    elif command == "validate":
        command_validate(args)
    elif command == "modify":
        command_modify(args)
    elif command == "merge":
        command_merge(args)
    else:
        print("Command '" + command + "' not recognized. Available commands: format, validate")
