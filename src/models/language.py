# Check placement requirements not belonging to an individual morph
def meets_requirements(morph, env):

    morph_dict = morph.morph

    if "derive-participle" in morph_dict:
        link_key = "form-stem-" + morph_dict["derive-participle"]
        if not (link_key in env.prev.morph or "form-stem" in env.prev.morph):
            return False

    return True
