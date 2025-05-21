from random import Random

import src.models
import src.generation.former as former
import src.utils.helpers as helpers
import src.utils.inflection as inflection

import src.language.latin.joining as lat_join
import src.language.greek.joining as grk_join
import src.language.modern_english.joining as mne_join

from src.generation.former import Former_Config

from src.utils.logging import Logger

# TODO: Move this to an Entry model, which would be populated in entry.py?
def entry(word):
    composed = get_form(word)
    tag = get_part_tag(word)
    definition = get_definition(word)
    entry = composed + " " + tag + "\n" + definition
    return entry

def get_part_tag(word):
    pos = word.get_type()

    if pos == "noun" or pos == "number":
        abbrev = "n"
    elif pos == "adj":
        abbrev = "adj"
    elif pos == "verb":
        abbrev = "v"
    elif pos == "prep":
        abbrev = "prep"
    else:
        abbrev = "???"
        Logger.error("Unknown word type")

    return "(" + abbrev + ")"

def get_form(word, former_config=None):
    form = ""
    
    for index, morph in enumerate(word.morphs):

        env = word.environment_for_index(index)
        random = Random(morph.seed)
        if former_config == None and morph.has_tag("obscure") and random.choice([True, False]):
            former_config = Former_Config(random.choice([True, False]), False)

        if former_config != None:
            addition = former.form(morph, env, former_config)
        else:
            addition = former.form(morph, env)
        
        # Handle joining rules
        if len(addition) > 0:
            if index > 0:
                last_morph = word.morphs[index-1]
            else:
                last_morph = None

            # Apply joining rules
            # If this word is a compound, apply them only to the final chunk
            if "-" not in form:
                form = get_joined_form(word.get_origin(), last_morph, morph, form, addition)
            else:
                # Handles cases like "three-starred", where treating 'three-star' as a single unit throws off the syllable count
                # TODO: Handle cases of compounds other than those separated by dashes, such as compound morphs
                chunks = form.split("-")
                form = "-".join(chunks[:-1]) + "-" + get_joined_form(word.get_origin(), last_morph, morph, chunks[-1], addition)

    return form
    
