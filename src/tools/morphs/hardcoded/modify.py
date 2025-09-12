def modify(morph):
    # Write code to modify the morph here, returning the new version
    if "form-raw" in morph \
        and "form-canon" in morph \
        and "form-participle-canon" in morph \
        and "form-raw-alt" not in morph \
        and "form-participle-raw" in morph \
        and type(morph["form-raw"]) == str:
        morph["form-oe"] = { 
            "form": {
                "infinitive": morph["form-raw"],
                "past-participle": morph["form-participle-raw"]
            },
            "canon": {
                "lemma": morph["form-canon"],
                "past-participle": morph["form-participle-canon"]
            }
        }
        del morph["form-raw"]
        del morph["form-canon"]
        del morph["form-participle-raw"]
        del morph["form-participle-canon"]

    return morph
