import json
import random

from pattern.en import conjugate, singularize, pluralize, tag

morphs = {}
roots = []
type_morphs = {}
morphs_from = {}
words = []

# Data import and setup

def setup():
    global morphs, roots, type_morphs, morphs_from, words
    
    (morphs, roots, type_morphs, morphs_from) = load_morphs()
    
def load_morphs():
    
    with open('morphs.json') as morph_data:
        raw_morphs = json.load(morph_data)
        morphs = {}
        roots = []
        type_morphs = {}
        morphs_from = {}
        
        for morph in raw_morphs:
            
            if not validate_morph(morph):
                print("ERROR - invalid morph")
                print(morph)
                exit(0)
            
            morphs[morph["key"]] = morph
            
            if "type" in morph:
                morph_type = morph["type"]
                if not morph_type in type_morphs:
                    type_morphs[morph_type] = []
                    
                type_morphs[morph_type].append(morph["key"])
                
                if morph_type in ["noun", "adj", "verb"]:
                    roots.append(morph)
                
            if "from" in morph:
                
                for from_type in morph["from"].split(","):
                    if not from_type in morphs_from:
                        morphs_from[from_type] = []

                    morphs_from[from_type].append(morph["key"])
            
        return (morphs, roots, type_morphs, morphs_from)

def validate_morph(morph):
    
    if morph["type"] == "verb":
        if not ("link-present" in morph and "link-perfect" in morph and "final" in morph):
            return False
    
    return True
    
# Helpers

def is_vowel(letter):
    return letter in ["a", "i", "e", "o", "u"]

def is_consonant(letter):
    return not is_vowel(letter)

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

def has_tag(morph, target):
    
    if "tags" in morph:
        if target in morph["tags"]:
            return True
        
    return False

def check_req(morph, last_morph):
    
    if "requires" in morph:
        
        if "follows" in morph["requires"]:
            
            if not last_morph:
                return False
            
            if "tags" in morph["requires"]["follows"]:
                
                if not "tags" in last_morph:
                    return False
                
                for tag in morph["requires"]["follows"]["tags"]:
                    
                    if not has_tag(last_morph, tag):
                        return False
    
    return True
     
# Assembling morphs

def get_root_morph():
    
    part = random.choice(["noun", "adj", "verb", "verb", "verb"])
    return morphs[random.choice(type_morphs[part])]

def next_morph(current):
    global morphs, type_morphs, morphs_from
    
    head_type = word_type(current)

    if len(current) > 0:
        last_morph = morphs[current[-1]]
        first_morph = morphs[current[0]]
    else:
        last_morph = None
        first_morph = None
        
    choice = None
    
    while choice == None or choice == current[-1]:

        # Special chance to add prefixes before verbs.
        # Necessary to inflate their frequency given their small number.
        if len(current) == 1 and head_type == "verb" and not has_tag(last_morph, "no-prep") and not first_morph["type"] in ["prep", "prefix"] and random.randint(0, 3) == 0:
            choice = random.choice(type_morphs["prep"])
            return [choice] + current
        
        # Special chance to use the preposition + noun + ate pattern    
        if len(current) == 1 and head_type == "noun" and not has_tag(last_morph, "no-prep") and random.randint(0, 4) == 0:
            #options = type_morphs["prep"]
            prep_choice = random.choice(["in", "ex", "trans", "inter", "sub", "super"])
            end_choice = random.choice(["ate", "al", "al", "ary", "ify", "ize"])
            return [prep_choice] + current + [end_choice]
        
        # Add a prefix to the whole thing
        if len(current) >= 1 and head_type == "verb" and not first_morph["type"] in ["prep", "prefix"] and random.randint(0, 8) == 0:
            choice = random.choice(type_morphs["prefix"])
            return [choice] + current
        
        # Basic morph addition
        else:
            choice = random.choice(morphs_from[head_type])
            
            if not check_req(morphs[choice], last_morph):
                choice = None
            else:    
                return current + [choice]
    
def generate_morphs(length, seed=[]):
    
    if seed != []:
        chosen = seed
    else:        
        chosen = [get_root_morph()["key"]]
    
    for i in range(0, length-1):
        chosen = next_morph(chosen)
        
    return chosen

def word_type(word_morphs):
    global morphs
    
    last_morph = morphs[word_morphs[-1]]
    
    if last_morph["type"] == "derive":
        return last_morph["to"]
    else:
        return last_morph["type"]
    
# Finishing the word

def anglicize(word):
    
    english_word = list(word)
    
    # Replace final ui with uy (e.g. soliloquy)
    if english_word[-2:] == list("ui"):
        english_word[-2:] = list("uy")
        
    return "".join(english_word)

