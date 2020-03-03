import json

import src.expressions as expressions   
    
class Morphothec:
    
    def __init__(self, files):

        self.morph_for_key = {}
        self.roots = []
        self.type_morphs = {}
        self.morphs_from = {}
        
        for file in files:
            
            errors = 0
            
            with open(file) as morph_data:

                raw_morphs = json.load(morph_data)
                for morph in raw_morphs:

                    if not self.validate_morph(morph):
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
                        if isinstance(morph["from"], str):
                            from_types = [morph["from"]]
                        else:
                            from_types = morph["from"]
                            
                        for from_type in from_types:
                            if not from_type in self.morphs_from:
                                self.morphs_from[from_type] = []

                            if "tags" not in morph or not "no-gen" in morph["tags"]:
                                self.morphs_from[from_type].append(morph["key"])
                                
                if errors > 0:
                    print("Exiting with " + str(errors) + " validation errors")
                    exit(0)
                    
    def filter_type(self, morph_type, morph_filter=None):

        if morph_filter is None:
            return self.type_morphs[morph_type]
        
        selected = []
        for morph in self.type_morphs[morph_type]:
            if expressions.evaluate_expression(morph_filter, self.morph_for_key[morph]):
                selected.append(morph)
        
        return selected

    def filter_appends_to(self, base_type, morph_filter=None):
        if morph_filter is None:
            return self.morphs_from[base_type]
        
        selected = []
        for morph in self.morphs_from[base_type]:
            if expressions.evaluate_expression(morph_filter, self.morph_for_key[morph]):
                selected.append(morph)
        
        return selected

    @classmethod
    def validate_morph(cls, morph):
    
        if not "key" in morph:
            print(" - key is missing")
            return False
    
        if not "type" in morph:
            print(" - type is missing")
            return False

        if not "origin" in morph:
            print(" - origin is missing")
            return False
    
        morph_type = morph["type"]
    
        if morph_type == "noun":
            if not "link" in morph or not "declension" in morph:
                print(" - noun must have 'link' and 'declension'")
                return False
            elif not ("tags" in morph and ("count" in morph["tags"] or "mass" in morph["tags"])):
                print(" - noun must have tag 'count' or 'mass'")
                return False
            elif morph["declension"] not in [0, 1, 2, 3, 4, 5]:
                print(" - invalid declension '" + str(morph["declension"]) + "'")
                return False
    
        elif morph_type == "adj":
            if not "link" in morph or not "declension" in morph:
                print(" - adjective must have 'link' and 'declension'")
                return False
            elif morph["declension"] not in [0, 12, 3]:
                print(" - invalid declension '" + str(morph["declension"]) + "'")
                return False
        
        elif morph_type == "verb":
            if not ("link-present" in morph and "link-perfect" in morph and "final" in morph and "conjugation" in morph):
                print(" - verbs require 'link-present', 'link-perfect', 'final', and 'conjugation'")
                return False
        
            if morph["conjugation"] not in [0, 1, 2, 3, 4]:
                print(" - invalid conjugation '" + str(morph["conjugation"]) + "'")
                return False
    
        elif morph_type == "derive":
            if not ("from" in morph and "to" in morph):
                print(" - derive morphs must have 'from' and 'to'")
                return False
    
        return True
