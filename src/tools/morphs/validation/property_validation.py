from src.tools.morphs.schemas.languages import valid_languages
from src.tools.morphs.validation.type_validation import Any, Array, Dict, Integer, Meta, one_or_more, schemata, String, valueset_type, ValueSet

from src.tools.morphs.schemas.properties import properties as valid_properties

def check_values(value, expected, context="in morph", custom_error=None):
    if type(expected) == Dict and len(expected.reference.keys()) == 1:
        context = "in property '" + list(expected.reference.keys())[0] + "'"
    meta = Meta(context, schemata, missing_value_context="in morph", context_override=True)
    errors = expected.get_errors(value, meta)

    if custom_error != None:
        return [custom_error]
    else:
        return [err.text for err in errors]

def validate_properties(morph):
    errors = []

    # Properties required by all morphs
    universal_requirements = [
        Dict({ "key": String() }, restrict=False),
        Dict({ "type": String(valueset_type) }, restrict=False),
        Dict({ "origin": String(ValueSet("origin", valid_languages)) }, restrict=False)
    ]
    for requirement in universal_requirements:
        errors += check_values(morph, requirement)

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
            errors += check_values(morph, requirement)

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
                Any(
                    [
                        Dict({ "form-stem-present": one_or_more(String()) }, restrict=False),
                        Dict({ "form-stem":one_or_more(String()), "form-final": one_or_more(String()) }, restrict=False)
                    ],
                    custom_error="missing required form property: 'form-stem', 'form-stem-present'"
                ),
                Dict({ "conjugation": Integer(ValueSet("Latin verb conjugation", [0, 1, 2, 3, 4])) }, restrict=False),
            ],
            "prefix": [
                Dict({ "form-stem": one_or_more(String()) }, restrict=False)
            ],
            "prep": [
                Any(
                    [
                        Dict({ "form-stem": one_or_more(String()) }, restrict=False),
                        Dict({ "form-assimilation": Dict({ "base": String(), "stem": String(), "case": Dict({}, restrict=False) }) }, restrict=False)
                    ],
                    custom_error="missing required form property: 'form-stem', 'form-assimilation'"
                )
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
                Any(
                    [
                        Dict({ "form-stem": one_or_more(String()) }, restrict=False),
                        Dict({ "form-raw": one_or_more(String()) }, restrict=False)
                    ],
                    custom_error="missing required form property: 'form-stem', 'form-raw'"
                )
            ],
            "adj": [
                Any(
                    [
                        Dict({ "form-stem": one_or_more(String()) }, restrict=False),
                        Dict({ "form-raw": one_or_more(String()) }, restrict=False)
                    ],
                    custom_error="missing required form property: 'form-stem', 'form-raw'"
                )
            ],
            "verb": [
                Any(
                    [
                        Dict({ "form-stem": one_or_more(String()) }, restrict=False),
                        Dict({ "form-raw": one_or_more(String()) }, restrict=False)
                    ],
                    custom_error="missing required form property: 'form-stem', 'form-raw'"
                ),
                Dict(
                    { "verb-class": Any(
                            [
                            Integer(ValueSet("verb class", [1, 2, 3, 4, 5, 6, 7])),
                            String(ValueSet("verb class", ["weak", "preterite-present"]))
                        ],
                        custom_error="missing required property 'verb-class'"
                    )},
                    restrict=False
                )
            ]
        }
    }

    if "origin" in morph and morph["origin"] in origin_type_requirements \
        and "type" in morph and morph["type"] in origin_type_requirements[morph["origin"]]:
            for requirement in origin_type_requirements[morph["origin"]][morph["type"]]:
                errors += check_values(morph, requirement)

    # Check key whitelist
    for key in morph:
        if not key in valid_properties:
            errors.append("Invalid morph property '" + key + "' found in morph '" + morph["key"] + "'")

    return errors
