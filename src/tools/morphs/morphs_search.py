import src.tools.morphs.morphs_files as file_tool

def get_matches(morphs):
    matches_found = []
    for morph in morphs:
        if matches(morph):
            matches_found += [morph]

    return matches_found

def matches(morph):
    # Write code for your specifier here
    return False

def get_count(morphs):
    return len(morphs)

def get_list(morphs):
    output = str(len(morphs)) + " matches found:"
    for morph in morphs:
        output += " - " + morph["key"] + "\n"

    return output

def search_morphs(files, task):
    # Read in morphs
    morphs = file_tool.morphs_from_files(files)

    # Find matches
    matches = get_matches(morphs)

    # Output
    if task == "count":
        print("Matching morphs: " + str(get_count(matches)))
    elif task == "list":
        print(get_list(matches))
