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
    oe_phonemes = oe_phonology.from_oe_written(oe_form)
    me_phonemes = me_phonology.from_oe_phonemes(oe_phonemes, config)
    modern_form = ne_orthography.from_me_phonemes(me_phonemes, config)

    return modern_form
