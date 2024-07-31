import src.evolutor.language.oe_read as oe_read
import src.evolutor.language.oe_morphology as oe_morphology
import src.evolutor.language.oe_phonology as oe_phonology
import src.evolutor.language.me_phonology as me_phonology
import src.evolutor.language.mne_write as mne_write
import src.evolutor.language.mne_affixation as mne_affixation

def oe_orth_to_oe_phone(oe_form, config):
    return oe_phonology.from_oe_written(oe_form)

def oe_phone_to_me_phone(oe_phone, config):
    return me_phonology.from_oe_phonemes(oe_phone, config)

def me_phone_to_ne_orth(me_phone, config):
    return ne_orthography.from_me_phonemes(me_phone, config)

def oe_form_to_ne_participle(oe_form, verb_class, method, config):
    if method in [1, 2]:
        pseudoparticiple = oe_morphology.get_pseudoparticiple(oe_form, verb_class)

        if method == 2 and pseudoparticiple.endswith("+en"):
            pseudoparticiple = pseudoparticiple[:-3]

        participle_form = oe_form_to_ne_form(pseudoparticiple, config)
    else:
        participle_form = oe_form_to_ne_form(oe_form, config)

    if verb_class == "weak" or method in [3, 4]:
        if not participle_form.endswith("e"):
            participle_form = mne_affixation.get_joined_form(participle_form, "ed")
        else:
            participle_form += "d"

    # TODO: Move this somewhere else
    if participle_form.endswith("ren") and len(participle_form) >= 4 and participle_form[-4] in ["a", "e", "i", "o", "u", "y"]:
        # Handle cases like 'boren' -> 'born'
        participle_form = participle_form[0:-2] + "n"

    return participle_form

def oe_form_to_ne_form(oe_form, config):
    elements = oe_form.split("-")
    modern_form = ""

    for element_form in elements:
        prefix = oe_morphology.get_prefix(element_form)
        if prefix != None:
            # Prefixes aren't subjected to the usual form evolution process, but have their own distinct forms
            # Note that at present, trying to process a word with its prefix attached to it will cause problems with e.g. syllable stress
            form = prefix
        else:
            irregular_form = get_irregular_form(oe_form, config)
            if irregular_form != None:
                form = irregular_form
            else:
                form = get_updated_form(element_form, config)

        modern_form += form

    return modern_form

def get_updated_form(form, config):
    oe_phonemes = oe_read.to_phonemes(form)
    me_phonemes = me_phonology.from_oe_phonemes(oe_phonemes, config)
    return mne_write.from_me_phonemes(me_phonemes, config)

# For the given Old English form, return an alternate form that should have the
# evolution process applied to it rather than the one supplied.
def get_irregular_form(cited_form, config):
    # Contracted class 7 strong verbs use irregular '-ang' form in MnE.
    # e.g. 'hōn' -> 'hang', 'gōn' -> 'gang'
    if cited_form[-3:] == "|ōn":
        if config.verbose:
            print("- Using contracted class 7 strong verb irregular form in '-ang'" + config.separator)
        # HACK: This doesn't represent a historical form, but is devised such that phonetic evolution will
        # always produce a modern form in '-ang'.
        # TODO: Come up with something cleaner here. Maybe a context property for evolution to enforce this spelling.
        return cited_form[:-3] + "æng"

    return None
