import getopt
import sys

import morphs_files as file_tool

def get_matches(morphs):
    matches_found = []
    for morph in morphs:
        if matches(morph):
            matches_found += [morph]

    return matches_found

def matches(morph):
    # Write code for your specifier here
    return True

def get_count(morphs):
    return len(morphs)

def get_list(morphs):
    output = str(len(morphs)) + " matches found:"
    for morph in morphs:
        output += " - " + morph["key"] + "\n"

    return output

if __name__ == '__main__':
    # Read args
    try:
        opts, params = getopt.getopt(sys.argv[1:], "cl", ["count", "list"])
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
        print("ERROR: must specify task")
        sys.exit(0)

    files = params

    # Read in morphs
    morphs = []
    for file in files:
        morphs += file_tool.get_morphs_from(file)

    # Find matches
    matches = get_matches(morphs)

    # Output
    if task == "count":
        print("Total morphs: " + str(get_count(matches)))
    elif task == "list":
        print(get_list(matches))
