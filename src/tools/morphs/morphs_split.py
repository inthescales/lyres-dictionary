import getopt
import sys

import morphs_files as file_tool
import morphs_format as format

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
            asorted = format.sort(morphs)
            formatted = format.format(asorted)
            file_tool.write_formatted_to(formatted, filenames[i])

if __name__ == '__main__':
    # Read args
    try:
        opts, params = getopt.getopt(sys.argv[1:], "", [])
    except getopt.GetoptError:
        print('ERROR: getopt error')
        sys.exit(2)

    file = params[0]

    # Read in morphs
    morphs = file_tool.get_morphs_from(file)

    # Divide into groups
    groups = group(morphs)

    # Write to output files
    write(groups, filenames)
