import random

import src.utils.inflection as inflection

from src.models.morph import Morph

# Generates an ad-hoc morph describing an alternate form for a common word
def with_alternate_form(morph, form):
    new_dict = {}
    new_dict["key"] = morph.morph["key"] + "-adhoc:alt"
    new_dict["type"] = morph.morph["type"]
    new_dict["gloss"] = "alternate form of '" + morph.morph["form-canon"] + "'"
    new_dict["form-final"] = form
    new_dict["tags"] = ["fixed-gloss", "final"]
    new_dict["origin"] = morph.morph["origin"]

    return Morph(new_dict)

def with_alternate_gloss(morph):
    new_dict = {}
    new_dict["key"] = morph.morph["key"] + "-adhoc:alt"
    new_dict["type"] = morph.morph["type"]
    new_dict["form-raw"] = morph.morph["form-raw"]
    if "form-canon" in morph.morph:
        new_dict["form-canon"] = morph.morph["form-canon"]
    if "tags" in morph.morph:
        new_dict["tags"] = morph.tags()
    new_dict["origin"] = morph.morph["origin"]

    if isinstance(morph.morph["gloss-alt"], list):
        new_dict["gloss"] = random.choice(morph.morph["gloss-alt"])
    elif isinstance(morph.morph["gloss-alt"], str):
        new_dict["gloss"] = morph.morph["gloss-alt"]

    if "verb-class" in morph.morph:
        new_dict["verb-class"] = morph.morph["verb-class"]

    return Morph(new_dict)

def with_alternate_form_and_gloss(morph, form):
    new_dict = {}
    new_dict["key"] = morph.morph["key"] + "-adhoc:alt"
    new_dict["type"] = morph.morph["type"]
    new_dict["form-final"] = form
    new_dict["origin"] = morph.morph["origin"]
    if "tags" in morph.morph:
        new_dict["tags"] = morph.tags()
    
    if isinstance(morph.morph["gloss-alt"], list):
        new_dict["gloss"] = random.choice(morph.morph["gloss-alt"])
    elif isinstance(morph.morph["gloss-alt"], str):
        new_dict["gloss"] = morph.morph["gloss-alt"]

    if "verb-class" in morph.morph:
        new_dict["verb-class"] = morph.morph["verb-class"]

    return Morph(new_dict)

def from_past_participle(morph, participle_form):
    new_dict = {}
    new_dict["key"] = morph.morph["key"] + "-adhoc:ppart"
    new_dict["form-stem"] = participle_form
    new_dict["form-final"] = participle_form
    new_dict["type"] = "adj"
    new_dict["tags"] = ["past-participle"]
    new_dict["origin"] = morph.morph["origin"]

    original_gloss = morph.morph["gloss"]
    if isinstance(original_gloss, list):
        new_dict["gloss"] = random.choice(original_gloss)
    else:
        new_dict["gloss"] = original_gloss
    new_dict["gloss"] = inflection.inflect(new_dict["gloss"], "ppart")

    canon_form = None
    canon_participles = None
    if "form-canon" in morph.morph:
        canon_form = morph.morph["form-canon"]
    if "form-participle-canon" in morph.morph:
        canon_participles = morph.morph["form-participle-canon"]
    if not morph.has_tag("obscure") and not morph.has_tag("speculative") \
        and canon_form == original_gloss \
        and canon_participles \
        and participle_form not in canon_participles:
        # NOTE: My other idea for the last condition above was:
        #   "form-participle-canon" in new_dict:
        # They both produce some weird output.
        # TODO: Do this or non-final tag randomly
        new_dict["gloss"] = "alternate form of '" + canon_participles[0] + "'"
        new_dict["tags"] += ["fixed-gloss", "final"]

    # TODO: Let this enable prefixes but not suffixes
    # elif not morph.has_tag("obscure") and not morph.has_tag("speculative") \
    #     and participle_form in canon_participles:
    #    new_dict["tags"] += ["non-final"]

    return Morph(new_dict)