import src.utils.helpers as helpers

from random import Random

from src.evolutor import evolutor
from src.evolutor.engine.config import Config
from src.utils.logging import Logger

class Former_Config():
    def __init__(self, include_alt_forms=False, canon_lock=True):
        self.include_alt_forms = include_alt_forms
        self.canon_lock = canon_lock

def form(morph, env, config=Former_Config()):
    form = ""

    morph_dict = morph.morph
    
    if env.next:
        next_morph = env.next.morph
    else:
        next_morph = None
        
    if env.prev:
        last_morph = env.prev.morph
    else:
        last_morph = None

    # Rules including sound evolution
    # Affixes always use canonical forms, if present
    if "form-raw" in morph_dict \
        and not ("form-stem" in morph_dict and morph.is_affix()):

        if morph_dict["origin"] == "old-english":
            # If canon-locked, use canon form
            if "form-canon" in morph_dict and config.canon_lock:
                return morph_dict["form-canon"]

            # Decide which form to use
            forms = []
            if type(morph_dict["form-raw"]) == list:
                forms = morph_dict["form-raw"]
            else:
                forms = [morph_dict["form-raw"]]

            if config.include_alt_forms and "form-raw-alt" in morph_dict:
                forms += helpers.list_if_not(morph_dict["form-raw-alt"])

            random = Random(morph.seed)
            raw_form = random.choice(forms)

            # Sub-function for processing
            def process(form):
                locked = True
                if morph.has_tag("obscure") or morph.has_tag("speculative"):
                    locked = False
                config = Config(locked=locked, seed=morph.seed)
                return evolutor.oe_form_to_ne_form(form, config) 

            # Process, dividing into chunks if needed
            if not "-" in raw_form:
                form = process(raw_form)
            else:
                split_form = raw_form.split("-")
                form = "".join([process(f) for f in split_form])

    # Get the proper form of the morph
    elif env.next != None:

        # Follow special assimilation rules if there are any
        if "form-assimilation" in morph_dict:

            next_form = env.next.as_dict(env.next_env(env.next))["form"]
            next_letter = next_form[0]

            assimilation_map = {}
            matched_case = None
            star_case = None

            for case, sounds in morph_dict["form-assimilation"].items():
                for sound in sounds:
                    if sound == "*":
                        star_case = case
                    elif sound not in assimilation_map:
                        if sound not in assimilation_map:
                            assimilation_map[sound] = case
                        else:
                            Logger.error("Repeated assimilation sound for key " + morph_dict["key"])

            for key in reversed(sorted(list(assimilation_map.keys()), key=len)):
                if next_form.startswith(key):
                    matched_case = assimilation_map[key]
                    break

            if matched_case:
                case = matched_case
            elif star_case:
                case = star_case

            if case == "form-stem":
                form = morph_dict["form-stem"]
            elif case == "form-stem-assim":
                form = morph_dict["form-stem-assim"]
            elif case == "cut":
                form = morph_dict["form-stem"] + "/"
            elif case == "double":
                form = morph_dict["form-stem-assim"] + next_letter
            elif case == "nasal":
                if next_letter == 'm' or next_letter == 'p' or next_letter == 'b':
                    form = morph_dict["form-stem-assim"] + 'm'
                else:
                    form = morph_dict["form-stem-assim"] + 'n'
            else:
                form = case

        # Default rules
        else:
            # Usually we'll use stem form
            if "form-stem" in morph_dict:
                form = morph_dict["form-stem"]

            # TODO: Make this more generalizable between languages
            
            # Verbs or verbal derivations need to take participle form into account
            elif morph_dict["type"] == "verb" or (morph_dict["type"] == "suffix" and morph_dict["derive-to"] == "verb"):
                if next_morph and "derive-participle" in next_morph:
                    if next_morph["derive-participle"] == "present":
                        form = morph_dict["form-stem-present"]
                    elif next_morph["derive-participle"] == "perfect":
                        form = morph_dict["form-stem-perfect"]
                elif "form-stem-verb" in morph_dict:
                    form = morph_dict["form-stem-verb"]
                else:
                    form = morph_dict["form-stem-perfect"]

            # Use final form if nothing overrides
            else:
                form = morph_dict["form-final"]

    # The final morph form
    else:
        if morph_dict["type"] == "prep":
            form = morph_dict["form-stem"]
        else:
            if "form-final" in morph_dict:
                form = morph_dict["form-final"]
            else:
                # If there's no final form, use stem
                form = morph_dict["form-stem"]
    
    form = helpers.one_or_random(form, seed=morph.seed)
    
    return form
