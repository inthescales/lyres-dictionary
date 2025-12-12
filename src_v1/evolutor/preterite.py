import src.evolutor.evolutor as evolutor
import src.language.modern_english.preterite as mne_preterite
import src.language.old_english.preterite as oe_preterite

from src.evolutor.engine.hinges import often

def oe_form_to_ne_preterite(oe_form, verb_class, config):
    return evolutor.process(oe_form, config, lambda oe_form, config: get_preterite_form(oe_form, verb_class, config))

def get_preterite_form(oe_form, verb_class, config):
    if verb_class != "weak" and often("PPart:use-strong", config):
        # Get a strong pseudopreterite
        pseudopreterite = oe_preterite.get_strong_pseudopreterite(oe_form, verb_class, config)
        if pseudopreterite == None:
            return None
        
        # MnE preterites always resolve certain hinges in consistent ways.
        # Add overrides to the config.
        overrides = [["Orth:ɔː->oa/oCV", "oCV"], ["HL:ng", False], ["Orth:ɛ/iu->ew/ue", "ew"]]
        config = config.copy_with_overrides(overrides)

        # Evolve to modern form
        preterite_form = evolutor.oe_form_to_ne_form(pseudopreterite, config)
    else:
        # Get a weak preterite form
        modern_form = evolutor.oe_form_to_ne_form(oe_form, config)
        preterite_form = mne_preterite.get_weak(modern_form)

    return preterite_form
