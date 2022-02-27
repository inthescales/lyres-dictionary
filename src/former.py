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
        if "form-assimilation" in morph_dict:

            next_form = env.next.as_dict(env.next_env(env.next))["form"]
            next_letter = next_form[0]

            assimilation_map = {}
            matched_case = None
            star_case = None

            for case, sounds in morph_dict["form-assimilation"].items():
                for sound in sounds:
                    if sound == "*":
                        star_case = case
                    elif sound not in assimilation_map:
                        if sound not in assimilation_map:
                            assimilation_map[sound] = case
                        else:
                            print("ERROR: Repeated assimilation sound for key " + morph_dict["key"])

            for key in reversed(sorted(list(assimilation_map.keys()), key=len)):
                if next_form.startswith(key):
                    matched_case = assimilation_map[key]
                    break

            if matched_case:
                case = matched_case
            elif star_case:
                case = star_case

            if case == "form-stem":
                form = morph_dict["form-stem"]
            elif case == "form-stem-assim":
                form = morph_dict["form-stem-assim"]
            elif case == "cut":
                form = morph_dict["form-stem"] + "/"
            elif case == "double":
                form = morph_dict["form-stem-assim"] + next_letter
            elif case == "nasal":
                if next_letter == 'm' or next_letter == 'p' or next_letter == 'b':
                    form = morph_dict["form-stem-assim"] + 'm'
                else:
                    form = morph_dict["form-stem-assim"] + 'n'
            else:
                form = case


        # Default rules
        else:
            # Usually we'll use stem form
            if "form-stem" in morph_dict:
                form = morph_dict["form-stem"]

            # Verbs or verbal derivations need to take participle form into account
            elif morph_dict["type"] == "verb" or (morph_dict["type"] == "derive" and morph_dict["derive-to"] == "verb"):
                if next_morph and "derive-participle" in next_morph:
                    if next_morph["derive-participle"] == "present":
                        form = morph_dict["form-stem-present"]
                    elif next_morph["derive-participle"] == "perfect":
                        form = morph_dict["form-stem-perfect"]
                elif "form-stem-verb" in morph_dict:
                    form = morph_dict["form-stem-verb"]
                else:
                    form = morph_dict["form-stem-perfect"]

            # Use final form if nothing overrides
            else:
                form = morph_dict["form-final"]

    # The final morph form
    else:
        if morph_dict["type"] == "prep":
            form = morph_dict["form-stem"]
        else:
            if "form-final" in morph_dict:
                form = morph_dict["form-final"]
            else:
                # If there's no final form, use stem
                form = morph_dict["form-stem"]
    
    if isinstance(form, list):
        form = random.choice(form)
    
    return form

def gloss(morph, env):
    
    morph_dict = morph.morph

    # Special case for prep-relative-to-noun cases (e.g. sub-limin-al)
    if env.prev and ((env.prev.get_type() == "noun" and env.anteprev and env.anteprev.get_type() == "prep" ) or (morph.get_type() == "verb" and env.prev.get_type() == "prep")) and "gloss-relative" in morph_dict:
        if morph.get_type() == "verb" and len(morph_dict["gloss-relative"].split(" ")) == 1:
            return "[" + morph_dict["gloss-relative"] + "]"
        else:
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
