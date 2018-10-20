import json
import random

morphs = {}
type_morphs = {}
morphs_from = {}
words = []

# Data import and setup

def setup():
    global morphs, type_morphs, morphs_from, words
    
    (morphs, type_morphs, morphs_from) = load_morphs()
    words = load_words()
    
def load_morphs():
    
    with open('morphs.json') as morph_data:
        raw_morphs = json.load(morph_data)
        morphs = {}
        type_morphs = {}
        morphs_from = {}
        
        for morph in raw_morphs:
            morphs[morph["base"]] = morph
            
            if "type" in morph:
                morph_type = morph["type"]
                if not morph_type in type_morphs:
                    type_morphs[morph_type] = []
                    
                type_morphs[morph_type].append(morph["base"])
                
            if "from" in morph:
                
                for from_type in morph["from"].split(","):
                    if not from_type in morphs_from:
                        morphs_from[from_type] = []

                    morphs_from[from_type].append(morph["base"])
            
        return (morphs, type_morphs, morphs_from)

def load_words():
    
    with open('words.json') as word_data:
        words = json.load(word_data)
        return words

# Assembling morphs

def next_morph(current, final):
    global morphs, type_morphs, morphs_from
    
    head_morph = morphs[current[-1]]
    head_type = head_morph["type"]
    
    options = morphs_from[head_type]
    
    choice = options[ random.randint(0, len(options)-1) ]
    
    return choice
    
    
# Finishing the word
    
def compose_word(in_morphs):
    global morphs
    
    word = ""
    
    for index, morph in enumerate(in_morphs):
        
        addition = ""
        
        # Get form of morph
        if index != len(in_morphs) - 1:
            addition = morphs[morph]["link"]
        else:
            addition = morphs[in_morphs[-1]]["base"]

        # Combine repeated letters
        if len(addition) > 0:
            
            if len(word) > 0 and addition[0] == word[-1]:
                addition = addition[1:]
            
            word += addition
    
    return word
        
setup()

root = "pecunia"
second = next_morph([root], 0)
word = compose_word([root, second])
print(word)
#word = compose_word(["caput", "al"])
