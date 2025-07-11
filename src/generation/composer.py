import re

import src.generation.former as former
import src.generation.glosser as glosser
import src.language.greek.joining as grk_join
import src.language.latin.joining as lat_join
import src.language.modern_english.joining as mne_join
import src.utils.helpers as helpers
import src.utils.inflection as inflection

from random import Random
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

# Compose forms =======================

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

# Add the two forms, applying any special rules of interaction
def get_joined_form(language, last_morph, morph, form, addition):
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
    if language == "old-english" and mne_join.should_join(last_morph, morph):
        y_to_i = last_morph.has_tag("y-to-i") or morph.has_tag("y-to-i")
        return mne_join.get_joined_form(form, addition, y_to_i=y_to_i)

    return form + addition

# Get any joining vowel needed to combine the two forms
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

# Compose definitions ====================

# Applies inflections to the wrapped morph's gloss text, indicated by '%inflectioncode'
def sub_inflection(gloss, wrapped, morph, last_morph):
    subbed = gloss
    while "%" in subbed:
        match = re.search(r'%([\w\@\!\']*)', subbed)
        code = match.group()

        if code == "%@":
            value = wrapped
        elif code == "%inf":
            value = glosser.inflect_gloss("to " + wrapped, inflection.infinitive)
        elif code == "%3sg":
            value = glosser.inflect_gloss(wrapped, inflection.third_singular)
        elif code == "%part":
            value = glosser.inflect_gloss(wrapped, inflection.present_participle)
        elif code == "%ppart":
            value = glosser.inflect_gloss(wrapped, inflection.past_participle)
        elif code == "%sg":
            if last_morph.has_tag("count"):
                inflected = glosser.inflect_gloss(wrapped, inflection.singular)
                article = helpers.indefinite_article_for(inflected)
                value = article + " " + inflected
            elif last_morph.has_tag("mass") or last_morph.has_tag("uncountable"):
                value = glosser.inflect_gloss(wrapped, inflection.singular)
            elif last_morph.has_tag("singleton"):
                article = "the"
                value = article + " " + glosser.inflect_gloss(wrapped, inflection.singular)
            else:
                # This case can be hit e.g. in cases where a suffix applies to both nouns and adjectives
                value = wrapped
        elif code == "%!sg":
            value = glosser.inflect_gloss(wrapped, inflection.singular)
        elif code == "%pl":
            if last_morph.has_tag("count"):
                value = glosser.inflect_gloss(wrapped, inflection.plural)
            elif last_morph.has_tag("singleton"):
                article = "the"
                value = article + " " +glosser.inflect_gloss(wrapped, inflection.singular)
            else:
                # This case can be hit e.g. in cases where a suffix applies to both nouns and adjectives
                value = wrapped
        elif code == "%!pl":
            value = glosser.inflect_gloss(wrapped, inflection.plural)
        else:
            Logger.error("unrecognized inflection code '" + code + "'")

        subbed = subbed.replace(code, value)

    return subbed

# Substitutes references to a wrapped morph's properties, indicated by '&(property-name)'
def sub_properties(gloss, morph, last_morph):
    subbed = gloss
    while "&" in subbed:
        match = re.search(r'&\((.*?)\)', subbed)

        ref_property = match.group(1)
        if not ref_property in last_morph.morph:
            Logger.error("referred to missing property '" + ref_property + "' in morph " + last_morph.morph["key"])

        value = helpers.one_or_random(last_morph.morph[ref_property], seed=morph.seed)

        # If the gloss is a single word, add brackets
        if not " " in value:
            value = "[" + value + "]"

        subbed = strip_brackets(subbed)
        subbed = subbed.replace(match.group(), value)

    return subbed

# Populates the morph's gloss with data from the environment
def populate_gloss(morph, last_morph, env, wrapped):
    gloss = glosser.gloss(morph, env)
    out_words = []

    if last_morph is None:
        return gloss

    gloss = sub_inflection(gloss, wrapped, morph, last_morph)
    gloss = sub_properties(gloss, morph, last_morph)

    return gloss

# Makes modifications to final definition text so that it can stand on its own
def finalize_definition(word, definition):
    if word.get_type() == "verb":
        return "to " + glosser.inflect_gloss(definition, inflection.infinitive)
    elif word.get_type() == "noun":
        last_morph = word.last_morph()
        inflected = glosser.inflect_gloss(definition, inflection.singular)

        if last_morph.has_tag("count"):
            return helpers.indefinite_article_for(inflected) + " " +  inflected
        elif last_morph.has_tag("mass") or last_morph.has_tag("uncountable"):
            return inflected
        elif last_morph.has_tag("singleton"):
            return "the " + inflected
        else:
            return inflected
    elif word.get_type() == "adj":
        return strip_brackets(definition)

# Gets the final definition for the word
def get_definition(word):
    prefix_stack = []

    # Returns the populated gloss of the topmost prefix in the stack
    def pop_prefix(last_morph, definition):
        top, env = prefix_stack.pop()
        return populate_gloss(top, last_morph, env, definition)

    morph = None
    definition = ""
    for index, morph in enumerate(word.morphs):
        env = word.environment_for_index(index)

        # Stack prepositions and prefixes for proper definition ordering
        if morph.is_prefix():
            prefix_stack.append([morph, env])
        else:
            definition = populate_gloss(morph, env.prev, env, definition)
            # TODO: This logic seems to mostly reflect verbal prefixes, but is apparently
            # necessary for relational circumfixes. Reconsider.
            if len(prefix_stack) > 0 and morph.is_root():
                definition = pop_prefix(morph, definition)

    # Apply prefixes in reverse order
    while len(prefix_stack) > 0:
        definition = pop_prefix(word.last_morph(), definition)

    # Finalize
    if not morph.has_tag("fixed-gloss"):
        definition = finalize_definition(word, definition)

    return definition

# Helpers ============================

def strip_brackets(string):
    return string.replace("[","").replace("]", "")
