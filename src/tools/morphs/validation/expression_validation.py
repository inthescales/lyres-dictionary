from src.tools.morphs.validation.type_validation import Meta, schemata

# Validate the structure and value types of an expression (as in morph requirements and exceptions)
def validate_expression(expression):
    errors = []

    meta = Meta(" in expression " + str(expression), schemata)
    errors = schemata["expression"].get_errors(expression, meta)
    return [err.text for err in errors]
