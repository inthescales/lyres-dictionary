import src.tools.morphs.morphs_files as file_tool

from src.tools.morphs.validation.expression_validation import validate_expressions
from src.tools.morphs.validation.property_validation import validate_properties
from src.utils.terminal import Color, color_text

from src.tools.morphs.schemas.tags import tags as valid_tags

# Validate a single morph
def validate_morph(morph):
    errors = []

    # Validate properties
    errors += validate_properties(morph)

    # Validate expressions
    errors += validate_expressions(morph)

    # Check tag whitelist
    if "tags" in morph:
        for tag in morph["tags"]:
            if not tag in valid_tags:
                errors.append("Invalid morph tag '" + str(tag) + "' found on morph '" + morph["key"] + "'")

    # Check tag dependencies
    # TODO: Reenable this after having a chance to revise tags

    # from src.tools.morphs.schemas.tags import tag_dependency_map as tag_dependencies
    
    # if "tags" in morph:
    #     for tag in morph["tags"]:
    #         if tag in tag_dependencies:
    #             for dependency in tag_dependencies[tag]:
    #                 if dependency not in morph["tags"]:
    #                     errors.append("Missing tag '" + dependency + "' required by tag '" + tag + "'")

    # Output
    if len(errors) > 0:
        if "key" in morph:
            print(str(len(errors)) + " errors found reading morph '" + morph["key"] + "'")
        else:
            print(str(len(errors)) + " errors found reading morph without key: " + str(morph))

        for error in errors:
            print(" - " + error)

    return len(errors) == 0

# Validate all morphs from the given files
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
        print(color_text(Color.green, "Validation succeeded"))
        return 0
    else:
        print(color_text(Color.red, "Validation failed on " + str(fail_count) + " morphs"))
        return 1
