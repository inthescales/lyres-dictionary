import src.utils.helpers as helpers

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
def joining_vowel(first, second, form, addition):
    # Trying out determining whether forms ending in 'y' with additions beginning with
    # a consonant should depend on the number of syllables in the form.
    # For example, 'bryology' vs 'tachyscope'.
    # This doesn't work for 'ichthyology' though
    syllable_count = helpers.syllable_count_simple(form, y_is_vowel=True)
    if (not form[-1] in ["a", "o"] or (form[-1] == "y" and syllable_count == 1)) \
        and not helpers.is_vowel(addition[0], y_is_vowel=True):
        return "o"
    else:
        return ""