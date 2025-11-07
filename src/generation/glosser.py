import src.utils.helpers as helpers
import src.utils.inflection as inflection

# Get a morph's gloss based on its environment
def gloss(morph, env):
    morph_dict = morph.sense.dict

    gloss = None

    # Check for special 'gloss-relative' glosses where prepositions are involved
    if env.prev \
        and ( \
            (env.prev.get_type() == "noun" and env.anteprev and env.anteprev.get_type() == "prep" ) \
            or (morph.get_type() == "verb" and env.prev.get_type() == "prep") \
        ) \
        and "gloss-relative" in morph_dict:
        gloss = morph_dict["gloss-relative"]
    
    # Check for a basic gloss
    elif "gloss" in morph_dict:
        gloss = morph_dict["gloss"]

    # Use linking gloss if this morph if not the last
    elif env.next and "gloss-link" in morph_dict:
        gloss = morph_dict["gloss-link"]

    # Use final gloss if this morph is the last
    elif not env.next and "gloss-final" in morph_dict:
        gloss = morph_dict["gloss-final"]

    # Use special gloss based on the type of a neighbor
    else:
        if morph.get_type() == "prep" or morph.get_type() == "prefix":
            relative = env.next
        else:
            relative = env.prev
        
        if relative and "gloss-" + relative.get_type() in morph_dict:
            gloss =morph_dict["gloss-" + relative.get_type()]

    # If the gloss is a list, choose one at random
    gloss = helpers.one_or_random(gloss, seed=morph.seed)

    if gloss != None:
        # If the gloss is a single word, and won't be substituted, bracket it as the target
        # of future inflections.
        if len(gloss.split(" ")) == 1 and gloss[0] not in ["%", "&"]:
            gloss = "[" + gloss + "]"

        return gloss

    Logger.error("failed to find gloss for " + morph_dict["key"] + ", joining to " + relative.get_key())

# Inflect the words in a gloss as indicated
def inflect_gloss(gloss, mode):
    words = gloss.split(" ")
    for i, word in enumerate(words):
        final_punctuation = None

        # Strip punctuation
        if word[0] == "[" \
            and (
                word[-1] == "]"
                or (word[-1] in [",", ";"] and word[-2] == "]")
            ):
            if word[-1] != "]":
                final_punctuation = word[-1]
                word = word[0:-1]

            word = word[1:-1]
        elif len(words) > 1:
            continue

        words[i] = inflection.inflect(word, mode)

        # Add back stripped final punctuation
        if final_punctuation:
            words[i] += final_punctuation

    return " ".join(words)