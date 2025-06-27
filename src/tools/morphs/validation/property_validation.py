from src.tools.morphs.schemas.languages import valid_languages
from src.tools.morphs.schemas.types import root_types
from src.tools.morphs.validation.type_validation import Dict, Meta, schemata, String, valueset_type, ValueSet

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

    # Example of checking for noun countability
    # if morph["type"] == "noun":
    #     errors += new_val(morph, Dict({ "tags": Array(String(ValueSet("countability", ["count", "mass", "singleton", "uncountable"])), require_all=False)}, restrict=False))

    # Properties required by morphs of a certain type
    type_requirements = {
        "noun": [
            { "tags": ["count", "mass", "singleton", "uncountable"] },
            { "tags": ["concrete", "abstract"] }
        ],
        "suffix": [
            { "key": "derive-from", "values": { "one-or-many": root_types } },
            { "key": "derive-to", "values": root_types }
        ],
        "prep": [
            { "key": "derive-from", "values": { "one-or-many": root_types }  },
        ],
        "prefix": [
            { "key": "derive-from", "values": { "one-or-many": root_types }  },
        ]
    }
    if "type" in morph and morph["type"] in type_requirements:
        evaluate_requirements(type_requirements[morph["type"]], morph, morph["type"])

    # Properties required by morphs of a certain type and origin
    origin_type_requirements = {
        "latin": {
            "noun": [
                { "key": "form-stem" },
                { "key": "declension", "values": [0, 1, 2, 3, 4, 5] },
            ],
            "adj": [
                { "key": "form-stem" },
                { "key": "declension", "values": [0, 12, 3] },
            ],
            "verb": [
                { "any": [
                    { "key": "form-stem-present" },
                    { "key": "form-stem" }
                ]},
                { "any": [
                    { "key": "form-final" },
                    { "key": "form-stem" }
                ]},
                { "key": "conjugation", "values": [0, 1, 2, 3, 4] },
            ],
            "prefix": [
                { "any": [
                    { "key": "form-stem" },
                    { "key": "form-assimilation" }
                ]}
            ]
        },
        "greek": {
            "noun": [
                { "key": "form-stem" },
            ],
            "adj": [
                { "key": "form-stem" },
            ],
            "verb": [
                { "key": "form-stem" },
            ]
        },
        "old-english": {
            "noun": [
                { "any": [
                    { "key": "form-stem" },
                    { "key": "form-raw" },
                ]}
            ],
            "adj": [
                { "any": [
                    { "key": "form-stem" },
                    { "key": "form-raw" },
                ]}
            ],
            "verb": [
                { "any": [
                    { "key": "form-stem" },
                    { "key": "form-raw" },
                ]},
                { "key": "verb-class", "values": [1, 2, 3, 4, 5, 6, 7, "weak", "preterite-present"] }
            ]
        }
    }

    if "origin" in morph and morph["origin"] in origin_type_requirements \
        and "type" in morph and morph["type"] in origin_type_requirements[morph["origin"]]:
        requirements = origin_type_requirements[morph["origin"]][morph["type"]]
        category = " ".join(morph["origin"].split("-")) + " " + morph["type"]
        evaluate_requirements(requirements, morph, category)

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

def new_val(value, expected):
    if "key" in value:
        context = "in morph with key '" + value["key"] + "'"
    else:
        context = "in morph without key " + str(value)
        
    meta = Meta(context, schemata)
    errors = expected.get_errors(value, meta)
    return [err.text for err in errors]
