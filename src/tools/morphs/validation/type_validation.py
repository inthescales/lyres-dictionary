from src.tools.morphs.schemas.tags import tags as valid_tags
from src.tools.morphs.schemas.properties import properties as valid_properties
from src.tools.morphs.schemas.types import morph_types as valid_morph_types

# Placeholder types =================================

# These represent different types of values that appear in the data files, which
# are used for both type and value validation.

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

# Base types that should be used when comparing the actual type of the data instance
base_types = {
    mprop: str,
    mtype: str,
    tag: str
}

# Returns the base type of the given placeholder type
def base_type(t):
    if t in base_types:
        return base_types[t]
    else:
        return t

# Container representing a value type, which may be a collection containing values of another type.
class ValueType:
    def __init__(self, maintype, subtype=None):
        self.type = maintype
        self.subtype = subtype
        self.base_type = base_type(maintype)
        self.base_subtype = base_type(subtype)

        if subtype != None:
            self.sub_as_main = ValueType(subtype)

# Validation functions =============================

# Get a name for the given type suitable for printing in error messages
def type_name(expected, plural=False):
    names = {
        str: "string",
        int: "integer",
        mprop: "property",
        mtype: "morph type",
        tag: "tag",
        list: "list",
        one_or_more: "one-or-list",
        dict: "expression dict" 
    }

    base_string = str(expected.type)
    if expected.type in names:
        base_string = names[expected.type]

    if plural:
        base_string += "s"

    if expected.type in [list, one_or_more]:
        base_string += " of " + type_name(expected.sub_as_main, plural=True)

    return base_string

# For types with restricted values, such as tags, confirms that the value is valid for that type.
def check_values(value, expected, key=None, expression=None):
    errors = []

    def check_as(t):
        return expected.type == t or (expected.type == one_or_more and expected.subtype == t and type(value) == expected.base_subtype)

    if check_as(tag) and value not in valid_tags:
        errors.append("invalid tag '" + str(value) + "' in expression: " + str(expression))

    if check_as(mtype) and value not in valid_morph_types:
        errors.append("invalid morph type '" + str(value) + "' in expression: " + str(expression))

    if check_as(mprop) and value not in valid_properties:
        errors.append("invalid morph property '" + str(value) + "' in expression: " + str(expression))

    return errors

# Checks whether the value has a type that matches the expected type, returning any errors found.
# This takes subtypes into account (e.g. expected type 'tag' matches any string that's in the valid tags list)
def type_match(value, expected, key=None, expression=None, is_member=False):
    errors = []
    
    # Check base type match
    if expected.type == one_or_more and expected.subtype != None:
        type_matches = type(value) in [list, expected.base_subtype]
    else:
        type_matches = type(value) == expected.base_type

    if not type_matches:
        if not is_member:
            errors.append("invalid value type for expression key \"" + key + "\" in expression: " + str(expression) +". Value should be " + type_name(expected) + "")
        else:
            errors.append("invalid value type for key \"" + key + "\" in expression: " + str(expression) +". List entries should be " + type_name(expected, plural=True))

    # Check matches for collection members
    if expected.type in [list, one_or_more] and type(value) == list:
        for member in value:
            errors += type_match(member, expected.sub_as_main, key, expression, True)

    # Check values for types with value restrictions
    if len(errors) == 0:
        errors += check_values(value, expected, key, expression)

    return errors
