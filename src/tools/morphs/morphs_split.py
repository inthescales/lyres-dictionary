import sys

import src.tools.morphs.morphs_files as file_tool
import src.tools.morphs.morphs_format as morphs_format

# Filenames for the new split files
# The indices should match the groups used below in get_group(...)
filenames = [
]

# Determine the group for the given morph
def get_group(morph):
    # Write code for dividing morphs into groups here
    return 0

# Divide morphs into groups
def group(morphs):
    groups = {}
    for morph in morphs:
        group = get_group(morph)
        if not group in groups:
            groups[group] = []

        groups[group] += [morph]

    return groups

# Write groups to the specified filenames
def write(groups, filenames):
    if len(filenames) < len(groups):
        print("ERROR: Not enough filenames for groups")
        sys.exit(0)

    group_keys = sorted(list(groups.keys()))
    for i in range(0, len(group_keys)):
        morphs = groups[i]

        if len(morphs) > 0:
            asorted = morphs_format.sort(morphs)
            formatted = morphs_format.format(asorted)
            file_tool.write_formatted_to(formatted, filenames[i])

def split_morphs(file):
    # Read in morphs
    morphs = file_tool.get_morphs_from(file)

    # Divide into groups
    groups = group(morphs)
    
    # Write to output files
    #write(groups, filenames)
