import getopt
import sys

import src.tablemaker.table as table
import src.tablemaker.evolution_table as evolution_table
import src.tablemaker.combination_table as combination_table

# Process command line input
if __name__ == '__main__' and len(sys.argv) > 0:
    
    list_root = "assets/word_lists/"
    
    mode = None
    list_path = None

    # Error cases
    def error_unrecognized_args():
        print("Error: Unrecognized arguments")
        sys.exit(1)
    
    def error_no_list():
        print("Error: must specify a word list")
        sys.exit(1)
    
    def error_no_mode():
        print("Error: no mode specified")
        sys.exit(1)
    
    # Get args
    try:
        opts, params = getopt.getopt(sys.argv[1:], "el:c", ["evolution", "list=", "combination"])
    except getopt.GetoptError:
        error_unrecognized_args()
        sys.exit(2)

    # Process args
    for opt, arg in opts:
        if opt in ["-e", "--evolution"]:
            mode = "evolution"
        elif opt in ["-c", "--combination"]:
            mode = "combination"
        elif opt in ["-l", "--list"]:
            list_path = arg

    if mode == "evolution":
        if list_path == None:
            error_no_list()
        
        path = list_root + list_path
        if len(list_path) < 4 or list_path[-4:] != ".csv":
            path += ".csv"

        file = open(path)
        raw = file.read()
        words = raw.split(",\n")

        table = evolution_table.make_table_oe_ne(words)

        print(table)
    elif mode == "combination":
        table = combination_table.combine()
        print(table)
    else:
        error_no_mode()
