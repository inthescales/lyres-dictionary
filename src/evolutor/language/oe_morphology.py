# Returns any prefix matching the given written form
def get_prefix(form):
    prefixes = {
        "a": "a",
        "ā": "a",
        "biġ": "by",
        "bī": "by",
        "be": "be",
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
        "t": "þ",
        "þ": "þ"
    }

    raw_value = "".join(form_tail).split("+")[0].split("|")[0]
    if raw_value in suffixes:
        return suffixes[raw_value]
