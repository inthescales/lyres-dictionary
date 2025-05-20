# Returns a string concatenating the given form and addition strings, applying
# typical Greek sound change rules.
def get_joined_form(form, addition):
	# e.g. tarac- (tarassein) + -sia -> (a)taraxia
    if form[-1] in ["c", "k", "g"] and addition[0] == "s":
        form = form[:-1]
        addition = "x" + addition[1:]

    # e.g. prac- (prattein) + -ma -> pragma(tic)
    elif form[-1] in ["c", "k"] and addition[0] == "m":
        form = form[:-1] + "g"
        addition = addition
   	
    elif form[-1] == "p" and addition[0] == "m":
        form = form[:-1] + "m"
    
    elif form[-1] == "t" and addition in ["ia", "y"] and form[-2] not in ["n", "r", "s", "u"]:
        form = form[:-1] + "s"

    return form + addition

# Returns a joining fowel for the given morphs and the form to be added
def joining_vowel(first, second, addition):
    if not helpers.is_vowel(addition[0], y_is_vowel=True):
        return "o"
    else:
        return ""