import src.language.modern_english.joining as mne_affixation

# Returns a weak preterite for the given form
def get_weak(form):
    if form.endswith("e"):
        return form + "d"
    elif form.endswith("ay"):
        return form[:-1] + "id"
    else:
        return mne_affixation.get_joined_form(form, "ed")
