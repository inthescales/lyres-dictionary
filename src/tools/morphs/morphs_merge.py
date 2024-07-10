import sys

import src.tools.morphs.morphs_files as file_tool
import src.tools.morphs.morphs_format as format

def morphs_from_all(files):
    raw_morphs = []
    for file in files:
        raw_morphs += file_tool.get_morphs_from(file)

    return raw_morphs

def merge(files):
    morphs = morphs_from_all(files)
    asorted = format.sort(morphs)
    formatted = format.format(asorted)
    return formatted

# Prints the merged, sorted, and formatted contents of all specified files
if __name__ == '__main__' and len(sys.argv) > 0:
    if len(sys.argv) < 2:
        print("ERROR: morph merge must take at least two file arguments")
        sys.exit(0)

    files = sys.argv[1:]
    merged = merge(files)
    print(merged)
