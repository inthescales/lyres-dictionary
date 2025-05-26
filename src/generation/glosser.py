import src.utils.helpers as helpers
import src.utils.inflection as inflection

# Get a morph's gloss based on its environment
def gloss(morph, env):
    morph_dict = morph.morph

    # Check for special 'gloss-relative' glosses where prepositions are involved
    if env.prev \
        and ( \
            (env.prev.get_type() == "noun" and env.anteprev and env.anteprev.get_type() == "prep" ) \
            or (morph.get_type() == "verb" and env.prev.get_type() == "prep") \
        ) \
        and "gloss-relative" in morph_dict:
        if morph.get_type() == "verb" and len(morph_dict["gloss-relative"].split(" ")) == 1:
            return "[" + morph_dict["gloss-relative"] + "]"
        else:
            return morph_dict["gloss-relative"]
    
    # Check for a basic gloss
    if "gloss" in morph_dict:
        gloss = helpers.one_or_random(morph_dict["gloss"], seed=morph.seed)
        if morph_dict["type"] in ["noun", "verb"] and len(gloss.split(" ")) == 1:
            return "[" + gloss + "]"
        else:
            return gloss
        
    else:
        # Use special linking or final glosses if present
        if env.next:
            if "gloss-link" in morph_dict:
                return morph_dict["gloss-link"]
        else:
            if "gloss-final" in morph_dict:
                return morph_dict["gloss-final"]
        
        # Use special gloss based on the type of a neighbor
        if morph.get_type() == "prep" or morph.get_type() == "prefix":
            relative = env.next
        else:
            relative = env.prev
        
        if relative and "gloss-" + relative.get_type() in morph_dict:
            return morph_dict["gloss-" + relative.get_type()]
    
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