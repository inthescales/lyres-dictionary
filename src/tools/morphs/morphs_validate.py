import src.tools.morphs.morphs_files as file_tool

from src.tools.morphs.expression_validation import validate_expression
from src.tools.morphs.schemas.properties import properties as valid_properties
from src.tools.morphs.schemas.tags import tags as valid_tags
from src.tools.morphs.schemas.tags import tag_dependency_map as tag_dependencies
from src.tools.morphs.schemas.types import morph_types, root_types

morph_origins = [
    "latin",
    "greek",
    "old-english",
    "modern-english"
]

def validate_morph(morph):
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

    valid = True

    # Properties required by all morphs
    universal_requirements = [
        { "key": "key" },
        { "key": "type", "values": morph_types},
        { "key": "origin", "values": morph_origins }
    ]
    valid = evaluate_requirements(universal_requirements, morph) and valid

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
        valid = evaluate_requirements(type_requirements[morph["type"]], morph, morph["type"]) and valid

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
        valid = evaluate_requirements(requirements, morph, category) and valid

    # Check key whitelist
    for key in morph:
        if not key in valid_properties:
            errors.append("Invalid morph property '" + key + "' found in morph '" + morph["key"] + "'")
            valid = False

    # Check tag whitelist
    if "tags" in morph:
        for tag in morph["tags"]:
            if not tag in valid_tags:
                errors.append("Invalid morph tag '" + tag + "' found on morph '" + morph["key"] + "'")
                valid = False

    # Check tag dependencies
    # TODO: Reenable this after having a chance to revise tags
    # if "tags" in morph:
    #     for tag in morph["tags"]:
    #         if tag in tag_dependencies:
    #             for dependency in tag_dependencies[tag]:
    #                 if dependency not in morph["tags"]:
    #                     errors.append("Missing tag '" + dependency + "' required by tag '" + tag + "'")

    # Validate requirements
    if "requires" in morph:
        for referent in ["follows", "precedes"]:
            if referent in morph["requires"]:
                valid = validate_expression(morph["requires"][referent], errors) and valid

    # Validate exceptions
    if "exception" in morph:
        for exception in morph["exception"]:
            if not "case" in exception:
                errors.append("Exception missing 'case': " + str(exception))

            for referent in ["follows", "precedes"]:
                if referent in exception["case"]:
                    valid = validate_expression(exception["case"][referent], errors) and valid

    # Output
    if len(errors) > 0:
        if "key" in morph:
            print(str(len(errors)) + " errors found reading morph '" + morph["key"] + "'")
        else:
            print(str(len(errors)) + " errors found reading morph without key: " + str(morph))

        for error in errors:
            print(" - " + error)

    return valid

def validate_morphs(files):
    # Read in morphs
    morphs = []
    for file in files:
        morphs += file_tool.get_morphs_from(file)

    fail_count = 0
    for morph in morphs:
        if not validate_morph(morph):
            fail_count += 1

    if fail_count == 0:
        print("Validation succeeded")
        return 0
    else:
        print("Validation failed on " + str(fail_count) + " morphs")
        return 1
