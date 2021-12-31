#from src.models import Morph, Word
import src.models
import src.inflection as inflection
import src.helpers as helpers

def get_entry(word):        
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

def get_form(word):
        form = ""
        morph = None

        for index, morph in enumerate(word.morphs):

            addition = morph.get_form()

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

                # Spelling changes during joins
                if len(form) > 0:

                    # e.g.: glaci + ify -> glacify
                    if addition[0] == form[-1] and helpers.is_vowel(addition[0]):

                        letter = addition[0]

                        if (not last_morph.get_type() == "prep" and not last_morph.get_type() == "prefix" and not last_morph.get_type() == "number"):
                            addition = addition[1:]
                        elif letter in ["a", "i", "u"]:
                            addition = "-" + addition

                    # Stem change
                    elif morph.has_tag("stem-change") and form[-1] == "i":
                        addition = "e" + addition

                    # Stem raise
                    elif morph.has_tag("stem-raise") and form[-1] == "e":
                        form = form[:-1]
                        addition = "i" + addition

                    # Drop first (sub + emere -> sumere)
                    elif morph.has_tag("drop-first"):
                        addition = addition[1:]

                    elif form[-1] == "/":
                        form = form[:-1]
                        addition = addition[1:]

                form += addition

        return form
    
def get_definition(word):
        morph = None

        prefix_stack = []

        def pop_prefix(morph, definition):

            top = prefix_stack.pop()

            return build_def(top, morph, definition)

        def build_def(morph, last_morph, definition):

            part = morph.get_gloss()
            if last_morph is None:
                definition = part
                
                # Adjectives don't get inflected, so proactively strip their brackets
                if morph.is_root() and morph.get_type() == "adj":
                    definition = definition.replace("[","").replace("]", "")
            else:

                words = part.split(" ")
                for (index, word) in enumerate(words):
                    if word == "%@":
                        words[index] = definition
                    if word == "[%@]":
                        words[index] = "[" + definition + "]"
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
                        elif last_morph.has_tag("mass"):
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
                        elif last_morph.has_tag("mass"):
                            words[index] = inflection.inflect(definition, "mass")
                        elif last_morph.has_tag("singleton"):
                            article = "the"
                            words[index] = article + " " +inflection.inflect(definition, "singleton")
                        else:
                            words[index] = definition
                    elif word == "%!pl":
                        words[index] = inflection.inflect(definition, "pl")

                definition = " ".join(words)

            return definition

        definition = ""

        for index, morph in enumerate(word.morphs):

            addition = ""

            last_morph = morph.prev
            next_morph = morph.next

            # Stack prepositions and prefixes for proper definition ordering
            if morph.get_type() == "prep" or morph.get_type() == "prefix" or morph.get_type() == "number":
                prefix_stack.append(morph)
            else:
                definition = build_def(morph, last_morph, definition)

                if index != 0:
                    if len(prefix_stack) > 0 and (morph.get_type() == "verb" or morph.get_type() == "adj" or morph.get_type() == "noun"):
                        definition = pop_prefix(morph, definition)

        while len(prefix_stack) > 0:
            definition = pop_prefix(word.morphs[word.size()-1], definition)

        # Verbs not otherwise resolved become infinitives
        if morph.get_type() == "verb":
            return "to " + inflection.inflect(definition, "inf")
        elif morph.get_type() == "noun":
            # TODO - Do necessary article handling here. Reuse the code lower down.
            return inflection.inflect(definition, "sg")
        else:
            return definition
