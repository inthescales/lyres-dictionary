import json

import src.expressions as expressions  
import src.morph_validator as validator
    
class Morphothec:
    
    class Language:
        def __init__(self):
            self.roots = []
            self.type_morphs = {}
            self.morphs_from = {}
        
        def add_morph(self, morph):
            morph_key = morph["key"]
            morph_type = morph["type"]

            if "tags" in morph and "no-gen" in morph["tags"]:
                return

            if morph_type != "derive":
                if not morph_type in self.type_morphs:
                    self.type_morphs[morph_type] = []

                self.type_morphs[morph_type].append(morph_key)

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

                    self.morphs_from[from_type].append(morph_key)
    
    def __init__(self, files):
        self.morph_for_key = {}
        self.languages = {}
        
        for file in files:
            
            errors = 0
            
            with open(file) as morph_data:

                raw_morphs = json.load(morph_data)
                for morph in raw_morphs:

                    if not validator.validate_morph(morph):
                        if "key" in morph:
                            print("ERROR - invalid morph for key " + morph["key"])
                        else:
                            print("ERROR - invalid morph:")
                            print(morph)
                        errors += 1
                        continue
                    
                    if not morph["origin"] in self.languages:
                        self.languages[morph["origin"]] = self.Language()
                    
                    self.morph_for_key[morph["key"]] = morph
                    language = self.languages[morph["origin"]]
                    language.add_morph(morph)
                            
                if errors > 0:
                    print("Exiting with " + str(errors) + " validation errors")
                    exit(0)
    
    def filter_type(self, morph_type, language="latin", morph_filter=None):

        if morph_filter is None:
            return self.languages[language].type_morphs[morph_type]
        
        selected = []
        for morph in self.languages[language].type_morphs[morph_type]:
            if expressions.evaluate_expression(morph_filter, self.morph_for_key[morph]):
                selected.append(morph)
        
        return selected

    def filter_appends_to(self, base_type, language="latin", morph_filter=None):
        if morph_filter is None:
            return self.languages[language].morphs_from[base_type]
        
        selected = []
        for morph in self.morphs_from[base_type]:
            if expressions.evaluate_expression(morph_filter, self.morph_for_key[morph]):
                selected.append(morph)
        
        return selected

    def root_count_for_language(self, language):
        if not language in self.languages:
            print("Error: language \"" + language + "\" not found.")
            return 0
                  
        return len(self.languages[language].roots)
