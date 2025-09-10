import src.language.old_english.orthography as orthography
import src.utils.helpers as helpers

from src.evolutor.engine.hinges import often, rarely

# Unhandled cases:
# - 

# TODOs:
# - Cases where a verb uses a different verb class' preterite-formation method

# TODO: Consider doing preterites and participles by directly manipulating modern forms

# Strong past forms ==============================================

# Mapping from strong verb class to pairs of infinitive and past participle vowels.
# For predicting past participle forms based on the form of the infinitive.
vowel_map = {
    1: { "ī": "ā" },
    3: {},
    # 4: { "e": "o", "i": "u", "ie": "o", "u": "u" },
    # 5: { "e": "e", "i": "e", "ie": "ie"}, # 'ġiefan' -> 'ġefen' (acc. Wiktionary)?
    # 6: { "a": "a", "e": "a", "ē": "aġ", "ea": "a", "ie": "a"} # 'a', 'ie' can also go to 'æ". 'ē' -> 'aġ' as in 'slēan', 'flēan'. TODO: Figure out cases like 'swerian' -> 'sworen' that have 'e' -> 'o'
}

verner_map = {
    "h": "ġ",
    "s": "r",
    "þ": "d"
}

# Get a pseudo-preterite form for the given form, treating it as the given verb class
#
# NOTE: this does *not* necessarily produce historical Old English preterites. Rather, it produces
# an alternative form that should convert properly into a modern-style past tense form.
#
# NOTE: The following cases are *not* handled by this function:
# - Weak verbs with participle forms in -'ht' (forming modern 'taught', 'sought', etc.)
#   As far as I can tell, these aren't predictable from the perspective of recorded OE.
#   TODO: Make a hinge for these if possible.
def get_strong_pseudopreterite(form, verb_class, config):
    if verb_class == "preterite-present":
        return None

    # If this is a contracted form, call the separate function for that
    if is_contracted(form):
        return get_strong_pseudopreterite_contracted(form, verb_class)

    # Remove inflectional ending, if any
    form = form.split("|")[0]
    if form[-1] == "i":
        form = form[:-1]

    # Get clusters
    clusters = helpers.split_clusters(form, lambda char: char in orthography.vowels)
    vowels_index = next(i for i in range(0, len(clusters)) if clusters[i][0] in orthography.vowels)
    vowels = clusters[vowels_index]

    lengthen = True

    if verb_class == 1:
        if form[-1] in ["s", "f", "þ"]:
            # Stems with final fricatives always take the long 'a'
            vowel = "ā"
        else:
            # Hinge covers cases like 'ride' -> 'rode' vs 'bite' -> 'bit'
            vowel = often("Pret:class-1-vowel", config)
            if vowel == "i":
                lengthen = False

    # Class 2:
    if verb_class == 2:
        if form[-3:] == "ēog":
            # As class 7, e.g. 'flēogan' -> 'fly' -> 'flew'
            vowel = "e"
        else:
            # As class 4
            vowel = "o"

    # Class 3:
    # TODO: Consider 'n' followed by two other consonants
    if verb_class == 3:
        if form[-2:] == "nd":
            # As in 'grind' -> 'ground'
            vowel = "u"
            lengthen = False
        elif clusters[-1][0] in ["m", "n"]:
            # Hinge covers 'swim' -> 'swam' vs 'stink' -> 'stunk' (latter assimilated from past participle)
            vowel = often("Pret:class-3a-vowel", config)
            if vowel == "a":
                lengthen = False
        else:
            # 'fought' is an exception here, but other class 3 words are almost all weak now
            return None

    if verb_class == 4:
        vowel = "o"

    if verb_class == 5:
        vowel = "a"

    if verb_class == 6:
        if form[-2:] in ["ag", "aġ"] or form[-1] == "ē":
            vowel = "e"
        elif vowels in ["a", "ā"]:
            vowel = "ō"
        elif vowels == "e":
            vowel = "o"
        else:
            # Class 6 strong verbs in MnE are few and various. If it doesn't match a known
            # case, just use a weak form.
            return None

    if verb_class == 7:
        if form[-2:] in ["āw", "ōw"]:
            # 'cnāwan' -> 'know' -> 'knew', 'grōwan' -> 'grow' -> 'grew'
            vowel = "e"
        else:
            # There are a few assorted other cases of class 7 strong verbs in MnE
            # TODO: Add analogical forms here
            return None

    # Geminates in some classes should be reduced, e.g. 'biddan' -> 'beden' (5), 'sċeappen' -> 'sċapen' (6)
    # (These words have infinitives that show gemination due to being formed with '-jan')
    # However, this should not apply to cases such as 'swellan' -> 'swollen' (3)
    if verb_class in [5, 6]:
        for i in range(0, len(clusters)):
            if len(clusters[i]) == 2:
                if clusters[i][0] == clusters[i][1] and clusters[i][0] in orthography.consonants:
                    clusters[i] = clusters[i][0]
                elif clusters[i][0:2] == "ċġ":
                    clusters[i] = "ġ"

    if lengthen and not helpers.is_vowel(clusters[-1][0], y_is_vowel=True):
        # Add a final vowel to ensure that fricatives become voiced when appropriate. Otherwise
        # we end up with mistakes like 'drīfan' -> *'drofe' (instead of 'drove')
        clusters += ["e"]

    form = "".join(clusters[0:vowels_index]) + vowel + "".join(clusters[vowels_index+1:])

    if rarely("PPart:verners-law", config):
        form = apply_verner(form)

    return form

def is_contracted(form):
    return form[-2:] in ["on", "ōn"] or form[-4:] == "ē|an"

# Get a pseudoparticiple for a verb in a contracted form (e.g. 'lēon', 'þēon')
def get_strong_pseudopreterite_contracted(form, verb_class):
    if verb_class == "weak":
        return form[0:-2]
    elif form[-4:] == "ē|on":
        # No strong preterites for e.g. 'tēon' -> 'tee' -> 'teed'
        return None

    if form[-4:] == "ē|an":
        # As in 'slē|an' -> 'slay' -> 'slew'
        return form[0:-4] + "ege"
    elif form[-3:] in ["|on", "|ōn"]:
        # As in 'h|ōn' -> 'hang' -> 'hung'
        return form[0:-3] + "ung"

    return None

# Verner's Law ==================================================

# Apply Verner's Law, as it appears in participles, to the given participle form.
# Ex. 'frosen' -> 'froren'
# Here I just replace the last, single consonant according to Verner's Law.
# Ignoring any cases with multiple consonants in the final cluster because I'm
# not sure whether Verner's Law should apply there - I'm not aware of any MnE cases.
# Equality check handles cases like 'hliehhan' -> 'hlæġen'
def apply_verner(form):
    if form[-1] not in orthography.consonants \
        or (form[-2] in orthography.consonants and form[-2] != form[-1]) \
        or form[-1] not in verner_map:
        return form

    if form[-2] != form[-1]:
        stem = form[:-1]
    else:
        stem = form[:-2]

    return stem + verner_map[form[-1]]
