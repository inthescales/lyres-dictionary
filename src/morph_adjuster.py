import src.diachronizer.language.oe_phonology as oe_phonology

# Makes automatic adjustments to morphs while importing data
def adjust_morph(morph):

    if morph["origin"] == "old-english":

        # Add 'no-prep' tag to any verb with a baked-in prepositional prefix
        if morph["type"] == "verb" \
            and "form-raw" in morph \
            and "-" in morph["form-raw"] \
            and any([oe_phonology.get_prefix(form) for form in morph["form-raw"].split("-")]) \
            and (not "tags" in morph or not "no-prep" in morph["tags"]):
            if "tags" in morph:
                morph["tags"] += ["no-prep"]
            else:
                morph["tags"] = ["no-prep"]

            # Make these rare too, for now
            if not "rare" in morph["tags"]:
                morph["tags"] += ["rare"]

        # Add 'rare' tag to homophonic words
        if "tags" in morph and "homophonic" in morph["tags"]:
            morph["tags"] += ["rare"]

    return morph
