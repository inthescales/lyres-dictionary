import json
import random

morphs = {}
roots = []
type_morphs = {}
morphs_from = {}
words = []

# Data import and setup

def setup():
    global morphs, roots, type_morphs, morphs_from, words
    
    (morphs, roots, type_morphs, morphs_from) = load_morphs()
    words = load_words()
    
def load_morphs():
    
    with open('morphs.json') as morph_data:
        raw_morphs = json.load(morph_data)
        morphs = {}
        roots = []
        type_morphs = {}
        morphs_from = {}
        
        for morph in raw_morphs:
            morphs[morph["base"]] = morph
            
            if "type" in morph:
                morph_type = morph["type"]
                if not morph_type in type_morphs:
                    type_morphs[morph_type] = []
                    
                type_morphs[morph_type].append(morph["base"])
                
                if morph_type in ["noun", "adj", "verb"]:
                    roots.append(morph)
                
            if "from" in morph:
                
                for from_type in morph["from"].split(","):
                    if not from_type in morphs_from:
                        morphs_from[from_type] = []

                    morphs_from[from_type].append(morph["base"])
            
        return (morphs, roots, type_morphs, morphs_from)

def load_words():
    
    with open('words.json') as word_data:
        words = json.load(word_data)
        return words

# Helpers

def is_vowel(letter):
    return letter in ["a", "i", "e", "o", "u"]

def is_consonant(letter):
    return not is_vowel(letter)
    
# Assembling morphs

def get_root_morph():
    
    return roots[random.randint(0, len(roots)-1)]

def next_morph(current):
    global morphs, type_morphs, morphs_from
    
    head_type = word_type(current)
    
    choice = None
    
    while choice == None or choice == current[-1]:

        # Special chance to add prefixes before verbs.
        # Necessary to inflate their frequency given their small number.
        if word_type(current) == "verb" and not morphs[current[0]]["type"] == "prep" and random.randint(0, 4) == 0:
            options = type_morphs["prep"]
            choice = options[ random.randint(0, len(options)-1) ]
            return [choice] + current
        # Special chance to use the preposition + noun + ate pattern    
        if len(current) == 1 and head_type == "noun" and random.randint(0, 0) == 0:
            options = type_morphs["prep"]
            options = ["in", "ex", "trans"]
            choice = options[ random.randint(0, len(options)-1) ]
            return [choice] + current + ["ate"]
        else:
            # Basic morph addition
            options = morphs_from[head_type]
            choice = options[ random.randint(0, len(options)-1) ]
            return current + [choice]
    
def generate_morphs(length, seed=[]):
    
    if seed != []:
        chosen = seed
    else:
        chosen = [get_root_morph()["base"]]
        #chosen = []
        #for pos in ["adj", "verb"]:
        #    options = type_morphs[pos]
        #    choice = options[ random.randint(0, len(options)-1) ]
        #    chosen.append(choice)
    
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
    definition = ""
    
    prefix_stack = []
    
    def pop_prefix():
        nonlocal morph
        nonlocal definition
        
        top = prefix_stack.pop()
        definition += " " + top["definition"]
    
    for index, token in enumerate(in_morphs):
        
        addition = ""
        morph = morphs[token]
        if index < len(in_morphs) - 1:
            next_morph = morphs[in_morphs[index+1]]
        else:
            next_morph = None
        
        # Stack prepositions and prefixes for proper definition ordering
        if morph["type"] == "prep" or morph["type"] == "prefix":
            prefix_stack.append(morph)
            
        # Get the proper form of the morph
        if index != len(in_morphs) - 1:
            
            # Follow special assimilation rules if there are any
            if "assimilation" in morph:
                
                next_letter = list(next_morph["base"])[0]
                
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
                        
                if case == "base":
                    addition = morph["base"]
                elif case == "link":
                    addition = morph["link"]
                elif case == "cut":
                    addition = morph["base"] + "-"
                elif case == "double":
                    addition = morph["link"] + next_letter
                elif case == "nasal":
                    if next_letter == 'm' or next_letter == 'p' or next_letter == 'b':
                        addition = morph["link"] + 'm'
                    else:
                        addition = morph["link"] + 'n'
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
                    addition = morph["base"]
        
        # The final morph
        else:
                # Non-verbs always use base form
                if not morph["type"] == "verb":
                    addition = morph["base"]
                    
                # Verbs use either their perfect or exception form
                else:
                    if "link-verb" in morph:
                        addition = morph["link-verb"]
                    else:
                        addition = morph["link-perfect"]

        if len(addition) > 0:

            # Combine repeated letters            
            if len(word) > 0 and addition[0] == word[-1] and is_vowel(addition[0]):
                addition = addition[1:]
            
            # Stem change
            if "stem-change" in morph and morph["stem-change"] == True:
                if word[-1] == "i" or word[-1] == "e":
                    addition = "e" + addition
            
            if len(word) > 0 and word[-1] == "-":
                word = word[:-1]
                addition = addition[1:]
            
            word += addition
            
        if index == 0:
            definition = morph["definition"]
        else:
            definition = morph["definition"].replace("%@", definition)
            if len(prefix_stack) > 0 and (morph["type"] == "verb" or morph["type"] == "adj" or morph["type"] == "noun"):
                pop_prefix()
    
    word = anglicize(word)
    
    while len(prefix_stack) > 0:
        pop_prefix()
    
    return (word, definition)
        
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

setup()

print("")

#print(compose_word(["ob", "bibere", "ion"]))

for i in range(0, 8):
    parts = generate_morphs(random.randint(2,3))
    (word, definition) = compose_word(parts)
    print(word + " " + part_tag(parts))
    print(definition)
    print("")

