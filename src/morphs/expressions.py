import sys

import src.utils.helpers as helpers

from src.utils.logging import Logger

def evaluate_expression(expression, referent):
    if len(expression.keys()) != 1:
        Logger.error("Expression dict, must have exactly one key")
        Logger.error(" - " + str(expression))
        sys.exit(1)
    
    key = list(expression.keys())[0]
    value = expression[key]

    # Logical operators
    if key == "or":
        if type(expression["or"]) != list:
            Logger.error("'or' expression requires list")
            sys.exit(1)
        
        for clause in expression["or"]:
            if evaluate_expression(clause, referent):
                return True
            
        return False
    elif key == "and":
        if type(expression["and"]) != list:
            Logger.error("'and' expression requires list")
            sys.exit(1)
        
        for clause in expression["and"]:
            if not evaluate_expression(clause, referent):
                return False
            
        return True
    elif key == "not":
        return not evaluate_expression(value, referent)    
    
    # Morph operations
    elif key == "has-property":
        return value in referent
    elif key == "has-key":
        return evaluate_key(value, referent["key"])
    elif key == "has-type":
        type_ = referent["type"]
        if referent["type"] == "suffix":
            type_ = referent["derive-to"]
        return evaluate_type(value, type_)
    elif key == "has-tag":
        if "tags" not in referent:
            return False
        return evaluate_tag(value, referent["tags"])
    elif key == "has-all-tags":
        if "tags" not in referent:
            return False
        return evaluate_all_tags(value, referent["tags"])
    elif key == "has-any-tags":
        if "tags" not in referent:
            return False
        return evaluate_any_tags(value, referent["tags"])
    elif key == "has-prefix":
        return evaluate_prefix(value, referent["form"])
    elif key == "has-suffix":
        return evaluate_suffix(value, referent["form"])
    elif key == "has-suffix-template":
        return evaluate_suffix_template(value, referent["form"])
    elif key == "has-conjugation":
        return evaluate_conjugation(value, referent["conjugation"])
    elif key == "has-declension":
        return evaluate_declension(value, referent["declension"])
    elif key == "syllable-count":
        return evaluate_syllable_count(referent["form"]) == value
    elif key == "is-root":
        return evaluate_is_root(referent["type"]) == value
    elif key == "is-final":
        return referent["form-final"] == value
    elif key == "final-or-semifinal-l":
        return helpers.l_in_last_two(referent["form"]) == value
    else:
        Logger.error("unrecognized expression operator: '" + key + "'")
        
def evaluate_key(key, comparand):
    if isinstance(key, str):
        return comparand == key
    
    elif isinstance(key, list):
        return comparand in key
    
    else:
        Logger.error("bad value in key comparison: '" + str(key) + "'")
        sys.exit(1)
        
def evaluate_type(type_, comparand):
    if isinstance(type_, str):
        return comparand == type_
    
    elif isinstance(type_, list):
        return comparand in type_
    
    else:
        Logger.error("bad value in type comparison: '" + type_ + "'")
        sys.exit(1)
        
def evaluate_tag(tag, referent_tags):
    if not isinstance(tag, str):
        print("IT IS: " + str(tag))
        Logger.error("tag must be string")
        sys.exit(1)
        
    return tag in referent_tags
        
def evaluate_all_tags(tags, referent_tags):
    for tag in tags:
        if not tag in referent_tags:
            return False
    
    return True

def evaluate_any_tags(tags, referent_tags):
    for tag in tags:
        if tag in referent_tags:
            return True
    
    return False

def evaluate_prefix(prefix, form):
    if isinstance(prefix, str):
        return form.startswith(prefix)
    
    elif isinstance(prefix, list):
        for cur in prefix:
            if form.startswith(cur):
                return True
        
        return False
    
    else:
        Logger.error("bad value for has-prefix:")
        Logger.error(" - " + str(prefix))
        sys.exit(1)

def evaluate_suffix(suffix, form):
    if isinstance(suffix, str):
        return form.endswith(suffix)
    
    elif isinstance(suffix, list):
        for cur in suffix:
            if form.endswith(cur):
                return True
        
        return False
    
    else:
        Logger.error("bad value for has-suffix:")
        Logger.error(" - " + str(suffix))
        sys.exit(1)

# Template format:
# - lowercase letters match that letter
# - V matches all vowels
# - C matches all consonants
#   - A heuristic determines whether 'y' counts as C or V
def evaluate_suffix_template(template, form):
    def matches(char, template, prev):
        if char == template:
            return True

        y_is_consonant = not helpers.y_is_vowel_heuristic(prev)
        if helpers.is_consonant(char, y_is_consonant) and template == "C":
            return True
        elif helpers.is_vowel(char, not y_is_consonant) and template == "V":
            return True

        return False

    templates = None
    if isinstance(template, list):
        templates = template
    elif isinstance(template, str):
        templates = [template]

    if templates != None:
        for template in templates:
            if len(form) < len(template):
                continue

            for i in range(0, len(template)):
                if i + 1 < len(template):
                    prev = template[-(i+2)]
                else:
                    prev = None

                if not matches(form[-i-1], template[-i-1], prev):
                    break

                if i == len(template) - 1:
                    return True

        return False
    
    else:
        Logger.error("bad value for has-suffix-template:")
        Logger.error(" - " + str(suffix))
        sys.exit(1)
        
def evaluate_conjugation(acceptable, conjugation):
    if conjugation is None:
        Logger.error("referent lacks conjugation")
        sys.exit(1)
        
    if isinstance(acceptable, int):
        return conjugation == acceptable
    
    elif isinstance(acceptable, list):
        return conjugation in acceptable
    
    else:
        Logger.error("Bad value for has-conjugation")
        sys.exit(1)

def evaluate_declension(acceptable, declension):
    if declension is None:
        Logger.error("referent lacks declension")
        sys.exit(1)
        
    if isinstance(acceptable, int):
        return declension == acceptable
    
    elif isinstance(acceptable, list):
        return declension in acceptable
    
    else:
        Logger.error("bad value for has-declension")
        sys.exit(1)
    
def evaluate_syllable_count(form):
    return helpers.syllable_count_smart(form)

def evaluate_is_root(morph_type):
    return morph_type in ["noun", "adj", "verb"]
