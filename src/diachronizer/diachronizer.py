import src.diachronizer.language.oe_phonology as oe_phonology
import src.diachronizer.language.me_phonology as me_phonology
import src.diachronizer.language.ne_orthography as ne_orthography

def oe_orth_to_oe_phone(oe_form, config):
    return oe_phonology.from_oe_written(oe_form)

def oe_phone_to_me_phone(oe_phone, config):
    return me_phonology.from_oe_phonemes(oe_phone, config)

def me_phone_to_ne_orth(me_phone, config):
    return ne_orthography.from_me_phonemes(me_phone, config)

def oe_form_to_ne_form(oe_form, config):
    elements = oe_form.split("-")
    modern_form = ""

    for element_form in elements:
        prefix = oe_phonology.get_prefix(element_form)
        if prefix != None:
            # Prefixes aren't subjected to the usual form evolution process, but have their own distinct forms
            # Note that at present, trying to process a word with its prefix attached to it will cause problems with e.g. syllable stress
            form = prefix
        else:
            oe_phonemes = oe_phonology.from_oe_written(element_form)
            me_phonemes = me_phonology.from_oe_phonemes(oe_phonemes, config)
            form = ne_orthography.from_me_phonemes(me_phonemes, config)
        
        modern_form += form

    return modern_form
