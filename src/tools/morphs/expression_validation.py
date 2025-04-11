from src.tools.morphs.schemas.expression_keys import tag, mtype, one_or_more, expression_value_types
from src.tools.morphs.schemas.expression_keys import expression_keys as valid_expression_keys
from src.tools.morphs.schemas.tags import tags as valid_tags
from src.tools.morphs.schemas.types import morph_types

# Get a name for the given type suitable for printing in error messages
# Types are in the schema format: [type] for simple types, [type, element-type] for collections
def print_name(t, plural=False):
    overrides = { str: "string", int: "integer", tag: "tag", list: "list", one_or_more: "one-or-list", dict: "expression dict" }
    base_string = str(t[0])
    if t[0] in overrides:
        base_string = overrides[t[0]]

    if plural:
        base_string += "s"

    if t[0] in [list, one_or_more]:
        base_string += " of " + print_name([t[1]], plural=True)

    return base_string

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

# Validate the structure and value types of an expression (as in morph requirements and exceptions)
def validate_expression(expression, errors):
    valid = True

    # Check that each expression contains only one key
    if len(expression.items()) > 1:
        errors.append("expressions may only have one key, but found key " + str(len(expression.items())) + ": " + str(expression))
        valid = False

    for key, value in expression.items():
        # Check that only valid keys appear
        if key not in valid_expression_keys:
            errors.append("invalid expression key \"" + key + "\" in expression: " + str(expression))
            valid = False

        # valid = type_match(value, expression_value_types[key], key, expression, errors)

        expected_type = expression_value_types[key]
        if not type_match(value, expected_type[0], errors) \
            and not (expected_type[0] == one_or_more and (type(value) == list or type_match(value, expected_type[1], errors))):
            errors.append("invalid value type for expression key \"" + key + "\" in expression: " + str(expression) +". Value should be " + print_name(expected_type) + "")
            valid = False        

        if expected_type[0] in [list, one_or_more] and type(value) == list:
            for list_value in value:
                if not type_match(list_value, expected_type[1], errors):
                    errors.append("invalid expression value for key \"" + key + "\" in expression: " + str(expression) +". List entries should be " + print_name([expected_type[1]], plural=True))
                    valid = False

        # Check the top-level value type
        # value_type = expression_value_types[key]
        # if type(value) != value_type[0] \
        #     and not (value_type[0] == one_or_more and type(value) in [list, value_type[1]]):
        #     errors.append("invalid value type for expression key \"" + key + "\" in expression: " + str(expression) +". Value should be " + print_name(value_type) + "")
        #     valid = False

        # Check the types of list members
        # if value_type[0] in [list, one_or_more] and type(value) == list:
        #     subvalue_type = value_type[1]
        #     for list_value in value:
        #         if type(list_value) != subvalue_type:
        #             errors.append("invalid expression value for key \"" + key + "\" in expression: " + str(expression) +". List entries should be " + print_name([value_type[1]], plural=True))
        #             valid = False

        # Recurse on sub-expressions
        if type(value) == dict:
            valid = validate_expression(value, errors) and valid
        elif type(value) == list:
            for subvalue in value:
                if type(subvalue) == dict:
                    valid = validate_expression(subvalue, errors) and valid

    return valid
