import src.utils.helpers as helpers

def get_joined_form(form, addition):
    if helpers.is_vowel(addition[0], True):
        if len(form) >= 2 \
        and helpers.is_consonant(form[-1], False) \
        and helpers.is_vowel(form[-2]) and not (len(form) >= 3 and helpers.is_vowel(form[-3])) \
            and form[-1] not in ["w", "x", "y"] \
            and helpers.syllable_count(form) == 1:
            # If word ends in a consonant following a short vowel, and suffix begins with vowel, double the final consonant
            # Ex. 'cat' + 'y' -> 'catty'
            form = form + form[-1]
        elif form[-1] == "e" \
            and (
                (helpers.is_consonant(form[-2]) and helpers.is_vowel(form[-3])) \
                or form[-2] == "l"
            ):
            # If word ends in a silent e, and suffix begins with a vowel, drop the e
            # Ex. 'rose' + 'y' -> 'rosy'
            form = form[:-1]
    elif helpers.is_consonant(addition[0]):
        if len(form) >= 2 and form[-2] == form[-1] and form[-1] == addition[0]:
            # Break up triple consonants by dropping one letter
            # Ex. 'full' + 'ly' -> 'fully'
            # TODO: Consider also using a dash here in some cases, such as 'burgess-ship'
            form = form[:-1]

        elif len(form) >= 2 and len(addition) >=2 and form[-2:-1] == addition[0:2] and addition[0:2] in ["sh", "ch", "th"]:
            # Break up repeated digraphs
            # Ex. 'fish' + 'ship' -X-> 'fishship'
            addition = "-" + addition

    if form[-1] == "y" \
        and (helpers.is_consonant(addition[0])):
        # If word ends in a vowel y, and suffix begins with a consonant or 'e'', change the y to i
        # Ex. 'day' + 'ly' -> 'daily', 'doughty' + 'ness' -> 'doughtiness'

        # NOTE: This is a phenomenon that mostly occurs to older constructions.
        # For instance, it applies in 'day' + 'ly' -> 'daily', but a more ad-hoc usage like
        # 'gray' + 'ly' -> 'graily' looks strage.
        #
        # I'm satisfied to use the earlier method for now when working from Old English, but in the
        # future will likely want to exempt certain additional cases.

        form = form[:-1] + "i"

    return form + addition
