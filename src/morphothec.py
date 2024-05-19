import os
import json

import src.expressions as expressions  
import src.morph_validator as validator

from src.logging import Logger
    
class Morphothec:
    
    class Language:
        def __init__(self):
            self.roots = []
            self.type_morphs = {}
            self.morphs_from = {}
            self.morphs_before = {}
        
        def add_morph(self, morph):
            morph_key = morph["key"]
            morph_type = morph["type"]

            # Skip this morph if it should not be generated
            if "tags" in morph and "no-gen" in morph["tags"]:
                return

            # Add this morph to the generation lists
            if morph_type == "derive":
                if isinstance(morph["derive-from"], str):
                    from_types = [morph["derive-from"]]
                else:
                    from_types = morph["derive-from"]

                for from_type in from_types:
                    if not from_type in self.morphs_from:
                        self.morphs_from[from_type] = []

                    self.morphs_from[from_type].append(morph_key)

            elif morph_type in ["prefix", "prep"]:
                if isinstance(morph["prefix-on"], str):
                    before_types = [morph["prefix-on"]]
                else:
                    before_types = morph["prefix-on"]

                for before_type in before_types:
                    if not before_type in self.morphs_before:
                        self.morphs_before[before_type] = []

                    self.morphs_before[before_type].append(morph_key)

            else:
                if not morph_type in self.type_morphs:
                    self.type_morphs[morph_type] = []

                self.type_morphs[morph_type].append(morph_key)

                if morph_type in ["noun", "adj", "verb"]:
                    self.roots.append(morph)


    def __init__(self, input):
        self.morph_for_key = {}
        self.languages = {}

        files = []

        if isinstance(input, list):
            files = input
        elif isinstance(input, str):
            all_files = os.listdir("./" + input)
            files = [input + file for file in all_files if file.startswith("morphs-") and file.endswith(".json")]
        else:
            Logger.error("invalid morphothec initialization")
        
        if len(files) == 0:
            Logger.error("no morph files found")

        for file in files:
            
            errors = 0
            
            with open(file) as morph_data:

                raw_morphs = json.load(morph_data)
                for morph in raw_morphs:

                    # Check that the morph is valid
                    if not validator.validate_morph(morph):
                        errors += 1
                        continue
                    
                    # Check for key collisions
                    if morph["key"] in self.morph_for_key:
                        Logger.error("duplicate morph key " + morph["key"])
                        errors += 1
                        continue

                    if not morph["origin"] in self.languages:
                        self.languages[morph["origin"]] = self.Language()
                    
                    self.morph_for_key[morph["key"]] = morph
                    language = self.languages[morph["origin"]]
                    language.add_morph(morph)
                            
                if errors > 0:
                    Logger.error("morphothec validation found " + str(errors) + " errors")
                    exit(0)
    
    def filter_type(self, morph_type, language, morph_filter=None):

        if morph_filter is None:
            return self.languages[language].type_morphs[morph_type]
        
        selected = []
        for morph in self.languages[language].type_morphs[morph_type]:
            if expressions.evaluate_expression(morph_filter, self.morph_for_key[morph]):
                selected.append(morph)
        
        return selected

    def filter_prepends_to(self, base_type, language, morph_filter=None):
        if not base_type in self.languages[language].morphs_before:
            return []

        if morph_filter is None:
            return self.languages[language].morphs_before[base_type]
        
        selected = []
        for morph in self.languages[language].morphs_before[base_type]:
            if expressions.evaluate_expression(morph_filter, self.morph_for_key[morph]):
                selected.append(morph)

        return selected

    def filter_appends_to(self, base_type, language, morph_filter=None):
        if not base_type in self.languages[language].morphs_from:
            return []

        if morph_filter is None:
            return self.languages[language].morphs_from[base_type]
        
        selected = []
        for morph in self.languages[language].morphs_from[base_type]:
            if expressions.evaluate_expression(morph_filter, self.morph_for_key[morph]):
                selected.append(morph)
        
        return selected

    def root_count_for_language(self, language):
        if not language in self.languages:
            Logger.error("language \"" + language + "\" not found.")
            return 0
                  
        return len(self.languages[language].roots)
