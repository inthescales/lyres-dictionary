def validate_morph(morph):

    if not "key" in morph:
        print(" - key is missing")
        return False

    if not "type" in morph:
        print(" - type is missing")
        return False

    if not "origin" in morph:
        print(" - origin is missing")
        return False

    morph_type = morph["type"]

    # TODO - pull these requirements into per-language data
    # TODO - make countability a property, not a tag
    if morph_type == "noun":
        if morph["origin"] == "latin":
            if not "link" in morph or not "declension" in morph:
                print(" - noun must have 'link' and 'declension'")
                return False
            elif not ("tags" in morph and ("count" in morph["tags"] or "mass" in morph["tags"] or "singleton" in morph["tags"])):
                print(" - noun must have tag 'count', 'mass', or 'singleton'")
                return False
            elif morph["declension"] not in [0, 1, 2, 3, 4, 5]:
                print(" - invalid declension '" + str(morph["declension"]) + "'")
                return False
        elif morph["origin"] == "greek":
            if not "link" in morph:
                print(" - noun must have 'link'")
                return False
            elif not ("tags" in morph and ("count" in morph["tags"] or "mass" in morph["tags"] or "singleton" in morph["tags"])):
                print(" - noun must have tag 'count', 'mass', or 'singleton'")
                return False

    elif morph_type == "adj":
        if morph["origin"] == "latin":
            if not "link" in morph or not "declension" in morph:
                print(" - adjective must have 'link' and 'declension'")
                return False
            elif morph["declension"] not in [0, 12, 3]:
                print(" - invalid declension '" + str(morph["declension"]) + "'")
                return False
        elif morph["origin"] == "greek":
            if not "link" in morph:
                print(" - adjective must have 'link'")
                return False

    elif morph_type == "verb":
        if morph["origin"] == "latin":
            if not ("link-present" in morph and "final" in morph and "conjugation" in morph):
                print(" - verbs require 'link-present', 'link-perfect', 'final', and 'conjugation'")
                return False

            if morph["conjugation"] not in [0, 1, 2, 3, 4]:
                print(" - invalid conjugation '" + str(morph["conjugation"]) + "'")
                return False

    elif morph_type == "derive":
        if not ("derive-from" in morph and "derive-to" in morph):
            print(" - derive morphs must have 'derive-from' and 'derive-to'")
            return False

    return True
