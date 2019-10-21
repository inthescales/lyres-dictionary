import json
    
class Morphary:
    
    def __init__(self, files):

        self.morph_for_key = {}
        self.roots = []
        self.type_morphs = {}
        self.morphs_from = {}
        self.words = []
        
        for file in files:
            
            errors = 0
            
            with open(file) as morph_data:

                raw_morphs = json.load(morph_data)
                for morph in raw_morphs:

                    if not validate_morph(morph):
                        if "key" in morph:
                            print("ERROR - invalid morph for key " + morph["key"])
                        else:
                            print("ERROR - invalid morph:")
                            print(morph)
                        errors += 1
                        continue

                    self.morph_for_key[morph["key"]] = morph

                    morph_type = morph["type"]
                    if morph_type != "derive":

                        if not morph_type in self.type_morphs:
                            self.type_morphs[morph_type] = []

                        self.type_morphs[morph_type].append(morph["key"])

                        if morph_type in ["noun", "adj", "verb"]:
                            self.roots.append(morph)

                    else:

                        for from_type in morph["from"].split(","):
                            if not from_type in self.morphs_from:
                                self.morphs_from[from_type] = []

                            if "tags" not in morph or not "no-gen" in morph["tags"]:
                                self.morphs_from[from_type].append(morph["key"])
                                
                if errors > 0:
                    print("Exiting with " + errors + " validation errors")
                    exit(0)

def validate_morph(morph):
    
    if not "key" in morph:
        print(" - key is missing")
        return False
    
    if not "type" in morph:
        print(" - type is missing")
        return False
    
    morph_type = morph["type"]
    
    if morph_type == "noun":
        if not "link" in morph:
            print(" - noun lacks link form")
            return False
        elif not ("tags" in morph and ("count" in morph["tags"] or "mass" in morph["tags"])):
            print(" - noun must have tag 'count' or 'mass'")
            return False
    
    elif morph_type == "verb":
        if not ("link-present" in morph and "link-perfect" in morph and "final" in morph):
            print(" - verbs require 'link-present', 'link-perfect', and 'final'")
            return False
    
    elif morph_type == "derive":
        if not ("from" in morph and "to" in morph):
            print(" - derive morphs must have 'from' and 'to'")
            return False
    
    return True
