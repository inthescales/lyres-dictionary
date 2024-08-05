import src.evolutor.language.oe_orthography as orthography
import src.evolutor.language.mne_affixation as mne_affixation
import src.utils.helpers as helpers

from src.evolutor.engine.hinges import often, even, occ

# Strong participles ==============================================

# Mapping from strong verb class to pairs of infinitive and past participle vowels.
# For predicting past participle forms based on the form of the infinitive.
vowel_map = {
    1: { "ī": "i" },
    2: { "ēo": "o", "ū": "o" },
    3: { "e": "o", "eo": "o", "i": "u", "ie": "o" },
    4: { "e": "o", "i": "u", "u": "u" },
    5: { "e": "e", "i": "e", "ie": "e"},
    6: { "a": "a", "e": "a", "ē": "aġ", "ea": "a", "ie": "a"} # 'a', 'ie' can also go to 'æ". 'ē' -> 'aġ' as in 'slēan', 'flēan'. TODO: Figure out cases like 'swerian' -> 'sworen' that have 'e' -> 'o'
}

# Get a pseudo-past-participle form for the given form, treating it as the given verb class
#
# NOTE: this does *not* produce historical Old English participles. Rather, it produces
# an alternative form that should convert properly into a modern-style participle.
#
# Specifically, it does not produce changes in consonants due to Verner's law, as in cases like
# 'frēosan' (freeze) -> 'fruron', or 'ċēosan' choose -> 'curon', as PDE does not include
# these sound changes, using the forms 'frozen' and 'chosen'
#
# That said, Verner's law does apply in cases like 'forlese' -> 'forlorn', or 'sodden' (from 'sēoþan'),
# so I should probably add handling from it at some point. There are also some cases of literary use,
# e.g. 'frore' in Milton
# TODO: Support Verner's law sound changes in past participles.
def get_strong_pseudoparticiple(form, verb_class, config):
    # If this is a contract form, call the separate function for that
    if form[-2:] in ["on", "ōn"]:
        return get_strong_pseudoparticiple_contracted(form, verb_class)

    # Remove inflectional ending, if any
    form = form.split("|")[0]

    # Determine whether the '-en' suffix should be added
    if (verb_class == 3 and not occ("PPart:use-class-3-suffix", config)):
        suffix = ""
    else:
        suffix = "+en"

    # Class 7 verbs don't involve vowel changes
    if verb_class == 7:
        return form + suffix

    if not verb_class in vowel_map:
        return None

    clusters = helpers.split_clusters(form, lambda char: char in orthography.vowels)
    vowels_index = next(i for i in range(0, len(clusters)) if clusters[i][0] in orthography.vowels)
    vowels = clusters[vowels_index]

    return "".join(clusters[0:vowels_index]) + vowel_map[verb_class][vowels] + "".join(clusters[vowels_index+1:]) + suffix

# Get a pseudoparticiple for a verb in a contracted form (e.g. 'lēon', 'þēon')
def get_strong_pseudoparticiple_contracted(form, verb_class):
    if verb_class == "weak":
        return form[0:-2]
    else:
        if form[-4:] == "ē|on":
            stem = form[0:-4]
        elif form[-2:] == "ōn":
            stem = form[0:-3]

        if verb_class == 1:
            # TODO: Handle cases where class 1 verbs are given class 2-style endings, as in 'tēon' -> 'togen'
            return stem + "iġ+en"
        elif verb_class == 2:
            return stem + "og+en"
        elif verb_class == 7:
            # Also appeared as '-ongen' in OE
            # HACK: '-æng' spelling is constructed, with intent of consistently giving '-ang' forms in MnE.
            # TODO: Find a more elegant way to do this.
            return stem + "æng+en"
        else:
            return None

# Make spelling adjustments in the MnE form of a participle based on PDE spelling conventions.
def get_strong_spelling_adjusted(form, config):
    if form.endswith("ren") and len(form) >= 4 and form[-4] in ["a", "e", "i", "o", "u", "y"]:
        # Handle cases like 'boren' -> 'born', 'forloren' -> 'forlorn'
        return form[0:-2] + "n"

    # TODO: Add contracted participle forms.
    # See participle tests file for examples.
    # if form.endswith("ed") and often("PPart:contract-weak", config):

    return form

# Weak participles ==============================================

# Returns a weak participle for the given form
def get_weak_participle_form(form):
    if not form.endswith("e"):
        return mne_affixation.get_joined_form(form, "ed")
    else:
        return form + "d"
