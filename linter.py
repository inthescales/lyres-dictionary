import getopt
import os
import sys

from src.tools.linter.imports import lint_imports

def lint(file):
    return lint_imports(file)

def find_files(root):
    res = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if '.' in file:
                extension = file.rsplit('.', 1)[1]
                if extension == "py":
                    res.append(root + "/" + file)

    return res

# Process command line input
if __name__ == '__main__' and len(sys.argv) > 0:
    if len(sys.argv) == 0:
        print("ERROR: Must specify filename/s")
        sys.exit(1)

    # Get args
    try:
        opts, params = getopt.getopt(sys.argv[1:], "r", ["recursive"])
    except getopt.GetoptError:
        sys.exit(2)

    recurse = False
    path = sys.argv[-1]
    
    # Process args
    for opt, arg in opts:
        if opt in ["-r", "--recursive"]:
            recurse = True

    if recurse:
        files = find_files(path)
    else:
        files = [path]

    print("Linting " + str(len(files)) + " files")

    result = 0
    for file in files:
        result = max(result, lint(file))

    if result == 0:
        print("Linting succeeded" + "\n")
        sys.exit(0)
    elif result == 1:
        print("Linter made code changes" + "\n")
        sys.exit(1)
    elif result == 2:
        print("Linting found errors" + "\n")
        sys.exit(2)
