import src.utils.helpers as helpers

from random import Random

from src.evolutor import evolutor
from src.evolutor.engine.config import Config
from src.utils.logging import Logger

class Former_Config():
    def __init__(self, include_alt_forms=False, canon_lock=True):
        self.include_alt_forms = include_alt_forms
        self.canon_lock = canon_lock

# Returns the form that the morph should have in the given environment
def form(morph, env, config=Former_Config()):
    form = ""

    morph_dict = morph.morph
    
    if env.next:
        next_morph = env.next.morph
    else:
        next_morph = None

    # Rules including sound evolution
    # Affixes always use canonical forms, if present
    if "form-raw" in morph_dict \
        and not ("form-stem" in morph_dict and morph.is_affix()):

        # If canon-locked, use canon form if any
        if "form-canon" in morph_dict and config.canon_lock:
            return morph_dict["form-canon"]

        # Decide which form to use
        forms = helpers.list_if_not(morph_dict["form-raw"])
        if "form-raw-alt" in morph_dict and config.include_alt_forms:
            forms += helpers.list_if_not(morph_dict["form-raw-alt"])

        random = Random(morph.seed)
        raw_form = random.choice(forms)

        # Sub-function for processing
        def process(form):
            # Common morphs already typically use canon-lock. Turning this off for more alternate forms
            # if morph.has_tag("obscure") or morph.has_tag("speculative"):
            #     locked = False
            # else:
            #     locked = True
            locked = False

            config = Config(locked=locked, seed=morph.seed)
            return evolutor.oe_form_to_ne_form(form, config) 

        # Process, dividing into chunks in the case of compounds
        if not "-" in raw_form:
            return process(raw_form)
        else:
            split_form = raw_form.split("-")
            return "".join([process(f) for f in split_form])

    # Stem or final form based on whether another morph follows
    if env.next != None:
        # Apply assimilation rules if there are any
        if "form-assimilation" in morph_dict:
            # TODO: Add some kind of "base form" method?"
            next_form = env.next.as_dict(env.next_env(env.next))["form"]
            form = apply_assimilation(morph, next_form)

        # Default rules
        else:
            # Usually use stem form
            if "form-stem" in morph_dict:
                form = morph_dict["form-stem"]

            # Latin verbs and verbal derivations need to take participle form into account
            elif morph.morph["origin"] == "latin" and morph.get_type() == "verb":
                if next_morph and "derive-participle" in next_morph:
                    if next_morph["derive-participle"] == "present":
                        form = morph_dict["form-stem-present"]
                    elif next_morph["derive-participle"] == "perfect":
                        form = morph_dict["form-stem-perfect"]
                else:
                    Logger.error("Latin suffix joins to verb but doesn't specify 'derive-participle'")
            else:
                Logger.error("no stem form found in non-final morph")

    else:
        if "form-final" in morph_dict:
            form = morph_dict["form-final"]
        else:
            # If there's no final form, use stem
            form = morph_dict["form-stem"]
    
    form = helpers.one_or_random(form, seed=morph.seed)
    
    return form

# Get the relevant form from an assimilation dict, based on the following form
def apply_assimilation(morph, following):
    next_letter = following[0]

    assimilation_map = {}
    matched_case = None
    star_case = None

    for case, sounds in morph.morph["form-assimilation"].items():
        for sound in sounds:
            if sound == "*":
                star_case = case
            elif sound not in assimilation_map:
                assimilation_map[sound] = case
            else:
                Logger.error("Repeated assimilation sound for key " + morph.morph["key"])

    for key in reversed(sorted(list(assimilation_map.keys()), key=len)):
        if following.startswith(key):
            matched_case = assimilation_map[key]
            break

    if matched_case:
        case = matched_case
    elif star_case:
        case = star_case

    if case == "form-stem":
        return morph.morph["form-stem"]
    elif case == "form-stem-assim":
        return morph.morph["form-stem-assim"]
    elif case == "cut":
        return morph.morph["form-stem"] + "/"
    elif case == "double":
        return morph.morph["form-stem-assim"] + next_letter
    elif case == "nasal":
        if next_letter == 'm' or next_letter == 'p' or next_letter == 'b':
            return morph.morph["form-stem-assim"] + 'm'
        else:
            return morph.morph["form-stem-assim"] + 'n'
    else:
        return case