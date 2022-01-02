import random

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
        dict_["form"] = self.get_form(env)
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
                    if env.next is None or not evaluate_expression(case["precedes"], env.next.as_dict(env)):
                        continue

                if "follows" in case:
                    if env.prev is None or not evaluate_expression(case["follows"], env.prev.as_dict(env)):
                        continue
                        
                self.apply_override(exception)
    
    def apply_override(self, override):
        for key, value in override.items():
            if key != "case":
                self.morph[key] = value
    
    def get_form(self, env):
        form = ""
        
        if env.next:
            next_morph = env.next.morph
        else:
            next_morph = None
            
        if env.prev:
            last_morph = env.prev.morph
        else:
            last_morph = None
    
        # Get the proper form of the morph
        if env.next != None:

            # Follow special assimilation rules if there are any
            if "assimilation" in self.morph:

                next_letter = list(next_morph["key"])[0]

                matched_case = None
                star_case = None

                for case, sounds in self.morph["assimilation"].items():

                    if "*" in sounds:
                        star_case = case

                    if next_letter in sounds:
                        matched_case = case
                        break

                if matched_case:
                    case = matched_case
                elif star_case:
                    case = star_case

                if case == "link":
                    form = self.morph["link"]
                elif case == "link-assim":
                    form = self.morph["link-assim"]
                elif case == "cut":
                    form = self.morph["link"] + "/"
                elif case == "double":
                    form = self.morph["link-assim"] + next_letter
                elif case == "nasal":
                    if next_letter == 'm' or next_letter == 'p' or next_letter == 'b':
                        form = self.morph["link-assim"] + 'm'
                    else:
                        form = self.morph["link-assim"] + 'n'
                else:
                    form = case


            # Default rules
            else:

                # Usually we'll use link form
                if "link" in self.morph:
                    form = self.morph["link"]

                # Verbs or verbal derivations need to take participle form into account
                elif self.morph["type"] == "verb" or (self.morph["type"] == "derive" and self.morph["to"] == "verb"):
                    if next_morph and "participle-type" in next_morph:
                        if next_morph["participle-type"] == "present":
                            form = self.morph["link-present"]
                        elif next_morph["participle-type"] == "perfect":
                            form = self.morph["link-perfect"]
                    elif "link-verb" in self.morph:
                        form = self.morph["link-verb"]
                    else:
                        form = self.morph["link-perfect"]

                # Use final form if nothing overrides
                else:
                    form = self.morph["final"]

        # The final morph form
        else:
            if self.morph["type"] == "prep":
                form = self.morph["link"]
            else:
                if "final" in self.morph:
                    form = self.morph["final"]
                else:
                    # If there's no final form, use link
                    form = self.morph["link"]
        
        if isinstance(form, list):
            form = random.choice(form)
        
        return form
    
    def get_gloss(self, env):
        
        # Special case for prep-relative-to-noun cases (e.g. sub-limin-al)
        if env.prev and ((env.prev.get_type() == "noun" and env.anteprev and env.anteprev.get_type() == "prep" ) or (self.get_type() == "verb" and env.prev.get_type() == "prep")) and "gloss-relative" in self.morph:
            return self.morph["gloss-relative"]
        
        if "gloss" in self.morph:
            if self.morph["type"] in ["noun", "verb"] and len(self.morph["gloss"].split(" ")) == 1:
                return "[" + self.morph["gloss"] + "]"
            else:
                return self.morph["gloss"]
        else:
            
            if env.next:
                if "gloss-link" in self.morph:
                    return self.morph["gloss-link"]
            else:
                if "gloss-final" in self.morph:
                    return self.morph["gloss-final"]
            

            if self.get_type() == "prep" or self.get_type() == "prefix":
                relative = env.next
            else:
                relative = env.prev

            if relative and "gloss-" + relative.get_type() in self.morph:
                return self.morph["gloss-" + relative.get_type()]
        
        print("ERROR - failed to find gloss for " + self.morph["key"])
        
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

# Morph Helpers ===============================

def check_req(morph, env):

    # No requirements to check, it's ok
    if not "requires" in morph:
        return True
    
    requirements = morph["requires"]
    keys = requirements.keys()
    if len(keys) != 1:
        print("Error: currently, requirement can only have one referent child")
        sys.exit(1)
        
    passes = True
        
    if "precedes" in keys:
        if env.next == None:
            print("Error: precedes block but no following morph given")
            sys.exit(1)
        
        passes = passes and evaluate_expression(requirements["precedes"], env.next.morph)
    
    if "follows" in keys:
        if env.prev == None:
            print("Error: follows block but no following morph given")
            sys.exit(1)

        passes = passes and evaluate_expression(requirements["follows"], env.prev.morph)
    
    return passes
