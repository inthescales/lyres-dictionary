from src.tools.morphs.schemas.tags import tags as valid_tags
from src.tools.morphs.schemas.types import morph_types

class one_or_more:
    def __init__(self):
        return

class tag:
    def __init__(self):
        return

class mtype:
    def __init__(self):
        return

# Get a name for the given type suitable for printing in error messages
# Types are in the schema format: [type] for simple types, [type, element-type] for collections
def print_name(t, plural=False):
    names = {
        str: "string",
        int: "integer",
        mtype: "morph type",
        tag: "tag",
        list: "list",
        one_or_more: "one-or-list",
        dict: "expression dict" 
    }

    base_string = str(t[0])
    if t[0] in names:
        base_string = names[t[0]]

    if plural:
        base_string += "s"

    if t[0] in [list, one_or_more]:
        base_string += " of " + print_name([t[1]], plural=True)

    return base_string

# Returns true if the value has a type that matches the expected type.
# This takes subtypes into account (e.g. expected type 'tag' matches any string
# that's in the valid tags list)
def type_match(value, expected, errors):
    valid = True

    def base_type(t):
        base_types = { mtype: str, tag: str}
        if t in base_types:
            return base_types[t]
        else:
            return t

    value_type = expected
    base_value_type = base_type(value_type)
    valid = type(value) == base_value_type

    if expected == tag and value not in valid_tags:
        valid = False

    if expected == mtype and value not in morph_types:
        valid = False

    return valid
