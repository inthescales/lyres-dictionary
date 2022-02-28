import random

from logging import Logger

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

    Logger.error("BAG ERROR")
    return nil

# Morphs have their own way of doing this, but this is for raw data
def has_tag(morph, tag):
    if not "tags" in morph:
        return False

    return tag in morph["tags"]

# Language

def is_vowel(letter, y_is_vowel=False):
    if not y_is_vowel:
        return letter in ["a", "i", "e", "o", "u"]
    else:
        return letter in ["a", "i", "e", "o", "u", "y"]

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

def syllable_count(word):
    count = 0
    in_vowels = False
    prev = None
    for char in word:
        if is_vowel(char) and (prev is None or not is_vowel(prev)) and not in_vowels:
            in_vowels = True
            count += 1
        elif is_consonant(char):
            in_vowels = False
        prev = char
    return count

def indefinite_article_for(word):
    if is_vowel(word[0]):
        return "an"
    else:
        return "a"
