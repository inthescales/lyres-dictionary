from random import Random

import src.models
import src.generation.former as former
import src.utils.helpers as helpers
import src.utils.inflection as inflection

import src.evolutor.language.mne_affixation as mne_affixation

def entry(word):
    composed = get_form(word)
    tag = get_part_tag(word)
    definition = get_definition(word)
    entry = composed + " " + tag + "\n" + definition
    return entry

def get_part_tag(word):

    pos = word.get_type()

    if pos == "noun":
        abbrev = "n"
    elif pos == "adj":
        abbrev = "adj"
    elif pos == "verb":
        abbrev = "v"
    elif pos == "prep":
        abbrev = "prep"
    else:
        abbrev = "???"

    return "(" + abbrev + ")"

def get_form(word, former_config=None):
    form = ""
    morph = None
    
    for index, morph in enumerate(word.morphs):

        env = word.environment_for_index(index)
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

            if index < word.size() - 1:
                next_morph = word.morphs[index+1]
            else:
                next_morph = None

            form = get_joined_form(word.get_origin(), last_morph, morph, form, addition)

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
        if morph.get_type() == "prep" or morph.get_type() == "prefix" or morph.get_type() == "number":
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
        if morph.get_type() == "verb":
            return "to " + inflection.inflect(definition, "inf")
        elif morph.get_type() == "noun":
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

    # Add joining vowel if needed
    if last_morph != None:
        joining_vowel = get_joining_vowel(language, last_morph, morph, form, addition)
        if joining_vowel != None and form[-1] != joining_vowel:
            form += joining_vowel

    # e.g.: glaci + ify -> glacify
    if language in ["latin", "greek"] and addition[0] == form[-1] and helpers.is_vowel(addition[0]):

        letter = addition[0]

        if (not last_morph.get_type() == "prep" and not last_morph.get_type() == "prefix" and not last_morph.get_type() == "number"):
            addition = addition[1:]
        elif letter in ["a", "i", "u"]:
            addition = "-" + addition

    # Stem change
    if morph.has_tag("stem-change") and form[-1] == "i":
        addition = "e" + addition

    # Stem raise
    elif morph.has_tag("stem-raise") and form[-1] == "e":
        form = form[:-1]
        addition = "i" + addition

    # Drop first (sub + emere -> sumere)
    elif morph.has_tag("drop-first"):
        addition = addition[1:]

    elif form[-1] == "/" or addition[0] == "/":
        form = form[:-1]
        addition = addition[1:]

    # Language-specific phonotactics
    if language == "greek":
        if form[-1] in ["c", "g", "k"] and addition[0] == "s":
            form = form[:-1]
            addition = "x" + addition[1:]

        if form[-1] in ["c", "k"] and addition[0] == "m":
            form = form[:-1] + "g"
            addition = addition
        
        if form[-1] == "p" and addition[0] == "m":
            form = form[:-1] + "m"
        
        if form[-1] == "t" and addition in ["ia", "y"] and form[-2] not in ["n", "r", "s", "u"]:
            form = form[:-1] + "s"
    
    if language == "old-english":
        if morph.is_suffix():
            return mne_affixation.get_joined_form(form, addition)

        if last_morph.get_type() == "number":
            form = form + "-"
        
    return form + addition

def get_joining_vowel(language, first, second, form, addition):

    # If either morph rejects joining vowels, don't use one
    if first.has_tag("no-tail-joiner") or second.has_tag("no-head-joiner"):
        return ""

    if language == "latin":

        # Prefixes never need joining vowels
        if first.is_prefix():
            return None

        # Override joining vowels are always used
        if "form-joiner" in first.morph:
            return first.morph["form-joiner"]

        # Some noun declensions use a standard joining vowel
        if first.get_type() == "noun" and first.morph["declension"] in [4, 5] \
            and (addition[0] in ["a", "o", "u"]): # or not helpers.is_vowel(addition[0])):
                vowels = {4: "u", 5: "i"}
                return vowels[first.morph["declension"]]

        # For verb suffixes using the present participle stem
        if first.get_type() == "verb" and not helpers.is_vowel(addition[0], y_is_vowel=True) and second.morph["derive-participle"] == "present" \
            and not helpers.is_vowel(addition[0], y_is_vowel=True):

            # If the verb declares a joiner for this case, use it
            if "form-joiner-present" in first.morph:
                return first.morph["form-joiner-present"]

            # Exceptional present-stem verb endings
            if first.get_type() == "verb" and second.morph["key"] in ["-nt", "-nt-noun", "-nce", "-nd"]:
                verb_vowels = {1: "a", 2: "e", 3: "e", 4: "ie", 0: ""}
                return verb_vowels[first.morph["conjugation"]]

            if first.get_type() == "verb" and second.morph["key"] in ["-ble"]:
                verb_vowels = {1: "a", 2: "i", 3: "i", 4: "i", 0: ""}
                return verb_vowels[first.morph["conjugation"]]

        # Return the base vowel otherwise
        if not helpers.is_vowel(addition[0], y_is_vowel=True):
            return "i"
        else:
            return ""

    elif language == "greek":

        # Prefixes never need joining vowels
        if first.is_prefix():
            return None

        # Override joining vowels are always used
        if "form-joiner" in first.morph:
            return first.morph["form-joiner"]

        if not helpers.is_vowel(addition[0], y_is_vowel=True):
            return "o"
        else:
            return ""
    
    elif language == "old-english":
        return ""

    Logger.error("Invalid language, or language '" + language + "' failed to pick a joining vowel")
    return ""
