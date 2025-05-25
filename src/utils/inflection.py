import lemminflect

from src.utils.logging import Logger

singular = "sg"
plural = "pl"
past_participle = "ppart"
present_participle = "part"
third_singular = "3sg"
infinitive = "inf"

# Inflect the words in a gloss as indicated
def inflect_gloss(gloss, mode):
    words = gloss.split(" ")
    for i, word in enumerate(words):
        final_punctuation = None

        # Strip punctuation
        if word[0] == "[" \
            and (
                word[-1] == "]"
                or (word[-1] in [",", ";"] and word[-2] == "]")
            ):
            if word[-1] != "]":
                final_punctuation = word[-1]
                word = word[0:-1]

            word = word[1:-1]
        elif len(words) > 1:
            continue

        words[i] = inflect(word, mode)

        # Add back stripped final punctuation
        if final_punctuation:
            words[i] += final_punctuation

    return " ".join(words)

# Returns an inflected form of the given word according to the mode
def inflect(word, mode):
    override_form = override_inflection(word, mode)
    if override_form != None:
        return override_form

    if mode == infinitive:
        return word
    
    if mode == third_singular:
        return lemminflect.getInflection(word, tag='VBZ')[0]

    if mode == present_participle:
        return lemminflect.getInflection(word, tag='VBG')[0]

    if mode == past_participle:
        return lemminflect.getInflection(word, tag='VBN')[0]

    if mode == singular:
        return lemminflect.getInflection(word, tag='NN')[0]

    if mode == plural:
        return lemminflect.getInflection(word, tag='NNS')[0]
    
    Logger.error("unrecognized inflection mode '" + mode + "'")

# Custom overrides for words the inflection library gets wrong
def override_inflection(word, mode):
    if word == "arms":
        if mode == "pl":
            return "arms"

    elif word == "die":
        if mode == "pl":
            return "dice"

    elif word == "dusk":
        if mode == "pl":
            return "dusks"

    elif word == "do":
        if mode == "3sg":
            return "does"
        elif mode == "ppart":
            return "done"

    elif word == "flour":
        if mode == "pl":
            return "flours"

    elif word == "omen":
        if mode == "pl":
            return "omens"

    elif word == "ox":
        if mode == "pl":
            return "oxen"

    elif word == "people":
        if mode == "pl":
            return "peoples"

    elif word == "sting":
        if mode == "part":
            return "stinging"

    elif word == "two":
        if mode == "pl":
            return "twos"

    elif word == "urine":
        if mode == "pl":
            return "urines"

    return None
