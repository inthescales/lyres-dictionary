from src.tools.morphs.type_validation import type_match, print_name, one_or_more

from src.tools.morphs.schemas.expression_keys import expression_value_types
from src.tools.morphs.schemas.expression_keys import expression_keys as valid_expression_keys


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

        # Recurse on sub-expressions
        if type(value) == dict:
            valid = validate_expression(value, errors) and valid
        elif type(value) == list:
            for subvalue in value:
                if type(subvalue) == dict:
                    valid = validate_expression(subvalue, errors) and valid

    return valid
