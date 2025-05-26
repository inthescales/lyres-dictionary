import random

import src.generation.former as former

from src.morphs.expressions import evaluate_expression
from src.morphs.requirements import meets_requirements

class Morph:
    
    def __init__(self, base_dict):
        self.base = base_dict
        self.morph = self.base.copy()
        self.seed = random.randint(0, 100)
    
    # TODO: Maybe move this to morphothec
    @classmethod
    def with_key(self, key, morphothec):
        return Morph(morphothec.morph_for_key[key])

    def __eq__(self, other):
        if other is None:
            return False
        
        return self.morph["key"] == other.morph["key"]
    
    def as_dict(self, env):
        dict_ = self.morph.copy()
        dict_["form"] = former.form(self, env)
        dict_["final"] = env.is_final()
        return dict_

    def refresh(self, env):
        self.morph = self.base.copy()
        self.morph["exception"] = ""

        if "exception" in self.base:
            for exception in self.base["exception"]:
                # Assume there's a match, and negate that if it doesn't meet a requirement
                # Match the first case that we fill
                match = True
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
        
    def get_key(self):
        return self.morph["key"]
        
    def get_type(self):
        # TODO: There should be a way to get the base type vs effective type
        if self.morph["type"] == "suffix":
            return self.morph["derive-to"]
        else:
            return self.morph["type"]
        
    def is_root(self):
        return self.morph["type"] in ["noun", "verb", "adj"]

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
        
    def suffixes(self):
        if "suffixes" not in self.morph:
            return None
        else:
            return self.morph["suffixes"]
        
    def tags(self):
        if "tags" in self.morph:
            return self.morph["tags"]
        else:
            return []

    def has_tag(self, target):
        if "tags" in self.morph:
            if target in self.morph["tags"]:
                return True

        return False

    def meets_requirements(self, env, filter_frequency=True):
        return meets_requirements(self, env, filter_frequency)
