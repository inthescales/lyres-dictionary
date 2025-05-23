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

    success = True
    for file in files:
        success = success and lint(file)

    if success:
        print("Linter passed")
        sys.exit(0)
    else:
        print("Linter failed")
        sys.exit(1)
