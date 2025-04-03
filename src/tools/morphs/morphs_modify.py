import getopt
import sys

import src.tools.morphs.morphs_files as file_tool
import src.tools.morphs.morphs_format as format

def modify(morph):
    # Write code to modify the morph here, returning the new version
    return morph

# Write groups to the specified filenames
def write(morphs, filename):
    asorted = format.sort(morphs)
    formatted = format.format(asorted)
    file_tool.write_formatted_to(formatted, filename)

def modify_morphs(files):
    for file in files:
        # Read in morphs
        morphs = file_tool.get_morphs_from(file)

        # Modify morphs
        morphs = [modify(m) for m in morphs]

        # Write back to file
        write(morphs, file)
