import json
import sys

def morphs_from(file):
    with open("data/" + file) as morph_data:
        return json.load(morph_data)