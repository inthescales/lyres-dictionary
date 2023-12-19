import getopt
import sys

import src.tablemaker.table as table
import src.tablemaker.evolution_table as evolution_table

list_root = "assets/word_lists/"
oe_inputs = [
        "stel|an",
        "bāt",
        "cȳð|an",
        "frēod",
        "heofon",
        "mete",
        "ċild",
        "dæg",
        "frēond",
        "nama",
        "eorðe",
        "cniht",
        "mægden",
        "hund",
        "bryċġ",
        "gāst",
        "gōd",
        "cēp|an",
        "cēpte",
        "mæt|an",
        "mētte",
        "niht",
        "hlæhh|an",
        "tōh",
        "mann",
        "lamb",
        "nacod"
    ]

# Process command line input
if __name__ == '__main__' and len(sys.argv) > 0:
    
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
        opts, params = getopt.getopt(sys.argv[1:], "el:", ["evolution", "list="])
    except getopt.GetoptError:
        error_unrecognized_args()
        sys.exit(2)

    # Process args
    for opt, arg in opts:
        if opt in ["-e", "--evolution"]:
            mode = "evolution"
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
    else:
        error_no_mode()
