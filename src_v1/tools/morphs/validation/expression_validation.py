from src.tools.morphs.validation.type_validation import Any, Array, Bool, Dict, Integer, Meta, Opt, One_Or_More, Schema, String, ValueSets

                                      # ARGUMENT TYPE                        EVALUATION RESULT
expression_schema = Any([
        Dict({"or":                   Array(Schema("expression"))}),         # true if any expression in list evaluates true
        Dict({"and":                  Array(Schema("expression"))}),         # true if all expressions in list evaluate true
        Dict({"not":                  Schema("expression")}),                # true if the expression evaluates false
        Dict({"has-key":              One_Or_More(String())}),               # true if the morph's key matches the given string, or is in the list
        Dict({"has-type":             One_Or_More(String(ValueSets.lex_class))}), # true if the morph's type is equal to the string, or is in the list
        Dict({"has-property":         String(ValueSets.prop)}),              # true if the morph contains a value for the given property
        Dict({"has-tag":              String(ValueSets.tag)}),               # true if the morph contains the given tag
        Dict({"has-all-tags":         Array(String(ValueSets.tag))}),        # true if the morph contains all of the given tags
        Dict({"has-any-tags":         Array(String(ValueSets.tag))}),        # true if the morph contains any of the given tags
        Dict({"has-prefix":           One_Or_More(String())}),               # true if the morph's form begins with the given string, or any in a given list
        Dict({"has-suffix":           One_Or_More(String())}),               # true if the morph's form ends with the given string, or any in a given list
        Dict({"has-suffix-template":  One_Or_More(String())}),               # true if the morph's form's ending matches the given string template, or any in a given list
                                                                             #   - C: matches any consonant
                                                                             #   - V: matches any vowel
                                                                             #   - other characters match as literals
        Dict({"has-conjugation":      One_Or_More(Integer())}),              # true if the morph has a conjugation equal to the given integer
        Dict({"has-declension":       One_Or_More(Integer())}),              # true if the morph has a declension equal to the given integer
        Dict({"syllable-count":       Integer()}),                           # true if the morph
        Dict({"is-root":              Bool()}),                              # true if the morph's type is a root type
        Dict({"is-final":             Bool()}),                              # true if no morphs follow this morph
        Dict({"final-or-semifinal-l": Bool()})                               # true if there is an l in the last two syllables
    ]
)

expression_specifier = Dict({ "follows": Opt(expression_schema), "precedes": Opt(expression_schema) })

morph_expressions = Dict({
        "requires": Opt(expression_specifier),
        "exception": Opt(Array(Dict({ "case": expression_specifier }, restrict=False)))
    }
    , restrict=False
)

def validate_expressions(morph):
    errors = []

    schemata = { "expression": expression_schema }
    meta = Meta(" in morph", schemata)
    errors = morph_expressions.get_errors(morph, meta)

    return [err.text for err in errors]
