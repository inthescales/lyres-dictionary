import json
import random

from pattern.en import conjugate, singularize, pluralize, tag

morphary = None

# Setup and data intake

def setup():
    global morphary
    
    morphary = Morphary(["morphs.json"])

def needs_setup():
    return morphary == None
    
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
            
# Word generation classes         

class Morph:
    
    def __init__(self, key):
        global morphary
        
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
    
    def __init__(self):
        self.morphs = []
        
    def set_keys(self, keys):
        
        self.morphs = []
        
        for key in keys:
            self.morphs.append( Morph(key) )
            
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
        global morphary
        
        type = random.choice(["noun", "adj", "verb", "verb", "verb"])
        key = random.choice(morphary.type_morphs[type])
        return Morph(key)     
        
    def next_morph(self):
        global morphary
        
        current_type = self.get_type()
        last_morph = self.last_morph()
        first_morph = self.first_morph()

        choice = None

        while True:

            # Special chance to add prefixes before verbs.
            # Necessary to inflate their frequency given their small number.
            if self.size() == 1 and current_type == "verb" and not last_morph.has_tag("no-prep") and not first_morph.get_type() in ["prep", "prefix"] and (random.randint(0, 3) == 0 or last_morph.has_tag("always-prep")):
                new_morph = Morph( random.choice(morphary.type_morphs["prep"]) )
                new_morph.join(first_morph)
                self.morphs = [new_morph] + self.morphs
                break

            # Special chance to use the preposition + noun + ate pattern    
            if self.size() == 1 and current_type == "noun" and not last_morph.has_tag("no-prep") and random.randint(0, 8) == 0:
                prep_morph = Morph( random.choice(["in", "ex", "trans", "inter", "sub", "super"]) )
                end_morph = Morph( random.choice(["ate", "al", "al", "ary", "ify", "ize"]) )
                prep_morph.join(first_morph)
                last_morph.join(end_morph)
                self.morphs =  [prep_morph] + self.morphs + [end_morph]
                break

            # Chance to use number + noun + "al" composition
            
            if self.size() == 1 and current_type == "noun" and random.randint(0,15) == 0:
                num_morph = Morph( random.choice(morphary.type_morphs["number"]) )
                end_morph = Morph( "al-number")
                num_morph.join(first_morph)
                first_morph.join(end_morph)
                self.morphs = [num_morph] + self.morphs + [end_morph]
                break
                
            # Add a prefix to the whole thing
            if self.size() >= 1 and current_type == "verb" and not first_morph.get_type() in ["prep", "prefix"] and random.randint(0, 8) == 0:
                new_morph = Morph( random.choice(morphary.type_morphs["prefix"]) )
                new_morph.join(first_morph)
                self.morphs = [new_morph] + self.morphs
                break

            # Basic morph addition
            else:
                choice = random.choice(morphary.morphs_from[current_type])

                if choice == last_morph.morph["key"] or not check_req(morphary.morph_for_key[choice], last_morph):
                    choice = None
                else:    
                    new_morph = Morph(choice)
                    last_morph.join(new_morph)
                    self.morphs.append(new_morph)
                    break
    
    def get_type(self):

        return self.last_morph().get_type()
        
    def compose(self):
        global morphary

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
                    if addition[0] == word[-1] and is_vowel(addition[0]):

                        letter = addition[0]

                        if (not last_morph.get_type() == "prep" and not last_morph.get_type() == "prefix" and not last_morph.get_type() == "number"):
                            addition = addition[1:]
                        elif letter in ["a", "i", "u"]:
                            addition = "-" + addition

                    elif word[-1] == "e" and addition[0] == "i":
                        word = word[:-1]

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

        # Post processing on the word
        word = anglicize(word)

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
        global morphary

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
                    elif word == "%part":
                        words[index] = rephrase(definition, "part")
                    elif word == "%ppart":
                        words[index] = rephrase(definition, "ppart")
                    elif word == "%3sg":
                        words[index] = rephrase(definition, "3sg")
                    elif word == "%sg":
                        if last_morph.has_tag("count"):
                            words[index] = rephrase(definition, "sg")
                        else:
                            words[index] = definition
                    elif word == "%pl":
                        if last_morph.has_tag("count"):
                            words[index] = rephrase(definition, "pl")
                        else:
                            words[index] = definition
                    elif word == "%!pl":
                        words[index] = rephrase(definition, "pl")

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

        return definition
    
    def entry(self):
        
        composed = self.compose()
        tag = self.part_tag()
        definition = self.get_definition()
        entry = composed + " " + tag + "\n" + definition
        return entry
    
# Helpers

def is_vowel(letter):
    return letter in ["a", "i", "e", "o", "u"]

def is_consonant(letter):
    return not is_vowel(letter)

# Word post-processing

def rephrase(string, mode):
    
    words = string.split(" ")    
    tags = tag(string)

    for i, curtag in enumerate(tags):
          
        if (mode in ["ppart", "part", "3sg"]) and (len(tags) == 1 or "VB" in curtag or "VBZ" in curtag or "VBG" in curtag):
            index = words.index(curtag[0])
            words[index] = conjugate(words[index], mode)

            if "VB" in curtag:
                del words[index-1]

            break
            
        elif mode == "sg" and ("NNS" in curtag or len(tags) == 1):
            index = words.index(curtag[0])
            
            if not "NN" in curtag:
                words[index] = singularize(words[index])
                
            words.insert(index, "a")
            
        elif mode == "pl" and ("NN" in curtag or (not "NNS" in curtag and len(tags) == 1)):
            index = words.index(curtag[0])
            words[index] = pluralize(words[index])
    
    return " ".join(words)

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

def anglicize(word):
    
    english_word = list(word)
    
    # Replace final ui with uy (e.g. soliloquy)
    if english_word[-2:] == list("ui"):
        english_word[-2:] = list("uy")
        
    return "".join(english_word)

# Generating operations

def run(count):
    
    print("")
    for i in range(0, count):
        print(generate_entry())
        print("")
    
def test(keys):

    if needs_setup():
        setup()
        
    word = Word()
    word.set_keys(keys)
    
    print("")
    print(word.entry())

def generate_entry():
   
    if needs_setup():
        setup()
    
    word = Word()
    word.grow_to_size(random.randint(2,3))
    return word.entry()

run(10)
#test(["vorare", "nt", "ous"])

# fix not adding "a" before multi-word nouns, ex "married woman"

# errors:
# - asspect
