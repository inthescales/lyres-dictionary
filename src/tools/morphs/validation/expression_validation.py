from src.tools.morphs.validation.type_validation import Meta, schemata

# Validate the structure and value types of an expression (as in morph requirements and exceptions)
def validate_expression(expression):
    errors = []

    meta = Meta("root", expression, schemata)
    return schemata["expression"].get_errors(expression, meta)
