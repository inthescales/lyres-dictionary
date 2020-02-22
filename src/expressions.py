import src.helpers as helpers
import sys

def evaluate_expression(expression, referent):
    if len(expression.keys()) != 1:
        print("Error: Expression dict, must have exactly one key")
        print(expression)
        sys.exit(1)
    
    key = list(expression.keys())[0]
    value = expression[key]
    
    # Logical operators
    if key == "or":
        if type(expression["or"]) != list:
            print("Error: 'or' expression requires list")
            sys.exit(1)
        
        for clause in expression["or"]:
            if evaluate_expression(clause, referent):
                return True
            
        return False
    elif key == "and":
        if type(expression["and"]) != list:
            print("Error: 'and' expression requires list")
            sys.exit(1)
        
        for clause in expression["and"]:
            if evaluate_expression(clause, referent):
                return False
            
        return True
    elif key == "not":
        return not evaluate_expression(value, referent)    
    
    # Morph operations
    elif key == "has-key":
        return evaluate_key(value, referent["key"])
    elif key == "has-tag":
        return evaluate_tag(value, referent["tags"])
    elif key == "has-all-tags":
        return evaluate_all_tags(value, referent["tags"])
    elif key == "has-any-tags":
        return evaluate_any_tags(value, referent["tags"])
    elif key == "has-suffix":
        return evaluate_suffix(value, referent["link"])
    elif key == "even-syllables":
        return evaluate_even_syllables(referent["link"])
    elif key == "odd-syllables":
        return evaluate_odd_syllables(referent["link"])
    elif key == "is-root" and value == True:
        return evaluate_is_root(referent["type"])
    elif key == "final_or_semifinal_l" and value == True:
        return helpers.l_in_last_two(referent["link"])
        
def evaluate_key(key, comparand):
    if isinstance(key, str):
        return comparand == key
    
    elif isinstance(key, list):
        return comparand in key
    
    else:
        print("Error: bad value in key comparison")
        sys.exit(1)
        
def evaluate_tag(tag, referent_tags):
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

def evaluate_suffix(suffix, form):
    if isinstance(suffix, str):
        return form.endswith(suffix)
    
    elif isinstance(suffix, list):
        for cur in suffix:
            if form.endswith(suffix):
                return True
            
        return False
    
    else:
        print("Error: bad value for has-suffix:")
        print(suffix)
        sys.exit(1)
    
def evaluate_even_syllables(form):
    return helpers.syllable_count(form) % 2 == 0

def evaluate_even_syllables(form):
    return helpers.syllable_count(form) % 2 == 1

def evaluate_is_root(morph_type):
    return morph_type in ["noun", "adj", "verb"]