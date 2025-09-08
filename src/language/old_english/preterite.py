import src.language.old_english.orthography as orthography
import src.utils.helpers as helpers

from src.evolutor.engine.hinges import even, rarely

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
    # 2: { "ēo": "o", "ū": "o" },
    # 3: { "e": "o", "eo": "o", "i": "u", "ie": "o", "y": "u" }, # 'y' -> 'u' as in 'byrnan' -> 'ġeburnen'
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

    # Class 1 verbs have two forms: one with a long vowel (ride -> rode) and one with shortened
    # (bite -> bit)
    if verb_class == 1:
        if form[-1] in ["s", "f", "þ"]:
            # Stems with final fricatives always take the long 'a'
            vowel = "ā"
        else:
            vowel = even("Pret:class-1-vowel", config)
        vowel_map[1]["ī"] = vowel # TODO: Fix this hack

    if not helpers.is_vowel(form[-1], y_is_vowel=True):
        # Add a final vowel to ensure that fricatives become voiced when appropriate. Otherwise
        # we end up with mistakes like 'drīfan' -> *'drofe' (instead of 'drove')
        form += "e"

    # Class 7 verbs don't involve vowel changes
    if verb_class == 7:
        return form

    if not verb_class in vowel_map:
        return None

    clusters = helpers.split_clusters(form, lambda char: char in orthography.vowels)
    vowels_index = next(i for i in range(0, len(clusters)) if clusters[i][0] in orthography.vowels)
    vowels = clusters[vowels_index]

    if vowels not in vowel_map[verb_class]:
        return form

    # Geminates in some classes should be reduced, e.g. 'biddan' -> 'beden' (5), 'sċeappen' -> 'sċapen' (6)
    # (These words have infinitives that show gemination due to being formed with '-jan')
    # However, this should not apply to cases such as 'swellan' -> 'swollen' (3)
    if verb_class in [5, 6]:
        for i in range(0, len(clusters)):
            if len(clusters[i]) == 2:
                if clusters[i][0] == clusters[i][1] and clusters[i][0] in orthography.consonants:
                    clusters[i] = clusters[i][0]
                elif clusters[i][0:1] == "ċġ":
                    clusters[i] = "ġ"

    form = "".join(clusters[0:vowels_index]) + vowel_map[verb_class][vowels] + "".join(clusters[vowels_index+1:])

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
        return None

    if form[-4:] == "ē|an":
        stem = form[0:-4]
    elif form[-2:] in ["on", "ōn"]:
        stem = form[0:-3]

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
