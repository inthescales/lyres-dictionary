from src.tools.morphs.schemas.languages import valid_languages
from src.tools.morphs.validation.type_validation import Any, Array, Dict, Integer, Meta, one_or_more, schemata, String, valueset_type, ValueSet

from src.tools.morphs.schemas.properties import properties as valid_properties

# Checks that the morphs
def validate_properties(morph):
    errors = []

    # Returns true if the key and optional value type are found by the given morph.
    # key_required indicates whether errors should be logged if the given key is missing
    # Clause format:
    # - key                                 valid if the key exists in the morph
    # - values:
    #    - list                             valid if the key's value is any of the elements in the list
    #    - dict { "one-or-many": [list] }   valid if the key's value is one of the elements in the list, or a list
    #                                       all of whose contents are in the given list
    def evaluate_key(clause, morph, key_required=True, category=None):
        key = clause["key"]
        if key not in morph:
            if key_required:
                if category == None:
                    errors.append("property '" + key + "' is required all morphs")
                else:
                    errors.append("property '" + key + "' is required for morphs of type '" + category + "'")
            return False

        elif "values" in clause:
            if type(clause["values"]) is list:
                accepted = clause["values"]
                if morph[key] not in accepted:
                    errors.append("invalid value '" + str(morph[key]) + "' for property '" + key + "' in morph '" + morph["key"] + "'. Accepted values: " + str(accepted))
                    return False
            elif type(clause["values"] is dict) and "one-or-many" in clause["values"]:
                accepted = clause["values"]["one-or-many"]
                if morph[key] not in accepted and not (type(morph[key]) == list and all(x in accepted for x in morph[key])):
                    errors.append("invalid value '" + str(morph[key]) + "' for property '" + key + "' in morph '" + morph["key"] + "'. Accepted values: " + str(accepted) + ", or a list of these.")
                    return False
            else:
                errors.append("unrecognized validation values requirement: " + str(clause["values"]))

        return True

    # Returns true if any of the tags given in the clause are found in the morph
    def evaluate_tags(clause, morph, category):
        if "tags" not in morph:
            if category == None:
                errors.append("all morphs require one of the following tags: " + str(clause["tags"]))
            else:
                errors.append("morphs of type '" + category + "' require one of the following tags: " + str(clause["tags"]))
            return False

        for tag in clause["tags"]:
            if tag in morph["tags"]:
                return True

        if category == None:
            errors.append("all morphs require one of the following tags: " + str(clause["tags"]))
        else:
            errors.append("morphs of type '" + category + "' require one of the following tags: " + str(clause["tags"]))

        return False

    # Returns true if any of the given clauses are satisfied by the given morph
    # Any format:
    #anylist of clauses, at least one of which must be valid
    def evaluate_any(clauses, morph, category=None):
        for clause in clauses:
            if evaluate_key(clause, morph, False, category):
                return True

        if category == None:
            errors.append("all morphs must contain one of: " + ", ".join([x["key"] for x in clauses]))
        else:
            errors.append("morphs of type '" + category + "' must contain one of: " + ", ".join([x["key"] for x in clauses]))

        return False

    # Checks whether the given requirements are satisfied by the given morph
    def evaluate_requirements(requirements, morph, category=None):
        valid = True
        for requirement in requirements:
            if "any" in requirement:
                valid = evaluate_any(requirement["any"], morph, category) and valid
            elif "tags" in requirement:
                valid = evaluate_tags(requirement, morph, category) and valid
            elif "key" in requirement:
                valid = evaluate_key(requirement, morph, True, category) and valid
            else:
                errors.append("unrecognized validation requirement type: " + str(requirement))

        return valid

    # Properties required by all morphs
    universal_requirements = [
        Dict({ "key": String() }, restrict=False),
        Dict({ "type": String(valueset_type) }, restrict=False),
        Dict({ "origin": String(ValueSet("origin", valid_languages)) }, restrict=False)
    ]
    for requirement in universal_requirements:
        errors += new_val(morph, requirement)

    # Properties required by all morphs of a certain type
    type_requirements = {
        "noun": [
            Dict({ "tags": Array(String(ValueSet("countability", ["count", "mass", "singleton", "uncountable"])), require_all=False)}, restrict=False),
            Dict({ "tags": Array(String(ValueSet("concreteness", ["concrete", "abstract"])), require_all=False)}, restrict=False)
        ],
        "suffix": [
            Dict({ "derive-from": one_or_more(String(valueset_type)) }, restrict=False),
            Dict({ "derive-to": String(valueset_type) }, restrict=False),
        ],
        "prep": [
            Dict({ "derive-from": one_or_more(String(valueset_type)) }, restrict=False),
        ],
        "prefix": [
            Dict({ "derive-from": one_or_more(String(valueset_type)) }, restrict=False),
        ]
    }
    if "type" in morph and morph["type"] in type_requirements:
        for requirement in type_requirements[morph["type"]]:
            errors += new_val(morph, requirement)

    # Properties required by all morphs of a certain type and origin
    origin_type_requirements = {
        "latin": {
            "noun": [
                Dict({ "form-stem": one_or_more(String()) }, restrict=False),
                Dict({ "declension": Integer(ValueSet("Latin noun declension", [0, 1, 2, 3, 4, 5])) }, restrict=False),
            ],
            "adj": [
                Dict({ "form-stem": one_or_more(String()) }, restrict=False),
                Dict({ "declension": Integer(ValueSet("Latin adjective declension", [0, 12, 3])) }, restrict=False),
            ],
            "verb": [
                Any([
                    Dict({ "form-stem-present": one_or_more(String()) }, restrict=False),
                    Dict({ "form-stem":one_or_more(String()), "form-final": one_or_more(String()) }, restrict=False)
                ]),
                Dict({ "conjugation": Integer(ValueSet("Latin verb conjugation", [0, 1, 2, 3, 4])) }, restrict=False),
            ],
            "prefix": [
                Dict({ "form-stem": one_or_more(String()) }, restrict=False)
            ],
            "prep": [
                Any([
                    Dict({ "form-stem": one_or_more(String()) }, restrict=False),
                    Dict({ "form-assimilation": Dict({ "base": String(), "stem": String(), "case": Dict({}, restrict=False) }) }, restrict=False)
                ])
            ]
        },
        "greek": {
            "noun": [
                Dict({ "form-stem": one_or_more(String()) }, restrict=False),
            ],
            "adj": [
                Dict({ "form-stem": one_or_more(String()) }, restrict=False),
            ],
            "verb": [
                Dict({ "form-stem": one_or_more(String()) }, restrict=False),
            ]
        },
        "old-english": {
            "noun": [
                Any([
                    Dict({ "form-stem": one_or_more(String()) }, restrict=False),
                    Dict({ "form-raw": one_or_more(String()) }, restrict=False)
                ])
            ],
            "adj": [
                Any([
                    Dict({ "form-stem": one_or_more(String()) }, restrict=False),
                    Dict({ "form-raw": one_or_more(String()) }, restrict=False)
                ])
            ],
            "verb": [
                Any([
                    Dict({ "form-stem": one_or_more(String()) }, restrict=False),
                    Dict({ "form-raw": one_or_more(String()) }, restrict=False)
                ]),
                Dict(
                    { "verb-class": Any([
                        Integer(ValueSet("verb class", [1, 2, 3, 4, 5, 6, 7])),
                        String(ValueSet("verb class", ["weak", "preterite-present"]))
                    ])},
                    restrict=False
                )
            ]
        }
    }

    if "origin" in morph and morph["origin"] in origin_type_requirements \
        and "type" in morph and morph["type"] in origin_type_requirements[morph["origin"]]:
            for requirement in origin_type_requirements[morph["origin"]][morph["type"]]:
                errors += new_val(morph, requirement)

    # Properties required within form assimilation blocks
    if "form-assimilation" in morph:
        assimilation_requirements = [
            { "key": "base" },
            { "key": "stem" },
            { "key": "case" }
        ]

        evaluate_requirements(assimilation_requirements, morph["form-assimilation"], "assimilating forms")

    # Check key whitelist
    for key in morph:
        if not key in valid_properties:
            errors.append("Invalid morph property '" + key + "' found in morph '" + morph["key"] + "'")

    return errors

def new_val(value, expected, context="in morph"):
    if type(expected) == Dict and len(expected.reference.keys()) == 1:
        context = "in property '" + list(expected.reference.keys())[0] + "'"
    meta = Meta(context, schemata, context_override=True)
    errors = expected.get_errors(value, meta)
    return [err.text for err in errors]
