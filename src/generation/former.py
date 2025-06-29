import src.generation.forming.oe_form as oe_form
import src.utils.helpers as helpers

from random import Random
from src.evolutor import evolutor
from src.evolutor.engine.config import Config
from src.utils.logging import Logger

class Former_Config():
    def __init__(self, include_alt_forms=False, canon_lock=True, seed=0):
        self.include_alt_forms = include_alt_forms
        self.canon_lock = canon_lock
        self.seed = seed

# Returns the form that the morph should have in the given environment
def form(morph, env, config=None):
    form = ""

    if config == None:
        config = Former_Config(seed=morph.seed)

    Rules including sound evolution
    Affixes always use fixed forms, if present
    if morph.has_raw_form() and not (morph.has_stem_form() and morph.is_affix()):

        # If canon-locked, use canon form if any
        if morph.has_canon_form() and config.canon_lock:
            return morph.get_canon_form()

        # Decide which form to use
        forms = morph.get_all_raw_forms(config.include_alt_forms)
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
        if morph.has_form_assimilation():
            # TODO: Add some kind of "base form" method?"
            next_form = env.next.as_dict(env.next_env(env.next))["form"]
            form = apply_assimilation(morph, next_form)

        # Stem form preëmpts other forms
        elif morph.has_stem_form():
            form = morph.get_stem_form()

        # Latin verbs and verbal derivations need to take participle form into account
        elif morph.get_origin() == "latin" and morph.get_type() == "verb" and env.next.get_base_type() == "suffix":
            stem_type = env.next.get_latin_suffix_stem_type()
            if stem_type == "present":
                form = morph.get_latin_present_stem()
            elif stem_type == "perfect":
                form = morph.get_latin_perfect_stem()
        else:
            Logger.error("no stem form found in non-final morph")

    else:
        if morph.has_final_form():
            form = morph.get_final_form()
        else:
            # If there's no final form, use stem
            # TODO: require a final form after I add a basic 'form' property
            form = morph.get_stem_form()
            Logger.trace("using stem form as final for morph '" + morph.get_key() + "'")
    
    form = helpers.one_or_random(form, seed=morph.seed)
    
    return form

# Get the relevant form from an assimilation dict, based on the following form
def apply_assimilation(morph, following):
    next_letter = following[0]

    assimilation_map = morph.get_assimilation_map()

    matched_case = None
    for key in reversed(sorted(list(assimilation_map.keys()), key=len)):
        if following.startswith(key):
            matched_case = assimilation_map[key]
            break

    if matched_case:
        case = matched_case
    else:
        if "*" in assimilation_map:
            case = assimilation_map["*"]
        else:
            Logger.trace("used default assimilation form '" + morph.get_assimilation_base() + " for morph " + morph.get_key() + "' followed by form '" + following + "'")
            return morph.get_assimilation_base()

    if case == "&base":
        return morph.get_assimilation_base()
    elif case == "&stem":
        return morph.get_assimilation_stem()
    elif case == "&cut":
        return morph.get_assimilation_base() + "/"
    elif case == "&geminate":
        return morph.get_assimilation_stem() + next_letter
    elif case == "&nasal":
        if next_letter == 'm' or next_letter == 'p' or next_letter == 'b':
            return morph.get_assimilation_stem() + 'm'
        else:
            return morph.get_assimilation_stem() + 'n'
    elif "&" in case:
        Logger.error("unrecognized assimilation code '" + case + "' in morph '" + morph.get_key() + "'")
    else:
        return case
