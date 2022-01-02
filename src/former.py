import random

def form(morph, env):
    form = ""

    morph_dict = morph.morph
    
    if env.next:
        next_morph = env.next.morph
    else:
        next_morph = None
        
    if env.prev:
        last_morph = env.prev.morph
    else:
        last_morph = None

    # Get the proper form of the morph
    if env.next != None:

        # Follow special assimilation rules if there are any
        if "assimilation" in morph_dict:

            next_letter = list(next_morph["key"])[0]

            matched_case = None
            star_case = None

            for case, sounds in morph_dict["assimilation"].items():

                if "*" in sounds:
                    star_case = case

                if next_letter in sounds:
                    matched_case = case
                    break

            if matched_case:
                case = matched_case
            elif star_case:
                case = star_case

            if case == "link":
                form = morph_dict["link"]
            elif case == "link-assim":
                form = morph_dict["link-assim"]
            elif case == "cut":
                form = morph_dict["link"] + "/"
            elif case == "double":
                form = morph_dict["link-assim"] + next_letter
            elif case == "nasal":
                if next_letter == 'm' or next_letter == 'p' or next_letter == 'b':
                    form = morph_dict["link-assim"] + 'm'
                else:
                    form = morph_dict["link-assim"] + 'n'
            else:
                form = case


        # Default rules
        else:
            # Usually we'll use link form
            if "link" in morph_dict:
                form = morph_dict["link"]

            # Verbs or verbal derivations need to take participle form into account
            elif morph_dict["type"] == "verb" or (morph_dict["type"] == "derive" and morph_dict["to"] == "verb"):
                if next_morph and "participle-type" in next_morph:
                    if next_morph["participle-type"] == "present":
                        form = morph_dict["link-present"]
                    elif next_morph["participle-type"] == "perfect":
                        form = morph_dict["link-perfect"]
                elif "link-verb" in morph_dict:
                    form = morph_dict["link-verb"]
                else:
                    form = morph_dict["link-perfect"]

            # Use final form if nothing overrides
            else:
                form = morph_dict["final"]

    # The final morph form
    else:
        if morph_dict["type"] == "prep":
            form = morph_dict["link"]
        else:
            if "final" in morph_dict:
                form = morph_dict["final"]
            else:
                # If there's no final form, use link
                form = morph_dict["link"]
    
    if isinstance(form, list):
        form = random.choice(form)
    
    return form

def gloss(morph, env):
    
    morph_dict = morph.morph

    # Special case for prep-relative-to-noun cases (e.g. sub-limin-al)
    if env.prev and ((env.prev.get_type() == "noun" and env.anteprev and env.anteprev.get_type() == "prep" ) or (morph.get_type() == "verb" and env.prev.get_type() == "prep")) and "gloss-relative" in morph_dict:
        return morph_dict["gloss-relative"]
    
    if "gloss" in morph_dict:
        if morph_dict["type"] in ["noun", "verb"] and len(morph_dict["gloss"].split(" ")) == 1:
            return "[" + morph_dict["gloss"] + "]"
        else:
            return morph_dict["gloss"]
    else:
        
        if env.next:
            if "gloss-link" in morph_dict:
                return morph_dict["gloss-link"]
        else:
            if "gloss-final" in morph_dict:
                return morph_dict["gloss-final"]
        

        if morph.get_type() == "prep" or morph.get_type() == "prefix":
            relative = env.next
        else:
            relative = env.prev

        if relative and "gloss-" + relative.get_type() in morph_dict:
            return morph_dict["gloss-" + relative.get_type()]
    
    print("ERROR - failed to find gloss for " + morph_dict["key"])
