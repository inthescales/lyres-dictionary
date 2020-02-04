import random
from src.morphary import Morphary
import src.inflection as inflection
import src.helpers as helpers

class Morph:
    
    def __init__(self, key, morphary):
        self.morphary = morphary
        self.base = morphary.morph_for_key[key]
        self.prev = None
        self.next = None
        self.refreshMorph()
        
    def __eq__(self, other):
        if other == None:
            return False
        
        return self.morph["key"] == other.morph["key"]
        
    def join(self, next_morph):
        self.next = next_morph
        next_morph.prev = self
        self.refreshMorph()
        next_morph.refreshMorph()
        
    def refreshMorph(self):
        
        def apply(case):
            for key, value in case.items():
                if key != "case":
                    self.morph[key] = value
        
        self.morph = self.base.copy()
        self.morph["exception"] = ""

        if "exception" in self.base:
            for exception in self.base["exception"]:
                # Assume there's a match, and negate that if it doesn't meet a requirement
                # Match the first case that we fill
                match = True
                case = exception["case"]

                if "precedes" in case and self.next:
                    for element in case["precedes"]:
                        if self.next.morph["key"] == element:
                            apply(exception)
                            return

                if "follows" in case and self.prev:
                    for element in case["follows"]:
                        if self.prev.morph["key"] == element:
                            apply(exception)
                            return
    
    def get_form(self):
        
        form = ""
        
        if self.next:
            next_morph = self.next.morph
        else:
            next_morph = None
            
        if self.prev:
            last_morph = self.prev.morph
        else:
            last_morph = None
    
        # Get the proper form of the morph
        if self.next != None:

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
                    elif "link-verb" in morph:
                        form = self.morph["link-verb"]
                    else:
                        form = self.morph["link-perfect"]

                # Use final form if nothing overrides
                else:
                    form = self.morph["final"]

        # The final morph form
        else:
            if not "final" in self.morph:
                print(self.morph)
            form = self.morph["final"]
        
        return form
    
    def get_definition(self):

        # Special case for prep-relative-to-noun cases (e.g. sub-limin-al)
        if self.prev and ((self.prev.get_type() == "noun" and self.prev.prev and self.prev.prev.get_type() == "prep" ) or (self.get_type() == "verb" and self.prev.get_type() == "prep")) and "definition-relative" in self.morph:
            return self.morph["definition-relative"]
        
        if "definition" in self.morph:
            if self.morph["type"] in ["noun", "verb"] and len(self.morph["definition"].split(" ")) == 1:
                return "[" + self.morph["definition"] + "]"
            else:
                return self.morph["definition"]
        else:
            
            if self.next:
                if "definition-link" in self.morph:
                    return self.morph["definition-link"]
            else:
                if "definition-final" in self.morph:
                    return self.morph["definition-final"]
            

            if self.get_type() == "prep" or self.get_type() == "prefix":
                relative = self.next
            else:
                relative = self.prev

            if relative and "definition-" + relative.get_type() in self.morph:
                return self.morph["definition-" + relative.get_type()]
        
        print("ERROR - failed to find definition for " + self.morph["key"])
        
    def get_type(self):
        
        if self.morph["type"] == "derive":
            return self.morph["to"]
        else:
            return self.morph["type"]
        
    def has_tag(self, target):

        if "tags" in self.morph:
            if target in self.morph["tags"]:
                return True

        return False

