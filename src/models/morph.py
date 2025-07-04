import random

import src.generation.former as former
import src.utils.helpers as helpers

from src.morphs.expressions import evaluate_expression
from src.morphs.requirements import meets_requirements

class Morph:
    
    def __init__(self, base_dict, sense=None):
        self.base = base_dict
        self.morph = self.base.copy()
        self.seed = random.randint(0, 100)

        self.sense = self.choose_sense(sense)
    
    # TODO: Maybe move this to morphothec
    @classmethod
    def with_key(self, key, morphothec, sense=None):
        return Morph(morphothec.morph_for_key[key], sense)

    def __eq__(self, other):
        if other is None:
            return False
        
        return self.morph["key"] == other.morph["key"]
    
    def as_dict(self, env):
        dict_ = self.morph.copy()
        dict_["form"] = former.form(self, env)
        dict_["final"] = env.is_final()
        return dict_

    # Expression processing ==========

    def meets_requirements(self, env, filter_frequency=True):
        return meets_requirements(self, env, filter_frequency)

    def refresh(self, env):
        self.morph = self.base.copy()
        self.morph["exception"] = ""

        # Apply all exceptions for which the requirements are met
        if "exception" in self.base:
            for exception in self.base["exception"]:
                case = exception["case"]
                
                if "precedes" in case:
                    if env.next is None or not evaluate_expression(case["precedes"], env.next.as_dict(env.next_env(self))):
                        continue

                if "follows" in case:
                    if env.prev is None or not evaluate_expression(case["follows"], env.prev.as_dict(env.prev_env(self))):
                        continue
                
                self.apply_override(exception)
    
    def apply_override(self, override):
        for key, value in override.items():
            if key != "case":
                self.morph[key] = value

                if "senses" not in self.morph:
                    self.sense[key] = value

    # Data provision ==========
        
    def get_key(self):
        return self.morph["key"]
        
    def get_type(self):
        # TODO: There should be a way to get the base type vs effective type
        if self.morph["type"] == "suffix":
            return self.morph["derive-to"]
        else:
            return self.morph["type"]

    def get_base_type(self):
        return self.morph["type"]

    # Form -----

    def has_raw_form(self):
        return "form-raw" in self.morph

    def get_raw_form(self):
        if "form-raw" in self.morph:
            return self.morph["form-raw"]

    def get_all_raw_forms(self, include_alt):
        forms = helpers.list_if_not(self.morph["form-raw"])
        if "form-raw-alt" in self.morph and include_alt:
            forms += helpers.list_if_not(self.morph["form-raw-alt"])

        return forms

    def has_canon_form(self):
        return "form-canon" in self.morph

    def get_canon_form(self):
        return self.morph["form-canon"]

    def has_stem_form(self):
        return "form-stem" in self.morph

    def get_stem_form(self):
        return self.morph["form-stem"]

    def has_final_form(self):
        return "form-final" in self.morph

    def get_final_form(self):
        return self.morph["form-final"]

    def has_form_assimilation(self):
        return "form-assimilation" in self.morph

    def get_assimilation_base(self):
        return self.morph["form-assimilation"]["base"]

    def get_assimilation_stem(self):
        if "stem" not in self.morph["form-assimilation"]:
            print(self.morph["form-assimilation"])
            exit(0)
        return self.morph["form-assimilation"]["stem"]

    def get_assimilation_map(self):
        assimilation_map = {}
        for case, sounds in self.morph["form-assimilation"]["case"].items():
            for sound in sounds:
                if sound not in assimilation_map:
                    assimilation_map[sound] = case
                else:
                    Logger.error("Repeated assimilation sound for key " + morph.get_key())

        return assimilation_map

    def get_latin_present_stem(self):
        return self.morph["form-stem-present"]

    def get_latin_perfect_stem(self):
        return self.morph["form-stem-perfect"]

    def get_latin_suffix_stem_type(self):
        return self.morph["derive-participle"]

    # Other -----
        
    def suffixes(self):
        if "suffixes" not in self.morph:
            return None
        else:
            return self.morph["suffixes"]

    def tags(self):
        if "tags" in self.sense:
            return self.sense["tags"]
        else:
            return []

    def has_tag(self, target):
        if "tags" in self.sense:
            if target in self.sense["tags"]:
                return True

        return False

    def get_origin(self):
        return self.morph["origin"]

    # Senses -------------------

    # Get the sense with the given identifier (string or integer index), if any
    def get_sense(self, ident):
        if type(ident) == str:
            return next(filter(lambda x: x.id == ident, self.all_senses))
        elif type(ident) == int and ident < len(self.all_senses):
            return self.all_senses[ident]
        else:
            Logger.error("Invalid sense ID " + str(ident))

    # Get all senses
    def all_senses(self):
        if "senses" not in self.morph:
            return [self.default_sense()]
        else:
            return self.morph["senses"]

    # The sense to be used if the morph has only a single sense
    def default_sense(self):
        return self.morph

    # Pick a sense according to rules and randomness
    def random_sense():
        return random.Random(self.seed).choice(self.all_senses())

    # Choose the sense to be used as the main one for this morph
    def choose_sense(self, ident):
        if "senses" in self.morph:
            if ident != None:
                return self.get_sense(ident)
            else:
                return self.random_sense()
        else:
            return self.default_sense()

    # Syntheses
    
    def is_root(self):
        return self.morph["type"] in ["noun", "verb", "adj", "number"]

    def is_prefix(self):
        return self.morph["type"] in ["prefix", "prep"]

    def is_suffix(self):
        return self.morph["type"] == "suffix"
    
    def is_affix(self):
        return self.is_prefix() or self.is_suffix()

    def final(self):
        return self.has_tag("final")

    def final_ok(self):
        has_form = "form-final" in self.morph or "form" in self.morph or "form-raw" in self.morph
        return not self.has_tag("non-final") and has_form
