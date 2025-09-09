import src.language.old_english.orthography as orthography
import src.utils.helpers as helpers

from src.evolutor.engine.hinges import occ, rarely

# Unhandled cases:
# - Weak verbs with infinitive in'-ēaġan', pp. in '-ēad', or '-ēoġan' / '-ēod' (not relevant to MnE)
# - Cases where 'g' or 'ġ' change their palatalization (I don't know this to be reflected in MnE)
# - 'ċġ' digraph appears to become 'ġ' in participles of words like 'seċġan', 'leċġan'. I can
#   get away without a rule for it because I do a similar change in phonetic processing, but
#   it may be necessary to process this here at some point. Note that this change happens even
#   for weak verbs.

# TODOs:
# - Cases where a verb uses a different verb class' participle-formation method
# - Cases where past participles are formed from preterite forms

# Strong participles ==============================================

# Mapping from strong verb class to pairs of infinitive and past participle vowels.
# For predicting past participle forms based on the form of the infinitive.
vowel_map = {
    1: { "ī": "i" },
    2: { "ēo": "o", "ū": "o" },
    3: { "e": "o", "eo": "o", "i": "u", "ie": "o", "y": "u" }, # 'y' -> 'u' as in 'byrnan' -> 'ġeburnen'
    4: { "e": "o", "i": "u", "ie": "o", "u": "u" },
    5: { "e": "e", "i": "e", "ie": "ie"}, # 'ġiefan' -> 'ġefen' (acc. Wiktionary)?
    6: { "a": "a", "e": "a", "ē": "aġ", "ea": "a", "ie": "a"} # 'a', 'ie' can also go to 'æ". 'ē' -> 'aġ' as in 'slēan', 'flēan'. TODO: Figure out cases like 'swerian' -> 'sworen' that have 'e' -> 'o'
}

verner_map = {
    "h": "ġ",
    "s": "r",
    "þ": "d"
}

# Get a pseudo-past-participle form for the given form, treating it as the given verb class
#
# NOTE: this does *not* necessarily produce historical Old English participles. Rather, it produces
# an alternative form that should convert properly into a modern-style participle. For example, it
# doesn't make changes in 'c' palatalization when surrounding vowels change
#
# NOTE: The following cases are *not* handled by this function:
# - Weak verbs with participle forms in -'ht' (forming modern 'taught', 'sought', etc.)
#   As far as I can tell, these aren't predictable from the perspective of recorded OE.
#   TODO: Make a hinge for these if possible.
def get_strong_pseudoparticiple(form, verb_class, config):
    if verb_class == "preterite-present":
        return None

    # If this is a contracted form, call the separate function for that
    if is_contracted(form):
        return get_strong_pseudoparticiple_contracted(form, verb_class)

    # Remove inflectional ending, if any
    form = form.split("|")[0]
    if form[-1] == "i":
        form = form[:-1]

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
                elif clusters[i][0:2] == "ċġ":
                    clusters[i] = "ġ"

    form = "".join(clusters[0:vowels_index]) + vowel_map[verb_class][vowels] + "".join(clusters[vowels_index+1:])

    if rarely("PPart:verners-law", config):
        form = apply_verner(form)

    return form + suffix

def is_contracted(form):
    return form[-2:] in ["on", "ōn"] or form[-4:] == "ē|an"

# Get a pseudoparticiple for a verb in a contracted form (e.g. 'lēon', 'þēon')
def get_strong_pseudoparticiple_contracted(form, verb_class):
    if verb_class == "weak":
        return form[0:-2]

    if form[-4:] in ["ē|on", "ē|an"]:
        stem = form[0:-4]
    elif form[-2:] in ["on", "ōn"]:
        stem = form[0:-3]

    # Contracted forms in '-ēon' formerly ended in -'han'. The 'h' was later elided, but
    # changed to 'g' in the past participle under Verner's Law.
    if verb_class in [1, 5]:
        # TODO: Handle cases where class 1 verbs are given class 2-style endings, as in 'tēon' -> 'togen'
        return stem + "iġ+en"
    elif verb_class == 2:
        return stem + "og+en"
    elif verb_class == 6:
        # Class 6 strong verbs in '-ēan' show various participle forms: '-agen', '-æġen', '-eġen'.
        # Of these, '-agen' seems to be the most regular for its class, but I believe '-eġen' best
        # represents reflexes in modern English.
        return stem + "eġ+en"
    elif verb_class == 7:
        # Also appeared as '-ongen' in OE
        # HACK: '-æng' spelling is constructed, with intent of consistently giving '-ang' forms in MnE.
        # TODO: Find a more elegant way to do this.
        return stem + "æng+en"
    else:
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
