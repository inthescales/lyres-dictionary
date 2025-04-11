from src.tools.morphs.type_validation import type_match, type_name, one_or_more

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

        # Call type validation
        type_schema = expression_value_types[key]
        expected_type = type_schema[0]
        expected_subtype = None
        if len(type_schema) > 1:
            expected_subtype = type_schema[1]

        type_errors = type_match(value, expected_type, expected_subtype, key, expression)
        valid = (len(type_errors) == 0) and valid
        errors += type_errors

        # Recurse on sub-expressions
        if type(value) == dict:
            valid = validate_expression(value, errors) and valid
        elif type(value) == list:
            for subvalue in value:
                if type(subvalue) == dict:
                    valid = validate_expression(subvalue, errors) and valid

    return valid
