import re
import sys

from src.utils.logging import Logger

# Returns whether the entry passes validation and can be posted.
def validate(entry):
    return validate_length(entry) and validate_decent(entry)

# Returns whether the entry is of an acceptable length    
def validate_length(entry):
    if len(entry) <= 280:
        return True
    else:
        validator_error(entry, "too long")
        return False

# Returns whether the entry contains a word I don't want it to use, or
# something too similar to that.
def validate_decent(entry):
    patterns = [
        r".*nig+[aeiou]r",
        r".*nig+[ae][h\W$]+",
        r".*tard"
    ]
    for pattern in patterns:
        regex = re.compile(pattern)
        result = regex.match(entry)
        if result != None:
            validator_error(entry, "indecent")
            return False
        
    return True

# Return a validation error
def validator_error(entry, reason):
    Logger.trace("validator flagged entry as " + reason + ":")
    Logger.trace(" - " + str(entry))
    return