def compose_word(in_morphs):
    global morphs
    
    word = ""
    morph = None
    last_morph = None
    next_morph = None
    
    for index, token in enumerate(in_morphs):
        
        addition = ""
        
        last_morph = morph
        morph = morphs[token]
        
        if index < len(in_morphs) - 1:
            next_morph = morphs[in_morphs[index+1]]
        else:
            next_morph = None
                        
        # Check for exceptional forms
        excepted = False
        if "exception" in morph:
            for exception in morph["exception"]:

                # Assume there's a match, and negate that if it doesn't meet a requirement
                # Match the first case that we fill
                match = True
                case = exception["case"]

                # TODO - this doesn't make sense, since each case has its own base/link
                if "precedes" in case:
                    
                    if not next_morph:
                        match = False
                    else:
                        precede_match = False
                        for element in case["precedes"]:
                            if next_morph["key"] == element:
                                precede_match = True
                                break

                        if not precede_match:
                            match = False
                            
                if "follows" in case:
                    
                    if not last_morph:
                        match = False
                    else:
                        follow_match = False
                        for element in case["follows"]:
                            if last_morph["key"] == element:
                                follow_match = True
                                break

                        if not follow_match:
                            match = False

                if match:
                    if next_morph == None:
                        print(morph["key"]) # TEST
                        addition = exception["final"]
                    else:
                        addition = exception["link"]
                    excepted = True
                    break
            
                
        if not excepted:
            # Get the proper form of the morph
            if index != len(in_morphs) - 1:

                # Follow special assimilation rules if there are any
                if "assimilation" in morph:

                    next_letter = list(next_morph["key"])[0]

                    matched_case = None
                    star_case = None

                    for case, sounds in morph["assimilation"].items():

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
                        addition = morph["link"]
                    elif case == "link-assim":
                        addition = morph["link-assim"]
                    elif case == "cut":
                        addition = morph["link"] + "-"
                    elif case == "double":
                        addition = morph["link-assim"] + next_letter
                    elif case == "nasal":
                        if next_letter == 'm' or next_letter == 'p' or next_letter == 'b':
                            addition = morph["link-assim"] + 'm'
                        else:
                            addition = morph["link-assim"] + 'n'
                    else:
                        addition = case


                # Default rules
                else:

                    # Usually we'll use link form
                    if "link" in morph:
                        addition = morph["link"]

                    # Verbs or verbal derivations need to take participle form into account
                    elif morph["type"] == "verb" or (morph["type"] == "derive" and morph["to"] == "verb"):
                        if next_morph and "participle-type" in next_morph:
                            if next_morph["participle-type"] == "present":
                                addition = morph["link-present"]
                            elif next_morph["participle-type"] == "perfect":
                                addition = morph["link-perfect"]
                        elif "link-verb" in morph:
                            addition = morph["link-verb"]
                        else:
                            addition = morph["link-perfect"]

                    # Use base form if nothing overrides
                    else:
                        addition = morph["final"]
        
            # The final morph
            else:
                print(morph["key"]) # TEST
                addition = morph["final"]

        if len(addition) > 0:

            # e.g.: glaci + ify -> glacify
            if len(word) > 0 and addition[0] == word[-1] and is_vowel(addition[0]) and not last_morph["type"] == "prep":
                addition = addition[1:]
            
            # Stem change
            if has_tag(morph, "stem-change"):
                if word[-1] == "i":
                    addition = "e" + addition
                    
            # Stem raise
            if has_tag(morph, "stem-raise") and word[-1] == "e":
                word = word[:-1]
                addition = "i" + addition
                
            # Drop first (sub + emere -> sumere)
            if has_tag(morph, "drop-first") and last_morph:
                addition = addition[1:]
                
            elif len(word) > 0 and word[-1] == "e" and addition[0] == "i":
                word = word[:-1]
            
            if len(word) > 0 and word[-1] == "-":
                word = word[:-1]
                addition = addition[1:]
            
            word += addition
    
    # Post processing on the word
    word = anglicize(word)
    
    return word
        
def compose_definition(in_morphs):
    global morphs
    
    word = ""
    morph = None
    last_morph = None
    
    prefix_stack = []
    
    def get_definition(morph, last_morph):
        
        if "definition" in morph:
            return morph["definition"]
        elif last_morph and ("definition-" + word_type([last_morph["key"]])) in morph:
            return morph["definition-" + word_type([last_morph["key"]])]
    
    def pop_prefix(morph, definition):
        
        top = prefix_stack.pop()
        
        return build_def(top, morph, definition)
    
    def build_def(morph, last_morph, definition):
        
        part = get_definition(morph, last_morph)
        
        if last_morph == None:
            definition = part
        else:
            
            if part == None:
                print("ERROR NO DEF")
                print(morph)
                print(last_morph)
            
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
                    if has_tag(last_morph, "count"):
                        words[index] = rephrase(definition, "sg")
                    else:
                        words[index] = definition
                elif word == "%pl":
                    if has_tag(last_morph, "count"):
                        words[index] = rephrase(definition, "pl")
                    else:
                        words[index] = definition
            
            definition = " ".join(words)
        
        return definition
    
    definition = ""
    
    for index, token in enumerate(in_morphs):
        
        addition = ""
        
        last_morph = morph
        morph = morphs[token]
        if index < len(in_morphs) - 1:
            next_morph = morphs[in_morphs[index+1]]
        else:
            next_morph = None
        
        # Stack prepositions and prefixes for proper definition ordering
        if morph["type"] == "prep" or morph["type"] == "prefix":
            prefix_stack.append(morph)
        else:
            definition = build_def(morph, last_morph, definition)

            if index != 0:
                if len(prefix_stack) > 0 and (morph["type"] == "verb" or morph["type"] == "adj" or morph["type"] == "noun"):
                    definition = pop_prefix(morph, definition)
                
    while len(prefix_stack) > 0:
        definition = pop_prefix(None, definition)
    
    return definition
        
        
    
def part_tag(word_morphs):

    pos = word_type(word_morphs)
    
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

def generate_entry():
    
    if len(morphs.keys()) == 0:
        setup()
    
    word_morphs = generate_morphs(random.randint(2,3))
    return write_entry(word_morphs)

def write_entry(morphs):
    
    word = compose_word(morphs)
    definition = compose_definition(morphs)
    entry = word + " " + part_tag(morphs) + "\n" + definition
    return entry

def run(count):
    
    print("")
    for i in range(0, count):
        print(generate_entry())
        print("")
    
def test(morphs):

    print("")
    print(write_entry(morphs))

setup()

run(5000)
#test(["com", "ordinare"])