def get_definition(word):
    morph = None
    
    prefix_stack = []

    def pop_prefix(last_morph, definition):

        top, env = prefix_stack.pop()

        return build_def(top, last_morph, env, definition)

    def build_def(morph, last_morph, env, definition):
        part = former.gloss(morph, env)

        if last_morph is None:
            definition = part
            
            # Adjectives don't get inflected, so proactively strip their brackets
            if morph.is_root() and morph.get_type() == "adj":
                definition = definition.replace("[","").replace("]", "")
        else:
            words = part.split(" ")
            for (index, word) in enumerate(words):
                bracketed = False
                if word[0] == "[" and word[-1] == "]" and word[1] == "%":
                    # Substitution points may be bracketed – preserve existing brackets
                    bracketed = True
                    word = word[1:-1]

                if word == "%@":
                    words[index] = definition
                elif word == "%part":
                    words[index] = inflection.inflect(definition, "part")
                elif word == "%ppart":
                    words[index] = inflection.inflect(definition, "ppart")
                elif word == "%3sg":
                    words[index] = inflection.inflect(definition, "3sg")
                elif word == "%inf":
                    words[index] = inflection.inflect("to " + definition, "inf")
                elif word == "%sg":
                    if last_morph.has_tag("count"):
                        inflected = inflection.inflect(definition, "sg")
                        article = helpers.indefinite_article_for(inflected)
                        words[index] = article + " " + inflected
                    elif last_morph.has_tag("mass") or last_morph.has_tag("uncountable"):
                        words[index] = inflection.inflect(definition, "mass")
                    elif last_morph.has_tag("singleton"):
                        article = "the"
                        words[index] = article + " " +inflection.inflect(definition, "singleton")
                    else:
                        words[index] = definition
                elif word == "%!sg":
                    if last_morph.has_tag("count"):
                        words[index] = inflection.inflect(definition, "sg")
                    elif last_morph.has_tag("mass"):
                        words[index] = inflection.inflect(definition, "mass")
                    elif last_morph.has_tag("singleton"):
                        words[index] = inflection.inflect(definition, "singleton")
                    else:
                        words[index] = definition
                elif word == "%pl":
                    if last_morph.has_tag("count"):
                        words[index] = inflection.inflect(definition, "pl")
                    elif last_morph.has_tag("mass") or last_morph.has_tag("uncountable"):
                        words[index] = inflection.inflect(definition, "mass")
                    elif last_morph.has_tag("singleton"):
                        article = "the"
                        words[index] = article + " " +inflection.inflect(definition, "singleton")
                    else:
                        words[index] = definition
                elif word == "%!pl":
                    words[index] = inflection.inflect(definition, "pl")
                elif "%(" in word and ")" in word:
                    open_index = word.index("%(")
                    close_index = word.index(")")

                    head = word[:open_index]
                    ref_property = word[open_index + 2:close_index]
                    tail = word[close_index + 1:]

                    if ref_property in last_morph.morph:
                        # Choose one at random if list
                        if isinstance(last_morph.morph[ref_property], list):
                            random = Random(morph.seed)
                            value = random.choice(last_morph.morph[ref_property])
                        else:
                            value = last_morph.morph[ref_property]

                        # If this is a kind of gloss, and is a single word, add brackets
                        if ref_property.startswith("gloss") and not " " in value and morph.get_type() in ["noun", "verb"]:
                            value = "[" + value + "]"

                        words[index] = head + value + tail
                    else:
                        Logger.error("referred to missing property '" + ref_property + "' in morph " + last_morph.morph["key"])

                if bracketed:
                    words[index] = "[" + words[index] + "]"


            definition = " ".join(words)

        return definition

    definition = ""

    for index, morph in enumerate(word.morphs):

        addition = ""

        env = word.environment_for_index(index)
        last_morph = env.prev
        next_morph = env.next

        # Stack prepositions and prefixes for proper definition ordering
        if morph.get_type() == "prep" or morph.get_type() == "prefix":
            prefix_stack.append([morph, env])
        else:
            definition = build_def(morph, last_morph, env, definition)

            if index != 0:
                if len(prefix_stack) > 0 and (morph.get_type() == "verb" or morph.get_type() == "adj" or morph.get_type() == "noun"):
                    definition = pop_prefix(morph, definition)

    while len(prefix_stack) > 0:
        definition = pop_prefix(word.last_morph(), definition)


    # Make modifications to outermost gloss
    if not morph.has_tag("fixed-gloss"):
        if word.get_type() == "verb":
            return "to " + inflection.inflect(definition, "inf")
        elif word.get_type() == "noun":
            inflected = inflection.inflect(definition, "sg")

            if morph.has_tag("count"):
                return helpers.indefinite_article_for(inflected) + " " +  inflected
            elif morph.has_tag("mass") or morph.has_tag("uncountable"):
                return inflected
            elif morph.has_tag("singleton"):
                return "the " + inflected
            else:
                return inflected

    return definition

def get_joined_form(language, last_morph, morph, original, proposed):
    form = original
    addition = proposed

    if len(form) == 0:
        return addition
    elif len(addition) == 0:
        return form

    # Add joining vowel if needed
    if last_morph != None:
        joining_vowel = get_joining_vowel(language, last_morph, morph, form, addition)
        if joining_vowel != None and form[-1] != joining_vowel:
            form += joining_vowel

    # Merge vowels, e.g.: glaci + ify -> glacify, rage + er -> rager
    if addition[0] == form[-1] and helpers.is_vowel(addition[0]):
        letter = addition[0]

        if (last_morph.get_type() not in ["prep", "prefix"]):
            addition = addition[1:]
        elif letter in ["a", "i", "u"]:
            addition = "-" + addition

    # Cut sounds if indicated
    elif form[-1] == "/" or addition[0] == "/":
        form = form[:-1]
        addition = addition[1:]

    # Language-specific joining rules
    if language == "greek":
        return grk_join.get_joined_form(form, addition)
    if language == "old-english":
        # TODO: Move the suffix and y-to-i checks into language file
        if morph.is_suffix():
            y_to_i = last_morph.has_tag("y-to-i") or morph.has_tag("y-to-i")
            return mne_join.get_joined_form(form, addition, y_to_i=y_to_i)

    return form + addition

def get_joining_vowel(language, first, second, form, addition):
    # If either morph rejects joining vowels, don't use one
    if first.has_tag("no-tail-joiner") or second.has_tag("no-head-joiner"):
        return ""

    # Override joining vowels are always used
    if "form-joiner" in first.morph:
        return first.morph["form-joiner"]

    # Prefixes never need joining vowels
    if first.is_prefix():
        return None

    #  Get vowel by language
    if language == "latin":
        return lat_join.joining_vowel(first, second, addition)
    elif language == "greek":
        return grk_join.joining_vowel(first, second, addition)
    elif language == "old-english":
        return None
    else:
        Logger.error("Invalid language, or language '" + language + "' failed to pick a joining vowel")
        return None
