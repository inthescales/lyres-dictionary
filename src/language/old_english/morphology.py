import src.generation.forming.oe_formset as oe_formset
import src.utils.helpers as helpers

from src.utils.logging import Logger

# Returns any prefix matching the given written form
def get_prefix(form):
    prefixes = {
        "a": "a",
        "ā": "a",
        "biġ": "by",
        "bī": "by",
        "be": "be",
        "for": "for",
        "ġe": "", # TODO: Allow this to be rendered as /a/, /e/, or /i/ in some cases (as in 'afford', 'enough', 'handiwork')
        "on": "a" # TODO: Maybe add a probability to this
    }

    if form in prefixes:
        return prefixes[form]

def get_derivational(form_tail):
    suffixes = {
        "ard": "ard",
        "els": "els",
        "else": "els",
        "elsi": "els",
        "en": "en",
        "iġ": "iġ",
        "t": "þ",
        "þ": "þ"
    }

    raw_value = "".join(form_tail).split("+")[0].split("|")[0]
    if raw_value in suffixes:
        return suffixes[raw_value]

# For the given Old English form, return an alternate indicative form that should have the
# evolution process applied to it rather than the one supplied.
def get_irregular_indicative(cited_form, config):
    # Level verbs ending in 'bb' to the 'f' form that typically appears in some forms.
    # Modern ex. 'libban' -> 'live', 'habban' -> 'have', 'hebban' -> 'heave'
    if len(cited_form) >=5 and cited_form[-5:] == "bb|an":
        return cited_form[:-5] + "f|an"

    # TODO: Maybe handle 'ċġ' -> /j/ here?

    # Contracted class 7 strong verbs in '-ōn', having '-ang' form in MnE.
    # These are contracted from earlier '-ahan' forms
    # e.g. 'hōn' -> 'hang', 'gōn' -> 'gang'
    if cited_form[-3:] == "|ōn":
        if config.verbose:
            Logger.trace("- Using contracted class 7 strong verb irregular form in '-ang'" + config.separator)

        # HACK: This doesn't represent a historical form, but is devised such that phonetic evolution will
        # always produce a modern form in '-ang'.
        # TODO: Come up with something cleaner here. Maybe a context property for evolution to enforce this spelling.
        return cited_form[:-3] + "æng"

    return None

# Returns True if the morph's form has a baked in '-iġ' ending
def has_ig_ending(morph):
    morph_dict = morph.morph

    if "form-raw" in morph_dict \
        and (
            (isinstance(morph_dict["form-raw"], str) and morph_dict["form-raw"].endswith("+iġ")) \
            or (isinstance(morph_dict["form-raw"], list) and any([form.endswith("+iġ") for form in morph_dict["form-raw"]])) \
        ):
        return True
    elif "form-oe" in morph_dict:
        formset = oe_formset.read(morph_dict["form-oe"], morph_dict["type"])
        lemmas = []
        for m in helpers.list_if_not(formset.all):
            for p in helpers.list_if_not(m.paradigm):
                for l in helpers.list_if_not(p.lemma):
                    if l.endswith("+iġ"):
                        return True

    return False
