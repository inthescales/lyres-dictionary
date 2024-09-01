import src.utils.helpers as helpers

# Returns a string concatenating the given form and addition strings, with typical
# modern English spelling changes applied.
def get_joined_form(form, addition, y_to_i=False):
    if helpers.is_vowel(addition[0], True):
        if len(form) >= 2 \
        and helpers.is_consonant(form[-1], False) \
        and helpers.is_vowel(form[-2]) and not (len(form) >= 3 and helpers.is_vowel(form[-3])) \
            and form[-1] not in ["w", "x", "y"] \
            and helpers.syllable_count_simple(form) == 1:
            # If word ends in a consonant following a short vowel, and suffix begins with vowel, double the final consonant
            # Ex. 'cat' + 'y' -> 'catty'
            form = form + form[-1]
        elif form[-1] == "e" and helpers.is_consonant(form[-2]) and helpers.syllable_count_simple(form, True) > 1:
            # TODO: Use syllable count — any word ending in '-Ce' with one syllable has a silent e
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

    if form[-1] == "y" and y_to_i \
    	and helpers.is_consonant(addition[0]) \
    	and not (helpers.syllable_count(form, True) == 1 and helpers.is_consonant(form[-2])):
        # If word ends in 'y', is being suffixed with a consonant, and the y-to-i flag is on,
        # change the 'y' to 'i'. The flag generally corresponds with the '-y' and '-ly' suffixes.

        # Only do this if the word is *not* a one-syllable word ending in '-Cy'.
        # Ex. 'day' + 'ly' -> 'daily', 'doughty' + 'ness' -> 'doughtiness'
        # Ex. of exceptions: 'dry' + 'ly' -> 'dryly', 'shy' + 'ness' -> 'shyness'

        # NOTE: There is some inconsistency in this phenomenon, which appears to vary by time period.
        # OED usages show a lack of this phenomenon in the Middle English period, with it picking up
        # around the 1700's and continuing to the present.
        #
        # There also seem to be a number of exceptions. We see 'daily' and 'gaily', but also 'grayly'
        # and 'coyly'. This may result from avoidance of confusion as to what root is being modified,
        # where 'graily' might seem to be derived from 'grail', or 'coily' from 'coil'.
        # 
        # TODO: If I ever add a common word list to this codebase, I could use it here too.

        form = form[:-1] + "i"

    return form + addition
