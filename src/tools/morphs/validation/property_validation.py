import src.tools.morphs.validation.form_mne_validation as modern_english
import src.tools.morphs.validation.form_oe_validation as old_english

from src.tools.morphs.schemas.languages import valid_languages
from src.tools.morphs.validation.type_validation import Any, Array, Dict, Integer, Meta, One_Or_More, String, ValueSet, ValueSets

from src.tools.morphs.schemas.properties import properties as valid_properties

# Requirement definitions =================================

# Properties required by all morphs
universal_requirements = [
    Dict({ "key": String() }, restrict=False),
    Dict({ "type": String(ValueSets.type) }, restrict=False),
    Dict({ "origin": String(ValueSet("origin", valid_languages)) }, restrict=False)
]

# Properties required by all morphs of a certain type
type_requirements = {
    "noun": [
        Dict({ "tags": Array(String(ValueSet("countability", ["count", "mass", "singleton", "uncountable"])), require_all=False)}, restrict=False),
        Dict({ "tags": Array(String(ValueSet("concreteness", ["concrete", "abstract"])), require_all=False)}, restrict=False)
    ],
    "suffix": [
        Dict({ "derive-from": One_Or_More(String(ValueSets.type)) }, restrict=False),
        Dict({ "derive-to": String(ValueSets.type) }, restrict=False),
    ],
    "prep": [
        Dict({ "derive-from": One_Or_More(String(ValueSets.type)) }, restrict=False),
    ],
    "prefix": [
        Dict({ "derive-from": One_Or_More(String(ValueSets.type)) }, restrict=False),
    ]
}

# Properties required by all morphs of a certain type and origin
origin_type_requirements = {
    "latin": {
        "noun": [
            Dict({ "form-stem": One_Or_More(String()) }, restrict=False),
            Dict({ "declension": Integer(ValueSet("Latin noun declension", [0, 1, 2, 3, 4, 5])) }, restrict=False),
        ],
        "adj": [
            Dict({ "form-stem": One_Or_More(String()) }, restrict=False),
            Dict({ "declension": Integer(ValueSet("Latin adjective declension", [0, 12, 3])) }, restrict=False),
        ],
        "verb": [
            Any(
                [
                    Dict({ "form-stem-present": One_Or_More(String()) }, restrict=False),
                    Dict({ "form-stem":One_Or_More(String()), "form-final": One_Or_More(String()) }, restrict=False)
                ],
                custom_error="missing required form property: 'form-stem', 'form-stem-present'"
            ),
            Dict({ "conjugation": Integer(ValueSet("Latin verb conjugation", [0, 1, 2, 3, 4])) }, restrict=False),
        ],
        "prefix": [
            Dict({ "form-stem": One_Or_More(String()) }, restrict=False)
        ],
        "prep": [
            Any(
                [
                    Dict({ "form-stem": One_Or_More(String()) }, restrict=False),
                    Dict({ "form-assimilation": Dict({ "base": String(), "stem": String(), "case": Dict({}, restrict=False) }) }, restrict=False)
                ],
                custom_error="missing required form property: 'form-stem', 'form-assimilation'"
            )
        ]
    },
    "greek": {
        "noun": [
            Dict({ "form-stem": One_Or_More(String()) }, restrict=False),
        ],
        "adj": [
            Dict({ "form-stem": One_Or_More(String()) }, restrict=False),
        ],
        "verb": [
            Dict({ "form-stem": One_Or_More(String()) }, restrict=False),
        ]
    },
    "old-english": {
        "noun": [
            Any(
                [
                    Dict({ "form-stem": One_Or_More(String()) }, restrict=False),
                    Dict({ "form-raw": One_Or_More(String()) }, restrict=False),
                    Dict({ "form-oe": old_english.schema_head }, restrict=False)
                ],
                custom_error="missing required form property: 'form-stem', 'form-raw'"
            )
        ],
        "adj": [
            Any(
                [
                    Dict({ "form-stem": One_Or_More(String()) }, restrict=False),
                    Dict({ "form-raw": One_Or_More(String()) }, restrict=False),
                    Dict({ "form-oe": old_english.schema_head }, restrict=False)
                ],
                custom_error="missing required form property: 'form-stem', 'form-raw'"
            )
        ],
        "verb": [
            Any(
                [
                    Dict({ "form-stem": One_Or_More(String()) }, restrict=False),
                    Dict({ "form-raw": One_Or_More(String()) }, restrict=False),
                    Dict({ "form-oe": old_english.schema_head }, restrict=False)
                ],
                custom_error="missing required form property: 'form-stem', 'form-raw'"
            ),
            Dict({ "verb-class": ValueSet("verb class", [1, 2, 3, 4, 5, 6, 7, "weak", "preterite-present"]) }, restrict=False)
        ]
    }
}

# Execution ==============================================

schemata = old_english.schemata | modern_english.schemata

# Check the given value dict against the expected type tree
def check_values(value, expected, custom_error=None):
    context = "in morph"
    if type(expected) == Dict and len(expected.reference.keys()) == 1:
        context = "in property '" + list(expected.reference.keys())[0] + "'"

    if "key" in value:
        morph_id = value["key"]
    else:
        morph_id = "nokey"
    
    meta = Meta(context, schemata, missing_value_context="in morph", context_override=True, ident=morph_id)
    errors = expected.get_errors(value, meta)

    if custom_error != None:
        return [custom_error]
    else:
        return [err.text for err in errors]

# Validate the properties of the given morph
def validate_properties(morph):
    errors = []

    # Check universal requirements
    for requirement in universal_requirements:
        errors += check_values(morph, requirement)

    # Check type requirements
    if "type" in morph and morph["type"] in type_requirements:
        for requirement in type_requirements[morph["type"]]:
            errors += check_values(morph, requirement)

    # Check origin and type requirements
    if "origin" in morph and morph["origin"] in origin_type_requirements \
        and "type" in morph and morph["type"] in origin_type_requirements[morph["origin"]]:
            for requirement in origin_type_requirements[morph["origin"]][morph["type"]]:
                errors += check_values(morph, requirement)

    # Check key whitelist
    for key in morph:
        if not key in valid_properties:
            errors.append("Invalid morph property '" + key + "' found in morph '" + morph["key"] + "'")

    return errors
