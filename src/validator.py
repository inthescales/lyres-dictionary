import re
import sys

from src.logging import Logger

def validate(entry):
    return validate_length(entry) and validate_decent(entry)
    
def validate_length(entry):
    if len(entry) <= 280:
        return True
    else:
        validator_error(entry, "too long")
        return False

def validate_decent(entry):
    patterns = [
        ".*nig+[aeiou]r",
        ".*nig+[ae][h\W$]+",
        ".*tard"
    ]
    for pattern in patterns:
        regex = re.compile(pattern)
        result = regex.match(entry)
        if result != None:
            validator_error(entry, "indecent")
            return False
        
    return True

def validator_error(entry, reason):
    Logger.trace("validator flagged entry as " + reason + ":")
    Logger.trace(" - " + str(entry))
    return
