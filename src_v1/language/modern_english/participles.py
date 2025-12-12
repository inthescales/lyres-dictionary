import src.language.modern_english.joining as mne_affixation

# Make spelling adjustments in the MnE form of a participle based on PDE spelling conventions.
def adjust_strong_spelling(form, config):
    if form.endswith("ren") and len(form) >= 4 and form[-4] in ["a", "e", "i", "o", "u", "y"]:
        # Handle cases like 'boren' -> 'born', 'forloren' -> 'forlorn'
        return form[0:-2] + "n"

    # TODO: Add contracted participle forms.
    # See participle tests file for examples.
    # if form.endswith("ed") and often("PPart:contract-weak", config):

    return form

# Returns a weak participle for the given form
def get_weak(form):
    if form.endswith("e"):
        return form + "d"
    elif form.endswith("ay"):
        return form[:-1] + "id"
    else:
        return mne_affixation.get_joined_form(form, "ed")
