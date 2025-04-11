from src.tools.morphs.schemas.tags import tags as valid_tags
from src.tools.morphs.schemas.properties import properties as valid_properties
from src.tools.morphs.schemas.types import morph_types

# May be a single value, or a list of values
class one_or_more:
    def __init__(self):
        return

# A string which is a valid tag
class tag:
    def __init__(self):
        return

# A string which is a valid morph type (e.g. noun, verb)
class mtype:
    def __init__(self):
        return

# A string which is a valid morph property
class mprop:
    def __init__(self):
        return

base_types = {
    mprop: str,
    mtype: str,
    tag: str
}

# Returns the base type of the given type.
# This is the type that will be actually compared to the value's type
def base_type(t):
    if t in base_types:
        return base_types[t]
    else:
        return t

# Get a name for the given type suitable for printing in error messages
# Types are in the schema format: [type] for simple types, [type, element-type] for collections
def type_name(expected_type, expected_subtype=None, plural=False):
    names = {
        str: "string",
        int: "integer",
        mtype: "morph type",
        tag: "tag",
        list: "list",
        one_or_more: "one-or-list",
        dict: "expression dict" 
    }

    base_string = str(expected_type)
    if expected_type in names:
        base_string = names[expected_type]

    if plural:
        base_string += "s"

    if expected_type in [list, one_or_more]:
        base_string += " of " + type_name(expected_subtype, plural=True)

    return base_string

# Checks whether the value has a type that matches the expected type, returning
# a list of any errors found.
# This takes subtypes into account (e.g. expected type 'tag' matches any string
# that's in the valid tags list)
def type_match(value, expected, subexpected=None, key=None, expression=None, is_member=False):
    errors = []
    
    # Check base type match
    if expected == one_or_more and subexpected != None:
        type_matches = type(value) in [list, base_type(subexpected)]
    else:
        type_matches = type(value) == base_type(expected)

    if not type_matches:
        if not is_member:
            errors.append("invalid value type for expression key \"" + key + "\" in expression: " + str(expression) +". Value should be " + type_name(expected, subexpected) + "")
        else:
            errors.append("invalid value type for key \"" + key + "\" in expression: " + str(expression) +". List entries should be " + type_name(subexpected, plural=True))

    # Check matches for collection members
    if expected in [list, one_or_more] and type(value) == list:
        for member in value:
            errors += type_match(member, subexpected, None, key, expression, True)

    # Check semantic strings
    def check_as(t):
        return expected == t or (expected == one_or_more and subexpected == t and type(value) == base_type(subexpected))

    if check_as(tag) and value not in valid_tags:
        errors.append("invalid tag '" + str(value) + "' in expression: " + str(expression))

    if check_as(mtype) and value not in morph_types:
        errors.append("invalid morph type '" + str(value) + "' in expression: " + str(expression))

    if check_as(mprop) and value not in valid_properties:
        errors.append("invalid morph property '" + str(value) + "' in expression: " + str(expression))

    return errors
