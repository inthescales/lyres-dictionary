from src.tools.morphs.schemas.expression_keys import expression_value_types
from src.tools.morphs.validation.type_validation import type_match

from src.tools.morphs.schemas.expression_keys import expression_keys as valid_expression_keys

# Validate the structure and value types of an expression (as in morph requirements and exceptions)
def validate_expression(expression):
    errors = []

    # Check that each expression contains only one key
    if len(expression.items()) > 1:
        errors.append("expressions may only have one key, but found key " + str(len(expression.items())) + ": " + str(expression))

    for key, value in expression.items():
        # Check that only valid keys appear
        if key not in valid_expression_keys:
            errors.append("invalid expression key \"" + key + "\" in expression: " + str(expression))

        # Call type validation
        type_errors = type_match(value, expression_value_types[key], key, expression)
        errors += type_errors

        # Recurse on sub-expressions
        if type(value) == dict:
            errors += validate_expression(value)
        elif type(value) == list:
            for subvalue in value:
                if type(subvalue) == dict:
                    errors += validate_expression(subvalue)

    return errors
