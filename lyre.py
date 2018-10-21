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

def next_morph(current, final):
    global morphs, type_morphs, morphs_from
    
    head_type = word_type(current)
    
    options = morphs_from[head_type]
    
    choice = None
    
    while choice == None or choice == current[-1]:
        choice = options[ random.randint(0, len(options)-1) ]
    
    return choice
    
def generate_morphs(length, seed=[]):
    
    if seed != []:
        chosen = seed
    else:
        chosen = [get_root_morph()["base"]]
    
    for i in range(0, length-1):
        newest = next_morph(chosen, 0)
        chosen.append(newest)
        
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
    
    for index, token in enumerate(in_morphs):
        
        addition = ""
        morph = morphs[token]
        if index < len(in_morphs) - 1:
            next_morph = morphs[in_morphs[index+1]]
        else:
            next_morph = None
        
        # Get form of morph
        if index != len(in_morphs) - 1:
            
            if "link" in morph:
                addition = morph["link"]
            elif morph["type"] == "verb" or (morph["type"] == "derive" and morph["to"] == "verb"):
                if next_morph and next_morph["participle-type"]:
                    if next_morph["participle-type"] == "present":
                        addition = morph["link-present"]
                    elif next_morph["participle-type"] == "perfect":
                        addition = morph["link-perfect"]
        else:
            addition = morphs[in_morphs[-1]]["base"]

        if len(addition) > 0:

            # Combine repeated letters            
            if len(word) > 0 and addition[0] == word[-1]:
                addition = addition[1:]
            
            # Stem change
            #if "stem-change" in morph and morph["stem-change"] == True:
            #    if word[-1] == "i" or word[-1] == "e":
            #        addition = "e" + addition
            
            word += addition
            
        if index == 0:
            definition = morph["definition"]
        else:
            definition = morph["definition"].replace("%@", definition)
    
    word = anglicize(word)
    
    return (word, definition)
        
setup()

print("")

for i in range(0, 8):
    parts = generate_morphs(random.randint(2,3))
    (word, definition) = compose_word(parts)
    print(word)
    print(definition)
    print("")

