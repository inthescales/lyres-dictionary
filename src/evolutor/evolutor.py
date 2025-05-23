import src.language.middle_english.phonology as me_phonology
import src.language.modern_english.write as mne_write
import src.language.old_english.morphology as oe_morphology
import src.language.old_english.phonology as oe_phonology
import src.language.old_english.read as oe_read

# Functions to be used externally ==================================

def oe_orth_to_oe_phone(oe_form, config):
    return oe_phonology.from_oe_written(oe_form)

def oe_phone_to_me_phone(oe_phone, config):
    return me_phonology.from_oe_phonemes(oe_phone, config)

def me_phone_to_ne_orth(me_phone, config):
    return ne_orthography.from_me_phonemes(me_phone, config)

def oe_form_to_ne_form(oe_form, config):
    return process(oe_form, config, get_modern_form)

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
            irregular_form = oe_morphology.get_irregular_indicative(oe_form, config)
            if irregular_form != None:
                element_form = irregular_form

            form = lammy(element_form, config)

        if form == None:
            return None
        
        modern_form += form

    return modern_form

# Returns a MnE form for a given OE word
def get_modern_form(form, config):
    oe_phonemes = oe_read.to_phonemes(form)
    me_phonemes = me_phonology.from_oe_phonemes(oe_phonemes, config)
    return mne_write.from_me_phonemes(me_phonemes, config)
