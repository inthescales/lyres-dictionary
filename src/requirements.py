import random

from src.expressions import evaluate_expression
from src.logging import Logger

# Check whether a morph meets the requirements to be added in a given location
def meets_requirements(morph, env, filter_frequency=True):
    return meets_universal_requirements(morph, env) \
           and meets_morph_requirements(morph, env) \
           and (not filter_frequency or frequency_filter(morph))
        
# Check placement requirements not belonging to an individual morph
def meets_universal_requirements(morph, env):
    morph_dict = morph.morph

    # The same morph should never appear twice in a row
    if (env.prev and env.prev.get_key() == morph.get_key()) \
        or (env.next and env.next.get_key() == morph.get_key()):
        return False

    # Can't put a suffix on a verb if that verb doesn't have the required participle type
    if "derive-participle" in morph_dict:
        link_key = "form-stem-" + morph_dict["derive-participle"]
        if not (link_key in env.prev.morph or "form-stem" in env.prev.morph):
            return False

    # Can't use an object-specifying affix if the verb has already specified its object.
    if morph.has_tag("object-specifier") and env.object_specified:
        return False

    return True

# Check the particular requirements belonging to a morph and its neighbors
def meets_morph_requirements(morph, env):
    morph_dict = morph.morph

    # No requirements to check, it's ok
    if not "requires" in morph_dict:
        return True
    
    requirements = morph_dict["requires"]
    keys = requirements.keys()
    if len(keys) != 1:
        Logger.error("currently, requirement can only have one referent child")
        sys.exit(1)
        
    if "precedes" in keys:
        if env.next == None:
            Logger.error("precedes block but no following morph given")
            sys.exit(1)
        
        if not evaluate_expression(requirements["precedes"], env.next.as_dict(env.next_env(morph))):
            return False
    
    if "follows" in keys:
        if env.prev == None:
            Logger.error("follows block but no following morph given")
            sys.exit(1)

        if not evaluate_expression(requirements["follows"], env.prev.as_dict(env.prev_env(morph))):
            return False
    
    return True

# Randomly filter out morphs with less than 100% frequency
def frequency_filter(morph):
    frequency = morph.frequency()
    if frequency < 100 and random.randint(1, 100) > frequency:
        return False

    return True