import lemminflect
import src.helpers as helpers

def inflect(string, mode):
    
    words = string.split(" ")    
    for i, word in enumerate(words):
        if word[0] == "[" and word[-1] == "]":
            words[i] = word[1:-1]
        elif len(words) > 1:
            continue

        # Local checking for forms 3rd party library does wrong
        override = override_inflection(words[i], mode)
        if override != None:
            return override  
        
        if mode == "ppart":
            words[i] = lemminflect.getInflection(words[i], tag='VBN')[0]
        elif mode == "part":
            words[i] = lemminflect.getInflection(words[i], tag='VBG')[0]
        elif mode == "3sg":
            words[i] = lemminflect.getInflection(words[i], tag='VBZ')[0]
        elif mode == "inf":
            continue
        elif mode == "sg":
            words[i] = lemminflect.getInflection(words[i], tag='NN')[0]
        elif mode == "pl":
            words[i] = lemminflect.getInflection(words[i], tag='NNS')[0]
        elif mode == "mass":
            words[i] = lemminflect.getInflection(words[i], tag='NN')[0]
        elif mode == "singleton":
            words[i] = lemminflect.getInflection(words[i], tag='NN')[0]
            
    return " ".join(words)

def override_inflection(string, mode):
    if string == "do":
        if mode == "3sg":
            return "does"
        elif mode == "ppart":
            return "done"
    elif string == "two":
        if mode == "pl":
            return "twos"
    elif string == "omen":
        if mode == "pl":
            return "omens"
    elif string == "urine":
        if mode == "pl":
            return "urines"

    return None
