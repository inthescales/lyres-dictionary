# Get posting metadata for the given word
def for_word(word):
    meta = {}

    for morph in word.morphs:
        if morph.has_tag("sexual"):
            meta["warning"] = "May contain sexual content"

    return meta
