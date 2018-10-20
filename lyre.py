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

# Helpers

def is_vowel(letter):
    return letter in ["a", "i", "e", "o", "u"]

def is_consonant(letter):
    return not is_vowel(letter)
    
# Assembling morphs

def next_morph(current, final):
    global morphs, type_morphs, morphs_from
    
    head_type = word_type(current)
    
    options = morphs_from[head_type]
    
    choice = options[ random.randint(0, len(options)-1) ]
    
    return choice
    
def generate_morphs(seed, length):
    
    chosen = [seed]
    
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
    
    english_word = word
    
    # Replaces Q + U + cons. with C + U + cons. (e.g. interlocutor)
    for i in range(0, len(english_word)-1):
        if english_word[i] == "q" and english_word[i+1] == "u" and is_consonant(english_word[i+2]):
            english_word[i] = "c"
    
    # Replace final ui with uy (e.g. soliloquy)
    if english_word[-2:-1] == "ui":
        english_word[-2:] = "uy"
        
    return english_word

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

        if len(addition) > 0:

            # Combine repeated letters            
            if len(word) > 0 and addition[0] == word[-1]:
                addition = addition[1:]
            
            # Stem change
            if "stem-change" in morphs[morph] and morphs[morph]["stem-change"] == True:
                if word[-1] == "i" or word[-1] == "e":
                    addition = "e" + addition
            
            word += addition
            
    
    word = anglicize(word)
    
    return word
        
setup()

parts = generate_morphs("caput", 3)
word = compose_word(parts)
print(word)

print(anglicize("soliloqui"))
print(anglicize("eloqution"))

#word = compose_word(["caput", "al"])
