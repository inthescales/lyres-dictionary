def modify(morph):
    # Write code to modify the morph here, returning the new version
    if "prefix-on" in morph:
        morph["derive-from"] = morph["prefix-on"]
        del morph["prefix-on"]

    if "prefix-to" in morph:
        morph["derive-to"] = morph["prefix-to"]
        del morph["prefix-to"]

    return morph
