import src.tools.morphs.morphs_files as file_tool

from src.tools.morphs.hardcoded.search import matches as matches_hardcoded
from src.morphs.expressions import evaluate_expression

import json

def get_matches(morphs, matches):
    matches_found = []
    for morph in morphs:
        if matches(morph):
            matches_found += [morph]

    return matches_found

def matches_expression(morph, expression):
    return evaluate_expression(expression, morph)

def get_count(morphs):
    return len(morphs)

def get_list(morphs):
    if len(morphs) == 0:
        return "0 matches found"

    output = str(len(morphs)) + " matches found:\n"
    for morph in morphs:
        output += " - " + morph["key"] + "\n"

    return output

def search_morphs(files, task, expression=None):
    # Read in morphs
    morphs = file_tool.morphs_from_files(files)

    # Find matches
    if expression != None:
        try:
            expression = json.loads(expression)
        except:
            print("ERROR: failed to parse expression:")
            print(expression)
            exit(1)

        matches = get_matches(morphs, lambda m: matches_expression(m, expression))
    else:
        matches = get_matches(morphs, matches_hardcoded)

    # Output
    if task == "count":
        print("Matching morphs: " + str(get_count(matches)))
    elif task == "list":
        print(get_list(matches))
