import json
import os

# Returns all morph files in the given root data directory
def all_morph_files(root_dir):
    all_files = os.listdir("./" + root_dir)
    return [root_dir + "/" + file for file in all_files if file.startswith("morphs-") and file.endswith(".json")]

# Returns a list of morphs from the file
def get_morphs_from(file):
    with open(file) as morph_data:
        return json.load(morph_data)

# Returns all morphs from the given files
def morphs_from_files(files):
    raw_morphs = []
    for file in files:
        raw_morphs += get_morphs_from(file)

    return raw_morphs

# Write formatted morphs to the given file
def write_formatted_to(formatted, file):
    with open(file, "w") as f:
        f.write(formatted)
