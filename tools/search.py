import json

def scan(files):
    
    for file in files:
        
        with open(file) as morph_data:

            raw_morphs = json.load(morph_data)

            for morph in raw_morphs:

                if (morph["type"] == "verb" or (morph["type"] == "derive" and morph["to"] == "verb")) and not "conjugation" in morph:
                    print("GOT EM: " + morph["key"])

files = ["data/morphs-latin.json"]

scan(files)
