import src.evolutor.language.oe_morphology as oe_morphology

# Makes automatic adjustments to morphs while importing data
def adjust_morph(morph):

    if morph["origin"] == "old-english":

        # Add 'no-prep' tag to any verb with a baked-in prepositional prefix
        if morph["type"] == "verb" \
            and "form-raw" in morph \
            and "-" in morph["form-raw"] \
            and any([oe_morphology.get_prefix(form) for form in morph["form-raw"].split("-")]) \
            and (not "tags" in morph or not "no-prep" in morph["tags"]):

            # For now, I don't actually want to see these
            # TODO: Try again when we have more morphs to balance these out
            # NOTE: These are in the ignore directory now. Remembering to move them out
            # if you want to try using them again.
            return None

            # if "tags" in morph:
            #     morph["tags"] += ["no-prep"]
            # else:
            #     morph["tags"] = ["no-prep"]

        # Add 'rare' tag to homophonic words
        if "tags" in morph and "homophonic" in morph["tags"]:
            morph["tags"] += ["rare"]

    return morph