class Word:
    
    def __init__(self, morphary):
        self.morphs = []
        self.morphary = morphary
        
    def set_keys(self, keys):
        
        self.morphs = []
        
        for key in keys:
            self.morphs.append( Morph(key, self.morphary) )
            
        for i in range(0, len(self.morphs)-1):
            self.morphs[i].join(self.morphs[i+1])
        
    def first_morph(self):
        if len(self.morphs) > 0:
            return self.morphs[0]
        else:
            return None
    
    def last_morph(self):
        if len(self.morphs) > 0:
            return self.morphs[len(self.morphs)-1]
        else:
            return None
        
    def size(self):
        return len(self.morphs)
        
    def grow_to_size(self,target_size):
        
        while self.size() < target_size:
            self.grow()
        
    def grow(self):
        if len(self.morphs) == 0:
            self.morphs = [self.get_seed()]
        else:
            self.next_morph()   
        
    def get_seed(self):      
        type = random.choice(["noun", "adj", "verb", "verb", "verb"])
        key = random.choice(self.morphary.type_morphs[type])
        return Morph(key, self.morphary)     
        
    def next_morph(self):
        current_type = self.get_type()
        last_morph = self.last_morph()
        first_morph = self.first_morph()

        choice = None

        while True:

            # Special chance to add prefixes before verbs.
            # Necessary to inflate their frequency given their small number.
            if self.size() == 1 and current_type == "verb" and not last_morph.has_tag("no-prep") and not first_morph.get_type() in ["prep", "prefix"] and (random.randint(0, 3) == 0 or last_morph.has_tag("always-prep")):
                new_morph = Morph( random.choice(self.morphary.type_morphs["prep"]), self.morphary)
                if not new_morph.has_tag("no-verb"):
                    new_morph.join(first_morph)
                    self.morphs = [new_morph] + self.morphs
                    break

            # Special chance to use the preposition + noun + ate pattern    
            if self.size() == 1 and current_type == "noun" and not last_morph.has_tag("no-prep") and random.randint(0, 8) == 0:
                prep_morph = Morph( random.choice(["in", "ex", "trans", "inter", "sub", "super", "infra", "supra"]), self.morphary )
                end_morph = Morph( random.choice(["ate", "al", "al", "ary", "ify", "ize"]), self.morphary )
                prep_morph.join(first_morph)
                last_morph.join(end_morph)
                self.morphs =  [prep_morph] + self.morphs + [end_morph]
                break

            # Chance to use number + noun + "al" composition
            
            if self.size() == 1 and current_type == "noun" and random.randint(0,15) == 0:
                num_morph = Morph( random.choice(self.morphary.type_morphs["number"]), self.morphary )
                end_morph = Morph( "al-number", self.morphary)
                num_morph.join(first_morph)
                first_morph.join(end_morph)
                self.morphs = [num_morph] + self.morphs + [end_morph]
                break
                
            # Add a prefix to the whole thing
            if self.size() >= 1 and current_type == "verb" and not first_morph.get_type() in ["prep", "prefix"] and random.randint(0, 8) == 0:
                new_morph = Morph( random.choice(self.morphary.type_morphs["prefix"]), self.morphary )
                if not new_morph.has_tag("no-verb"):
                    new_morph.join(first_morph)
                    self.morphs = [new_morph] + self.morphs
                    break

            # Basic morph addition
            else:
                choice = random.choice(self.morphary.morphs_from[current_type])

                if choice == last_morph.morph["key"] or not check_req(self.morphary.morph_for_key[choice], last_morph):
                    choice = None
                else:    
                    new_morph = Morph(choice, self.morphary)
                    last_morph.join(new_morph)
                    self.morphs.append(new_morph)
                    break
    
    def get_type(self):

        return self.last_morph().get_type()
        
    def compose(self):
        word = ""
        morph = None

        for index, morph in enumerate(self.morphs):

            addition = morph.get_form()

            # Handle joining rules
            if len(addition) > 0:

                if index > 0:
                    last_morph = self.morphs[index-1]
                else:
                    last_morph = None

                if index < self.size() - 1:
                    next_morph = self.morphs[index+1]
                else:
                    next_morph = None

                # Spelling changes during joins
                if len(word) > 0:

                    # e.g.: glaci + ify -> glacify
                    if addition[0] == word[-1] and helpers.is_vowel(addition[0]):

                        letter = addition[0]

                        if (not last_morph.get_type() == "prep" and not last_morph.get_type() == "prefix" and not last_morph.get_type() == "number"):
                            addition = addition[1:]
                        elif letter in ["a", "i", "u"]:
                            addition = "-" + addition

                    # Stem change
                    elif morph.has_tag("stem-change") and word[-1] == "i":
                        addition = "e" + addition

                    # Stem raise
                    elif morph.has_tag("stem-raise") and word[-1] == "e":
                        word = word[:-1]
                        addition = "i" + addition

                    # Drop first (sub + emere -> sumere)
                    elif morph.has_tag("drop-first"):
                        addition = addition[1:]

                    elif word[-1] == "/":
                        word = word[:-1]
                        addition = addition[1:]

                word += addition

        return word
        
    def part_tag(self):

        pos = self.get_type()

        if pos == "noun":
            abbrev = "n"
        elif pos == "adj":
            abbrev = "adj"
        elif pos == "verb":
            abbrev = "v"
        elif pos == "prep":
            abbrev = "prep"
        else:
            abbrev = "???"

        return "(" + abbrev + ")"
        
    def get_definition(self):
        word = ""
        morph = None

        prefix_stack = []

        def pop_prefix(morph, definition):

            top = prefix_stack.pop()

            return build_def(top, morph, definition)

        def build_def(morph, last_morph, definition):

            part = morph.get_definition()

            if last_morph == None:
                definition = part
            else:

                words = part.split(" ")
                for (index, word) in enumerate(words):
                    if word == "%@":
                        words[index] = definition
                    if word == "[%@]":
                        words[index] = "[" + definition + "]"
                    elif word == "%part":
                        words[index] = inflection.inflect(definition, "part")
                    elif word == "%ppart":
                        words[index] = inflection.inflect(definition, "ppart")
                    elif word == "%3sg":
                        words[index] = inflection.inflect(definition, "3sg")
                    elif word == "%sg":
                        if last_morph.has_tag("count"):
                            words[index] = inflection.inflect(definition, "sg")
                        else:
                            words[index] = inflection.inflect(definition, "mass")
                    elif word == "%pl":
                        if last_morph.has_tag("count"):
                            words[index] = inflection.inflect(definition, "pl")
                        else:
                            words[index] = inflection.inflect(definition, "mass")
                    elif word == "%!pl":
                        words[index] = inflection.inflect(definition, "pl")

                definition = " ".join(words)

            return definition

        definition = ""

        for index, morph in enumerate(self.morphs):

            addition = ""

            last_morph = morph.prev
            next_morph = morph.next

            # Stack prepositions and prefixes for proper definition ordering
            if morph.get_type() == "prep" or morph.get_type() == "prefix" or morph.get_type() == "number":
                prefix_stack.append(morph)
            else:
                definition = build_def(morph, last_morph, definition)

                if index != 0:
                    if len(prefix_stack) > 0 and (morph.get_type() == "verb" or morph.get_type() == "adj" or morph.get_type() == "noun"):
                        definition = pop_prefix(morph, definition)

        while len(prefix_stack) > 0:
            definition = pop_prefix(self.morphs[self.size()-1], definition)

        # Verbs not otherwise resolved become infinitives
        if morph.get_type() == "verb":
            return inflection.inflect(definition, "inf")
        else:
            return definition
    
    def entry(self):
        
        composed = self.compose()
        tag = self.part_tag()
        definition = self.get_definition()
        entry = composed + " " + tag + "\n" + definition
        return entry
    
# Word post-processing

def check_req(morph, last_morph):
    
    if "requires" in morph:
        
        if "follows" in morph["requires"]:
            
            if not last_morph:
                return False
            
            if "tags" in morph["requires"]["follows"]:
                
                for tag in morph["requires"]["follows"]["tags"]:
                    
                    if not last_morph.has_tag(tag):
                        return False
    
    return True
