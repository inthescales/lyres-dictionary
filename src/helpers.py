def is_vowel(letter):
    return letter in ["a", "i", "e", "o", "u"]

def is_consonant(letter):
    return not is_vowel(letter)

def indefinite_article_for(word):
    if is_vowel(word[0]):
        return "an"
    else:
        return "a"
