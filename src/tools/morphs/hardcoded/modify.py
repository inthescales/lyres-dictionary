def modify(morph):
    # Write code to modify the morph here, returning the new version
    if morph["type"] == "number":
        morph["type"] = "prefix"
        morph["derive-from"] = "noun"
        if "tags" not in morph:
            morph["tags"] = []
        morph["tags"].append("numerical")

    return morph
