import getopt
import os
import sys

from src.tools.linter.imports import lint_imports

def lint(file):
	lint_imports(file)

# Process command line input
if __name__ == '__main__' and len(sys.argv) > 0:
	if len(sys.argv) == 0:
		print("ERROR: Must specify filename/s")
		sys.exit(1)

	for file in sys.argv[1:]:
		lint(file)
