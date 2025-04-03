import getopt
import os
import sys

from src.tools.morphs.morphs_format import format_morphs
from src.tools.morphs.morphs_validate import validate_morphs
import src.tools.morphs.morphs_files as file_tool

data_dir = "./data"
meta_dir = "./data/meta"

# Process command line input
if __name__ == '__main__' and len(sys.argv) > 0:
    
    command = sys.argv[1]

    if command == "format":
        try:
            opts, params = getopt.getopt(sys.argv[2:], "t", ["test"])
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

    elif command == "validate":
        params = sys.argv[2:]

        if len(params) == 0:
            morphs_files = file_tool.all_morph_files(data_dir)
            print("Validating " + str(len(morphs_files)) + " files")
        else:
            print("Validating " + str(len(params)) + " files")
            morphs_files = params

        validate_morphs(morphs_files, meta_dir)

    else:
        print("Command '" + command + "' not recognized. Available commands: format, validate")
