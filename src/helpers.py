import random

# Bag probability

def choose_bag(bag):

    total = 0

    for item in bag:
        total += item[1]

    pull = random.randint(0, total-1)
    count = 0

    for item in bag:
        if pull < item[1] + count:
            return item[0]
        else:
            count += item[1]

    print("BAG ERROR")
    return nil

# Morphs have their own way of doing this, but this is for raw data
def has_tag(morph, tag):
    if not "tags" in morph:
        return False

    return tag in morph["tags"]

# Language

def is_vowel(letter):
    return letter in ["a", "i", "e", "o", "u"]

def is_consonant(letter):
    return not is_vowel(letter)

def l_in_last_two(word):
    state = 0
    prev = None
    for char in word[::-1]:
        if char == "l":
            return True
        elif char == "r":
            return False
        if prev != None and is_vowel(char) != is_vowel(prev):
            state += 1
        if state == 3:
            return False
        prev = char
    return False
        

def indefinite_article_for(word):
    if is_vowel(word[0]):
        return "an"
    else:
        return "a"
