import src.evolutor.evolutor as evolutor
import src.language.modern_english.participles as mne_participles
import src.language.old_english.participles as oe_participles

from src.evolutor.engine.hinges import often

def oe_form_to_ne_participle(oe_form, verb_class, config):
    return evolutor.process(oe_form, config, lambda oe_form, config: get_participle_form(oe_form, verb_class, config))

# Consider using a lambda for the OE -> MnE transformation
def get_participle_form(oe_form, verb_class, config):
    if verb_class != "weak" and often("PPart:use-strong", config):
        # Strong participle forms
        pseudoparticiple = oe_participles.get_strong_pseudoparticiple(oe_form, verb_class, config)
        if pseudoparticiple == None:
            return None
        
        participle_form = evolutor.oe_form_to_ne_form(pseudoparticiple, config)
        participle_form = mne_participles.adjust_strong_spelling(participle_form, config)
    else:
        modern_form = evolutor.oe_form_to_ne_form(oe_form, config)
        participle_form = mne_participles.get_weak(modern_form)

    return participle_form
