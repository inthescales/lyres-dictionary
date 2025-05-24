import getopt
import os
import sys

from src.utils.terminal import Color, color_text
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
    paths = params
    
    # Process args
    for opt, arg in opts:
        if opt in ["-r", "--recursive"]:
            recurse = True

    files = []
    for path in paths:
        if recurse:
            files += find_files(path)
        else:
            files += [path]

    print("Linting " + str(len(files)) + " files")

    result = 0
    for file in files:
        result = max(result, lint(file))

    if result == 0:
        print(color_text(Color.green, "Linter succeeded"))
        print()
        sys.exit(0)
    elif result == 1:
        print(color_text(Color.yellow, "Linter made code changes"))
        print()
        sys.exit(1)
    elif result == 2:
        print(color_text(Color.red, "Linter found errors"))
        print()
        sys.exit(2)
