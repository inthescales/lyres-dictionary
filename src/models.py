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
           form = self.morph["final"]
        
        return form
    
    def get_gloss(self):

        # Special case for prep-relative-to-noun cases (e.g. sub-limin-al)
        if self.prev and ((self.prev.get_type() == "noun" and self.prev.prev and self.prev.prev.get_type() == "prep" ) or (self.get_type() == "verb" and self.prev.get_type() == "prep")) and "gloss-relative" in self.morph:
            return self.morph["gloss-relative"]
        
        if "gloss" in self.morph:
            if self.morph["type"] in ["noun", "verb"] and len(self.morph["gloss"].split(" ")) == 1:
                return "[" + self.morph["gloss"] + "]"
            else:
                return self.morph["gloss"]
        else:
            
            if self.next:
                if "gloss-link" in self.morph:
                    return self.morph["gloss-link"]
            else:
                if "gloss-final" in self.morph:
                    return self.morph["gloss-final"]
            

            if self.get_type() == "prep" or self.get_type() == "prefix":
                relative = self.next
            else:
                relative = self.prev

            if relative and "gloss-" + relative.get_type() in self.morph:
                return self.morph["gloss-" + relative.get_type()]
        
        print("ERROR - failed to find gloss for " + self.morph["key"])
        
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
        
    def get_type(self):
        return self.last_morph().get_type()

    def get_origin(self):
        return self.last_morph().morph["origin"]
    
    # Modifying --------------------------------
    
    def set_keys(self, keys):
        
        self.morphs = []
        
        for key in keys:
            self.morphs.append( Morph(key, self.morphary) )
            
        for i in range(0, len(self.morphs)-1):
            self.morphs[i].join(self.morphs[i+1])

    def add_prefix(self, morph):
        morph.join(self.first_morph())
        self.morphs = [morph] + self.morphs
            
    def add_suffix(self, morph):
        self.last_morph().join(morph)
        self.morphs = self.morphs + [morph]
        
    def add_affixes(self, prefix, suffix):
        self.add_prefix(prefix)
        self.add_suffix(suffix)
    
    # Composing entries ---------------------------
        
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

            part = morph.get_gloss()
            
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

# Morph Helpers ===============================

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