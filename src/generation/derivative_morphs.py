import random

import src.utils.inflection as inflection

# Generates an ad-hoc morph describing an alternate form for a common word
def with_alternate_form(morph, form):
    morph.morph["key"] += "-adhoc:alt"
    morph.morph["gloss"] = "alternate form of '" + morph.morph["form-canon"] + "'"
    del morph.morph["form-raw"]
    del morph.morph["form-canon"]
    morph.morph["form-final"] = form
    if "tags" in morph.morph:
        morph.morph["tags"] += ["fixed-gloss"]
    else:
        morph.morph["tags"] = ["fixed-gloss"]

    return morph

def with_alternate_gloss(morph):
    morph.morph["key"] += "-adhoc:alt"
    if isinstance(morph.morph["gloss-alt"], list):
        morph.morph["gloss"] = random.choice(morph.morph["gloss-alt"])
    elif isinstance(morph.morph["gloss-alt"], str):
        morph.morph["gloss"] = morph.morph["gloss-alt"]

    return morph

def with_alternate_form_and_gloss(morph, form):
    morph.morph["key"] += "-adhoc:alt"

    if isinstance(morph.morph["gloss-alt"], list):
        morph.morph["gloss"] = random.choice(morph.morph["gloss-alt"])
    elif isinstance(morph.morph["gloss-alt"], str):
        morph.morph["gloss"] = morph.morph["gloss-alt"]

    del morph.morph["form-raw"]
    del morph.morph["form-canon"]
    morph.morph["form-final"] = form

    return morph

def from_past_participle(morph, participle_form):
    morph.morph["key"] += "-adhoc:ppart"
    morph.morph["type"] = "adj"

    original_gloss = morph.morph["gloss"]
    if isinstance(morph.morph["gloss"], list):
        morph.morph["gloss"] = random.choice(morph.morph["gloss"])
    morph.morph["gloss"] = inflection.inflect(morph.morph["gloss"], "ppart")
    if not morph.has_tag("obscure") and not morph.has_tag("speculative") \
        and morph.morph["form-canon"] == original_gloss:
        # NOTE: My other idea for the last condition above was:
        #   "form-participle-canon" in morph.morph:
        # They both produce some weird output.
        morph.morph["gloss"] = "alternate form of '" + morph.morph["form-participle-canon"][0] + "'"

    del morph.morph["form-raw"]
    if "form-canon" in morph.morph:
        del morph.morph["form-canon"]
    morph.morph["form-final"] = participle_form
    if "tags" in morph.morph:
        morph.morph["tags"] += ["fixed-gloss"]
    else:
        morph.morph["tags"] = ["fixed-gloss"]

    return morph