import src.language.old_english.orthography as orthography
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
