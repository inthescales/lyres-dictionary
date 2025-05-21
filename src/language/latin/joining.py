import src.utils.helpers as helpers

# Returns a joining fowel for the given morphs and the form to be added
def joining_vowel(first, second, addition):
    # Some noun declensions use a standard joining vowel
    if first.get_type() == "noun" and first.morph["declension"] in [4, 5] \
        and (addition[0] in ["a", "o", "u"]): # or not helpers.is_vowel(addition[0])):
            vowels = {4: "u", 5: "i"}
            return vowels[first.morph["declension"]]

    # For verb suffixes using the present participle stem
    if first.get_type() == "verb" \
        and "derive-participle" in second.morph \
        and second.morph["derive-participle"] == "present" \
        and not helpers.is_vowel(addition[0], y_is_vowel=True):

        # If the verb declares a joiner for this case, use it
        if "form-joiner-present" in first.morph:
            return first.morph["form-joiner-present"]

        # Exceptional present-stem verb endings
        if first.get_type() == "verb" and second.morph["key"] in ["-nt", "-nt-noun", "-nce", "-nd"]:
            verb_vowels = {1: "a", 2: "e", 3: "e", 4: "ie", 0: ""}
            return verb_vowels[first.morph["conjugation"]]

        if first.get_type() == "verb" and second.morph["key"] in ["-ble"]:
            verb_vowels = {1: "a", 2: "i", 3: "i", 4: "i", 0: ""}
            return verb_vowels[first.morph["conjugation"]]

    # Return the base vowel otherwise
    if not helpers.is_vowel(addition[0], y_is_vowel=True):
        return "i"
    else:
        return ""
