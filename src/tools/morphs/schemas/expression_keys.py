from src.tools.morphs.type_validation import one_or_more, tag, mtype

                                # ARGUMENT TYPE             EVALUATION RESULT
expression_schema = [
    ["or",                      [list, dict]],              # true if any expression in list evaluates true
    ["and",                     [list, dict]],              # true if all expressions in list evaluate true
    ["not",                     [dict]],                    # true if the expression evaluates false
    ["has-key",                 [one_or_more, str]],        # true if the morph's key matches the given string, or is in the list
    ["has-type",                [one_or_more, mtype]],        # true if the morph's type is equal to the string, or is in the list
    ["has-property",            [str]],                     # true if the morph contains a value for the given property
    ["has-tag",                 [tag]],                     # true if the morph contains the given tag
    ["has-all-tags",            [list, tag]],               # true if the morph contains all of the given tags
    ["has-any-tags",            [list, tag]],               # true if the morph contains any of the given tags
    ["has-prefix",              [one_or_more, str]],        # true if the morph's form begins with the given string, or any in a given list
    ["has-suffix",              [one_or_more, str]],        # true if the morph's form ends with the given string, or any in a given list
    ["has-suffix-template",     [one_or_more, str]],        # true if the morph's form's ending matches the given string template, or any in a given list
                                                            #   - C: matches any consonant
                                                            #   - V: matches any vowel
                                                            #   - other characters match as literals
    ["has-conjugation",         [one_or_more, int]],        # true if the morph has a conjugation equal to the given integer
    ["has-declension",          [one_or_more, int]],        # true if the morph has a declension equal to the given integer
    ["syllable-count",          [int]],                     # true if the morph
    ["is-root",                 [bool]],                    # true if the morph's type is a root type
    ["is-final",                [bool]],                    # true if no morphs follow this morph
    ["final-or-semifinal-l",    [bool]]                     # true if there is an l in the last two syllables
]

expression_keys = [x[0] for x in expression_schema]
expression_value_types = {}
for entry in expression_schema:
    expression_value_types[entry[0]] = entry[1]
