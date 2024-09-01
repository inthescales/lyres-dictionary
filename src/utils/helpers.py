import random

from src.utils.logging import Logger

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

def is_consonant(letter, y_is_consonant=True):
    return not is_vowel(letter, not y_is_consonant)

def y_is_vowel_heuristic(prev_char):
    return prev_char != None and is_consonant(prev_char, True)

# Returns the estimated number of syllables in the word, based on vowel/consonant clusters
# Does not handle silent 'e', always evaluates 'y' one-way, based on parameter
# TODO: Delete this when it's no longer needed OR rename 'vowel_cluster_count' or something
def syllable_count(word, y_is_vowel=False):
    count = 0
    in_vowels = False
    prev = None
    for char in word:
        if is_vowel(char, y_is_vowel) and (prev is None or not is_vowel(prev, y_is_vowel)) and not in_vowels:
            in_vowels = True
            count += 1
        elif is_consonant(char, not y_is_vowel):
            in_vowels = False
        prev = char
    return count

# Returns an estimated syllable count for the word
# Based primarly on the number of vowel clusters, with the following additional behavior:
# - 'y' is treated as a consonant if it touches a vowel, otherwise it's counted as a vowel
# - A final 'e' preceded by a consonant (including 'y') is assumed to be silent and not counted
# NOTE: Consider adding config parameters, such as for counting final 'e' in words like 'simile'
# TODO: Delete the other syllable count function if this one is able to supersede it
def syllable_count_smart(word):
    count = 0
    in_vowels = False
    prev = None
    for (i, char) in enumerate(word):
        # 'y' counts as a vowel if it's not touching another vowel
        is_vowel_adjacent = (i > 0 and is_vowel(word[i-1], False)) or (i < len(word) - 1 and is_vowel(word[i+1], False))

        # A final 'e' preceded by a consonant is presumed to be silent
        is_silent_e = (char == "e" and i == len(word) - 1 and i > 0 and is_consonant(word[i-1], False))

        if (
            is_vowel(char) \
            or (char == "y" and not is_vowel_adjacent)  \
        ) \
            and not is_silent_e \
            and not in_vowels:
            in_vowels = True
            count += 1
        elif is_consonant(char, False):
            in_vowels = False
        prev = char
    return count

# Returns the letters in the given word, split into consonant/vowel clusters, as
# an array of strings
def split_clusters(word, is_vowel=lambda char: is_vowel(char)):
    polarity = None
    result = []
    for i in range(0, len(word)):
        new_polarity = is_vowel(word[i])
        if new_polarity != polarity:
            result += [""]
            polarity = new_polarity

        result[-1] += word[i]

    return result

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
    word = word.replace("[", "").replace("]", "")
    if is_vowel(word[0]):
        return "an"
    else:
        return "a"
