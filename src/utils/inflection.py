import lemminflect

import src.utils.helpers as helpers

def inflect(string, mode):
    words = string.split(" ")    
    for i, word in enumerate(words):
        final_punctuation = None

        if word[0] == "[" \
            and (
                word[-1] == "]"
                or (word[-1] in [",", ";"] and word[-2] == "]")
            ):
            if word[-1] != "]":
                final_punctuation = word[-1]
                word = word[0:-1]

            words[i] = word[1:-1]
        elif len(words) > 1:
            continue

        # Local checking for forms 3rd party library does wrong
        override = override_inflection(words[i], mode)
        if override != None:
            words[i] = override          
        elif mode == "ppart":
            words[i] = lemminflect.getInflection(words[i], tag='VBN')[0]
        elif mode == "part":
            words[i] = lemminflect.getInflection(words[i], tag='VBG')[0]
        elif mode == "3sg":
            words[i] = lemminflect.getInflection(words[i], tag='VBZ')[0]
        elif mode == "inf":
            # do nothing
            pass
        elif mode == "sg":
            words[i] = lemminflect.getInflection(words[i], tag='NN')[0]
        elif mode == "pl":
            words[i] = lemminflect.getInflection(words[i], tag='NNS')[0]
        elif mode == "mass":
            words[i] = lemminflect.getInflection(words[i], tag='NN')[0]
        elif mode == "singleton":
            words[i] = lemminflect.getInflection(words[i], tag='NN')[0]
        
        if final_punctuation:
            words[i] += final_punctuation
    
    return " ".join(words)

def override_inflection(string, mode):
    if string == "arms":
        if mode == "pl":
            return "arms"

    elif string == "die":
        if mode == "pl":
            return "dice"

    elif string == "do":
        if mode == "3sg":
            return "does"
        elif mode == "ppart":
            return "done"

    elif string == "flour":
        if mode == "pl":
            return "flours"

    elif string == "omen":
        if mode == "pl":
            return "omens"

    elif string == "people":
        if mode == "pl":
            return "peoples"

    elif string == "two":
        if mode == "pl":
            return "twos"

    elif string == "urine":
        if mode == "pl":
            return "urines"

    return None
