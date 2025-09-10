def modify(morph):
    # Write code to modify the morph here, returning the new version
    if "form-raw" in morph \
        and "form-canon" in morph \
        and "form-raw-alt" not in morph \
        and "form-participle-raw" not in morph \
        and "form-participle-canon" not in morph \
        and type(morph["form-raw"]) == str:
        morph["form-oe"] = { "form": morph["form-raw"], "canon": morph["form-canon"] }
        del morph["form-raw"]
        del morph["form-canon"]

    return morph
