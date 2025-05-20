import src.language.old_english.read as oe_read
import src.language.old_english.morphology as oe_morphology
import src.language.old_english.phonology as oe_phonology
import src.language.old_english.participles as oe_participles
import src.language.middle_english.phonology as me_phonology
import src.language.modern_english.write as mne_write

from src.evolutor.engine.hinges import often, even, occ
from src.utils.logging import Logger

# Functions to be used externally ==================================

def oe_orth_to_oe_phone(oe_form, config):
    return oe_phonology.from_oe_written(oe_form)

def oe_phone_to_me_phone(oe_phone, config):
    return me_phonology.from_oe_phonemes(oe_phone, config)

def me_phone_to_ne_orth(me_phone, config):
    return ne_orthography.from_me_phonemes(me_phone, config)

def oe_form_to_ne_form(oe_form, config):
    return process(oe_form, config, get_modern_form)

def oe_form_to_ne_participle(oe_form, verb_class, config):
    return process(oe_form, config, lambda oe_form, config: get_participle_form(oe_form, verb_class, config))

# Old English form processing ======================================

# Control-flow function for applying any modernizing process to an Old English word while
# using stock prefix forms.
def process(oe_form, config, lammy):
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
                element_form = irregular_form

            form = lammy(element_form, config)

        modern_form += form

    return modern_form

# Returns a MnE form for a given OE word
def get_modern_form(form, config):
    oe_phonemes = oe_read.to_phonemes(form)
    me_phonemes = me_phonology.from_oe_phonemes(oe_phonemes, config)
    return mne_write.from_me_phonemes(me_phonemes, config)

# TODO: Move this to the participles file if possible.
# Consider using a lambda for the OE -> MnE transformation
def get_participle_form(oe_form, verb_class, config):
    if verb_class != "weak" and often("PPart:use-strong", config):
        # Strong participle forms
        pseudoparticiple = oe_participles.get_strong_pseudoparticiple(oe_form, verb_class, config)
        if pseudoparticiple == None:
            return None
        
        participle_form = oe_form_to_ne_form(pseudoparticiple, config)
        participle_form = oe_participles.get_strong_spelling_adjusted(participle_form, config)
    else:
        # Weak participle forms
        participle_form = oe_form_to_ne_form(oe_form, config)
        participle_form = oe_participles.get_weak_participle_form(participle_form)

    return participle_form

# For the given Old English form, return an alternate form that should have the
# evolution process applied to it rather than the one supplied.
# TODO: Move this somewhere else — it feels outside the scope of this file to
# be managing verb paradigms; rather it should be delegating that work.
def get_irregular_form(cited_form, config):
    # Contracted class 7 strong verbs in '-ōn', having '-ang' form in MnE.
    # These are contracted from earlier '-ahan' forms
    # e.g. 'hōn' -> 'hang', 'gōn' -> 'gang'
    if cited_form[-3:] == "|ōn":
        if config.verbose:
            Logger.trace("- Using contracted class 7 strong verb irregular form in '-ang'" + config.separator)

        # HACK: This doesn't represent a historical form, but is devised such that phonetic evolution will
        # always produce a modern form in '-ang'.
        # TODO: Come up with something cleaner here. Maybe a context property for evolution to enforce this spelling.
        return cited_form[:-3] + "æng"

    return None
