import lemminflect

singular = "sg"
plural = "pl"
past_participle = "ppart"
present_participle = "part"
third_singular = "3sg"
infinitive = "inf"

# Returns an inflected form of the given word according to the mode
def inflect(word, mode):
    words = word.split(" ")    
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

            words[i] = word[1:-1]
        elif len(words) > 1:
            continue

        # Local overrides for forms the 3rd party library does wrong
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
        
        # Add back stripped final punctuation
        if final_punctuation:
            words[i] += final_punctuation
    
    return " ".join(words)

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
