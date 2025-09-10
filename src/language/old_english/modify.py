import src.language.old_english.orthography as orthography

# Returns a degeminated form of the given OE consonant cluster
def degeminate(form):
    if len(form) == 2:
        if form[0] == form[1] and form[0] in orthography.consonants:
            return form[0]
        elif form[0:2] == "ċġ":
            return "ġ"

    return form

# Apply Verner's Law, as it appears in inflected forms, to the given form, e.g. 'frosen' -> 'froren'
# Here I just replace the last, single consonant according to Verner's Law.
# Ignoring any cases with multiple consonants in the final cluster because I'm
# not sure whether Verner's Law should apply there - I'm not aware of any MnE cases.
# Equality check handles cases like 'hliehhan' -> 'hlæġen'
def apply_verner(form):
    verner_map = {
        "h": "ġ",
        "s": "r",
        "þ": "d"
    }
    if form[-1] not in orthography.consonants \
        or (form[-2] in orthography.consonants and form[-2] != form[-1]) \
        or form[-1] not in verner_map:
        return form

    if form[-2] != form[-1]:
        stem = form[:-1]
    else:
        stem = form[:-2]

    return stem + verner_map[form[-1]]
