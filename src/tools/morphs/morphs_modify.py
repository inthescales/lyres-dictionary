import getopt
import sys

import morphs_files as file_tool
import morphs_format as format

def modify(morph):
    # Write code to modify the morph here, returning the new version
    options = ["count", "mass", "singleton", "uncountable"]
    for option in options:
        if "tags" in morph and option in morph["tags"]:
            morph["noun-countability"] = option
            morph["tags"].remove(option)
    return morph

# Write groups to the specified filenames
def write(morphs, filename):
    asorted = format.sort(morphs)
    formatted = format.format(asorted)
    file_tool.write_formatted_to(formatted, filename)

if __name__ == '__main__':
    # Read args
    try:
        opts, params = getopt.getopt(sys.argv[1:], "", [])
    except getopt.GetoptError:
        print('ERROR: getopt error')
        sys.exit(2)

    files = params

    if len(files) == 0:
        print("ERROR: Must specify at least one morphs file")
        sys.exit(0)

    for file in files:
        # Read in morphs
        morphs = file_tool.get_morphs_from(file)

        # Modify morphs
        morphs = [modify(m) for m in morphs]

        # Write back to file
        write(morphs, file)
