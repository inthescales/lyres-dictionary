import sys

import src.tools.morphs.morphs_format as format

from src.tools.morphs.morphs_files import morphs_from

def morphs_from_all(files):
    raw_morphs = []
    for file in files:
        raw_morphs += morphs_from(file)

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
