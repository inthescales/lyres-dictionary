import json
import sys

def get_morphs_from(file):
    with open(file) as morph_data:
        return json.load(morph_data)

def write_formatted_to(formatted, file):
    with open(file, "w") as f:
        f.write(formatted)

