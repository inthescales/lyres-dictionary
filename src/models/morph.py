import src.former as former

from src.expressions import evaluate_expression
from src.morphothec import Morphothec

class Morph:
    
    def __init__(self, key, morphothec):
        self.morphothec = morphothec
        self.base = morphothec.morph_for_key[key]
        self.morph = self.base.copy()
        
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
        
    def get_type(self):
        if self.morph["type"] == "derive":
            return self.morph["to"]
        else:
            return self.morph["type"]
        
    def is_root(self):
        return self.morph["type"] in ["noun", "verb", "adj"]
        
    def suffixes(self):
        if "suffixes" not in self.morph:
            return None
        else:
            return self.morph["suffixes"]
        
    def has_tag(self, target):

        if "tags" in self.morph:
            if target in self.morph["tags"]:
                return True

        return False

    def meets_requirements(self, env):

        # No requirements to check, it's ok
        if not "requires" in self.morph:
            return True
        
        requirements = self.morph["requires"]
        keys = requirements.keys()
        if len(keys) != 1:
            print("Error: currently, requirement can only have one referent child")
            sys.exit(1)
            
        if "precedes" in keys:
            if env.next == None:
                print("Error: precedes block but no following morph given")
                sys.exit(1)
            
            if not evaluate_expression(requirements["precedes"], env.next.as_dict(env.next_env(self))):
                return False
        
        if "follows" in keys:
            if env.prev == None:
                print("Error: follows block but no following morph given")
                sys.exit(1)

            if not evaluate_expression(requirements["follows"], env.prev.as_dict(env.prev_env(self))):
                return False
        
        return True
