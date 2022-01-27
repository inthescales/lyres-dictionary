# Check placement requirements not belonging to an individual morph
def meets_requirements(morph, env):

    morph_dict = morph.morph

    if "participle-type" in morph_dict:
        link_key = "link-" + morph_dict["participle-type"]
        if not (link_key in env.prev.morph or "link" in env.prev.morph):
            return False

    return True
