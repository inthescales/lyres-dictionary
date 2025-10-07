import src.tools.morphs.validation.formsets.mne_formset_validation as modern_english
import src.tools.morphs.validation.formsets.oe_formset_validation as old_english

from src.tools.morphs.schemas.languages import valid_languages
from src.tools.morphs.schemas.periods import periods_for
from src.tools.morphs.validation.type_validation import All, Any, Array, Dict, Integer, Meta, Not, One_Or_More, Opt, String, ValueSet, ValueSets

from src.tools.morphs.schemas.languages import valid_languages as all_languages
from src.tools.morphs.schemas.properties import properties as valid_properties

# Requirement definitions =================================

gloss_requirement = Any([
    Dict({ "gloss": One_Or_More(String()) }, restrict=False),
    Dict({ "gloss-link": One_Or_More(String()), "gloss-final": One_Or_More(String()) }, restrict=False),
    Dict({ "gloss-adj": One_Or_More(String()) }, restrict=False),
    Dict({ "gloss-noun": One_Or_More(String()) }, restrict=False),
    Dict({ "gloss-number": One_Or_More(String()) }, restrict=False),
    Dict({ "gloss-verb": One_Or_More(String()) }, restrict=False),
    ],
    custom_error="no valid gloss property found"
)

# ----------------------------------------------------

# Properties required by all morphs
def make_universal_requirements(language):
    periods = periods_for(language)

    return [
        Dict({ "key": String() }, restrict=False),
        Dict({ "type": String(ValueSets.type) }, restrict=False),
        Dict({ "tags": Opt(Array(String(ValueSets.tag))) }, restrict=False),
        Dict({ "origin": String(ValueSet("origin", valid_languages)) }, restrict=False),
        Any([
                gloss_requirement,
                Dict(
                    { "senses": Array(
                        All([
                            Dict({
                                "id": Opt(Any([String(), Integer()], custom_error="invalid sense ID")),
                                "period": Opt(String(ValueSet("period", periods))),
                                "tags": Opt(Array(String(ValueSets.tag)))
                            }, restrict=False),
                            gloss_requirement
                        ])
                    )},
                    restrict=False
                )
            ],
            custom_error="must have either a gloss or a list of senses"
        ),
        Not(
            All([
                Dict({ "tags": Array(String(ValueSets.tag)) }, restrict=False),
                Dict(
                    { "senses": Array(
                            Dict({
                                "tags": Array(String(ValueSets.tag))
                            },
                            restrict=False),
                        require_all=False)
                    },
                    restrict=False
                )
            ]),
            custom_error="cannot have tags both on the morph and in senses"
        )
    ]

universal_requirements = {}
for language in all_languages:
    universal_requirements[language] = make_universal_requirements(language)

# Properties required by all morphs of a certain type
type_requirements = {
    "noun": [
        Any([
            All([
                Dict({ "tags": Array(String(ValueSet("countability", ["count", "mass", "singleton", "uncountable"])), require_all=False)}, restrict=False),
                Dict({ "tags": Array(String(ValueSet("concreteness", ["concrete", "abstract"])), require_all=False)}, restrict=False)
            ]),
            All([
                Dict({ "senses": Array(Dict({ "tags": Array(String(ValueSet("countability", ["count", "mass", "singleton", "uncountable"])), require_all=False)}, restrict=False)) }, restrict=False),
                Dict({ "senses": Array(Dict({ "tags": Array(String(ValueSet("concreteness", ["concrete", "abstract"])), require_all=False)}, restrict=False)) }, restrict=False)
            ])
        ],
        custom_error="all nouns must have a countability tag and a concreteness tag"
        )
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
    if "origin" in morph:
        for requirement in universal_requirements[morph["origin"]]:
            errors += check_values(morph, requirement)
    else:
        for requirement in make_universal_requirements(None):
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
