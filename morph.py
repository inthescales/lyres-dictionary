import getopt
import os
import sys

from src.tools.morphs.morphs_format import format_morphs
import src.tools.morphs.morphs_files as file_tool

commands = {
    "format": ["", "[-r (replace)] [-s (sort)] [files]"]
}

data_dir = "./data"
meta_dir = "./data/meta"

# Process command line input
if __name__ == '__main__' and len(sys.argv) > 0:
    
    command_name = sys.argv[1]

    if command_name not in commands:
        print("ERROR: command '" + command + "' not recognized. Available commands are:")
        for key, value in commands.items():
            print(" - " + key + " " + value[1])
        exit(1)

    command = commands[command_name]

    if command_name == "format":
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
