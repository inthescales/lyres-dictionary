import src.evolutor.language.oe_orthography as orthography
import src.utils.helpers as helpers

# Returns any prefix matching the given written form
def get_prefix(form):
    prefixes = {
        "a": "a",
        "ā": "a",
        "biġ": "by",
        "bī": "by",
        "be": "be",
        "ġe": "", # TODO: Allow this to be rendered as /a/, /e/, or /i/ in some cases (as in 'afford', 'enough', 'handiwork')
        "on": "a" # TODO: Maybe add a probability to this
    }

    if form in prefixes:
        return prefixes[form]

def get_derivational(form_tail):
    suffixes = {
        "ard": "ard",
        "els": "els",
        "else": "els",
        "elsi": "els",
        "en": "en",
        "iġ": "iġ",
        "t": "þ",
        "þ": "þ"
    }

    raw_value = "".join(form_tail).split("+")[0].split("|")[0]
    if raw_value in suffixes:
        return suffixes[raw_value]

# Get a pseudo-past-participle form for the given form, treating it as the given verb class
#
# NOTE: this does *not* produce historical Old English participles. Rather, it produces
# an alternative form that should convert properly into a modern-style participle.
#
# Specifically, it does not produce changes in consonants in cases such as
# 'sniþan' -> '(ġe)sniden'. Rather, it would would produce 'sniþen', since that type
# of consonant change is not present in modern English, where the observed participle
# of this word is 'snithen'
def get_pseudoparticiple(form, verb_class):
    # Remove inflectional ending, if any}
    form = form.split("|")[0]

    if verb_class == "weak":
        # TODO: handle class 3 weak verbs (2 is close enough)
        return form
    elif verb_class == 7:
        return form + "+en"

    vowel_map = {
        1: { "ī": "i" },
        2: { "ēo": "o", "ū": "o" },
        3: { "e": "o", "eo": "o", "i": "u", "ie": "o" },
        4: { "e": "o", "i": "u", "u": "u" },
        5: { "e": "e", "i": "e", "ie": "e"},
        6: { "a": "a", "e": "a", "ea": "a", "ie": "a"}, # 'ie' as in 'hliehhan'. 'a', 'ie' can also go to 'æ".
        7: {}
    }

    if not verb_class in vowel_map:
        print("VERB CLASS NOT IN VOWEL MAP! HAVE: " + str(verb_class))

    cluster_indices = []
    for i in range(0, len(form)):
        if form[i] in orthography.vowels:
            cluster_indices = [i]
            for j in range(i, len(form)):
                if form[j] not in orthography.vowels:
                    cluster_indices += [j]
                    break

            if len(cluster_indices) == 2:
                break
            elif len(cluster_indices) == 1:
                cluster_indices += [len(form)]

    if not len(cluster_indices) == 2:
        print("DIDN'T GET PROPER INDICES! HAVE: " + str(cluster_indices))

    vowels = form[cluster_indices[0]: cluster_indices[1]]
    if vowels not in vowel_map[verb_class]:
        print("VOWELS NOT FOUND IN VOWEL MAP! Have " + str(vowels) + " FOR CLASS " + str(verb_class))

    return form[0:cluster_indices[0]] + vowel_map[verb_class][vowels] + form[cluster_indices[1]:] + "+en"
