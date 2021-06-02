import sys
import src.helpers as helpers

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
            if not evaluate_expression(clause, referent):
                return False
            
        return True
    elif key == "not":
        return not evaluate_expression(value, referent)    
    
    # Morph operations
    elif key == "has-key":
        return evaluate_key(value, referent["key"])
    elif key == "has-type":
        type_ = referent["type"]
        if referent["type"] == "derive":
            type_ = referent["to"]
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
    elif key == "has-conjugation":
        return evaluate_conjugation(value, referent["conjugation"])
    elif key == "has-declension":
        return evaluate_declension(value, referent["declension"])
    elif key == "even-syllables":
        return evaluate_even_syllables(referent["form"])
    elif key == "odd-syllables":
        return evaluate_odd_syllables(referent["form"])
    elif key == "is-root" and value == True:
        return evaluate_is_root(referent["type"])
    elif key == "is-final" and value == True:
        return referent["final"] == True
    elif key == "final_or_semifinal_l" and value == True:
        return helpers.l_in_last_two(referent["form"])
        
def evaluate_key(key, comparand):
    if isinstance(key, str):
        return comparand == key
    
    elif isinstance(key, list):
        return comparand in key
    
    else:
        print("Error: bad value in key comparison")
        sys.exit(1)
        
def evaluate_type(type_, comparand):
    if isinstance(type_, str):
        return comparand == type_
    
    elif isinstance(type_, list):
        return comparand in type_
    
    else:
        print("Error: bad value in type comparison")
        sys.exit(1)
        
def evaluate_tag(tag, referent_tags):
    if not isinstance(tag, str):
        print ("Error: tag must be string")
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
        print("Error: bad value for has-prefix:")
        print(prefix)
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
        print("Error: bad value for has-suffix:")
        print(suffix)
        sys.exit(1)
        
def evaluate_conjugation(acceptable, conjugation):
    if conjugation is None:
        print("Error: referent lacks conjugation")
        sys.exit(1)
        
    if isinstance(acceptable, int):
        return conjugation == acceptable
    
    elif isinstance(acceptable, list):
        return conjugation in acceptable
    
    else:
        print("Error: Bad value for has-conjugation")
        sys.exit(1)

def evaluate_declension(acceptable, declension):
    if declension is None:
        print("Error: referent lacks declension")
        sys.exit(1)
        
    if isinstance(acceptable, int):
        return declension == acceptable
    
    elif isinstance(acceptable, list):
        return declension in acceptable
    
    else:
        print("Error: Bad value for has-declension")
        sys.exit(1)
    
def evaluate_even_syllables(form):
    return helpers.syllable_count(form) % 2 == 0

def evaluate_even_syllables(form):
    return helpers.syllable_count(form) % 2 == 1

def evaluate_is_root(morph_type):
    return morph_type in ["noun", "adj", "verb"]