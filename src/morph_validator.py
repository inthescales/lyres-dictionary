from src.logging import Logger

valid_properties = [
    "key",
    "type",
    "prefix-on",                # Preposition / Prefix - determines what root types this can be prefixed to
    "derive-from",              # Type derive attaches to
    "derive-to",                # Type derive produces
    "derive-participle",        # Participle type used by a suffix
    "form",
    "form-final",
    "form-stem",
    "form-raw",                 # Original form, before historical changes
    "form-canon",               # Actual form in modern English (as opposed to plausible alternatives)
    "form-stem-present",        # Present participle stem for Latin verbs
    "form-stem-perfect",        # Perfect participle stem for Latin verbs
    "form-stem-assim",          # Stem for assimilating prefixes
    "form-joiner",              # Joining vowel override for this morph
    "form-joiner-present",      # Joining vowel(s) used for Latin present participles
    "form-assimilation",        # Assimilation rules
    "conjugation",
    "declension",
    "gloss",
    "gloss-final",              # Gloss used when this is the last morph
    "gloss-link",               # Gloss used when not the last morph
    "gloss-relative",           # Verb:   Alternate gloss used with prepositional prefix
                                # Derive: Gloss used in relative constructs
    "gloss-adj",                # Gloss used when derive is attached to adjective.
    "gloss-noun",               # Gloss used when preposition attaches to noun in relative construct
    "gloss-verb",               # Gloss used when preposition or derive is attached to verb
    "gloss-state",              # Adjective gloss associated with a stative verb
    "gloss-tool",               # Verb gloss associated with a tool noun
    "suffixes",                 # Valid suffixes that can follow this morph
    "tags",
    "requires",
    "exception",
    "origin",
    "notes"
]

valid_tags = [
    "count",                    # Noun countability - countable
    "mass",                     # Noun countability - mass
    "singleton",                # Noun countability - singleton, e.g. "The Earth"
    "uncountable",              # Noun countability - generically uncountable, will never use articles
    "concrete",                 # Noun actuality - a concrete object in the world
    "abstract",                 # Noun actuality - something not physically in the world
    "bounded",                  # Noun actuality - optionally for abstracts, does it have a bounded aspect (e.g. a length of time)
    "living",                   # Noun semantics - a living being
    "animal",                   # Noun semantics - an animal
    "plant",                    # Noun semantics - a plant
    "person",                   # Noun semantics - a kind of person
    "bodypart",                 # Noun semantics - member or organ of a living being, animal or plant
    "bodypart-plant",           # Noun semantics - a member belonging only to a plant, like a leaf or stem
    "bodypart-single",          # Noun semantics - a bodypart that someone has only one of
    "secretion",                # Noun semantics - a bodily secretion
    "tool",                     # Noun semantics - a tool
    "weapon",                   # Noun semantics - a weapon
    "material",                 # Noun semantics - a material things can be made out of
    "metal",                    # Noun semantics - a metal
    "fluid",                    # Noun semantics - a fluid, like a liquid or gas
    "liquid",                   # Noun semantics - a liquid
    "gas",                      # Noun semantics - a gas
    "region",                   # Noun semantics - a region
    "terrain",                  # Noun semantics - a type of land
    "grouping",                 # Noun semantics - a group or collection of things
    "color",                    # Noun semantics - a color
    "shape",                    # Noun semantics - a shape
    "time",                     # Noun semantics - a period of time
    "number",                   # Noun semantics - a number (used as a noun)
    "superlative",              # Adjective morphology - a superlative
    "character",                # Adjective semantics - descriptor of a person's character
    "transitive",               # Verb transitivity - transitive verb
    "intransitive",             # Verb transitivity - intransitive verb
    "no-prep",                  # Verb morphology - cannot take a prepositional prefix
    "always-prep",              # Verb morphology - must always have a prepositional prefix
    "stative",                  # Verb syntax - describes being in a particular state, as a verb
    "object-specifier",         # Verb syntax - specifies the object of an attached verb
    "motion",                   # Verb semantics - moving or causing motion
    "joining",                  # Verb semantics - joining or connecting two things into one
    "dividing",                 # Verb semantics - dividing one thing into two or more
    "no-head-joiner",           # Form - Doesn't take joining vowels on the front end
    "no-tail-joiner",           # Form - Doesn't take joining vowels on the back end
    "no-length",                # Generation - does not count towards maximum morph count
    "rare",                     # Generation - occurs less often in generation
    "no-gen",                   # Generation - will not be chosen randomly in generation, only if specified as allowed suffix
    "non-final",                # Generation - cannot be the final morph in the word"
    "suffix-only",              # Generation - adding a suffix is the only valid transformation following this morph
]

def validate_morph(morph):

    if not "key" in morph:
        Logger.error("no key found in morph:")
        Logger.error(" - " + str(morph))
        return False

    errored = False
    def record_error(message):
        nonlocal errored

        if errored == False:
            Logger.warn("errors found reading morph '" + morph["key"] + "'")
            errored = True

        Logger.warn(message)

    if not "type" in morph:
        record_error(" - type is missing")
        return False

    if not "origin" in morph:
        record_error(" - origin is missing")
        return False

    morph_type = morph["type"]

    derive_type = None
    if morph_type == "derive": derive_type = morph["derive-to"]

    # Derives requirements (not exclusive with root type requirements)  
    if morph_type == "derive":
        if not ("derive-from" in morph and "derive-to" in morph):
            record_error(" - derive morphs must have 'derive-from' and 'derive-to'")
            return False

    # Root and prefix type requirements
    if morph_type == "noun" or derive_type == "noun":
        if morph["origin"] == "latin":
            if not "form-stem" in morph or not "declension" in morph:
                record_error(" - noun must have 'form-stem' and 'declension'")
                return False
            elif not ("tags" in morph and ("count" in morph["tags"] or "mass" in morph["tags"] or "singleton" in morph["tags"] or "uncountable" in morph["tags"])):
                record_error(" - noun must have a countability tag ('count', 'mass', 'singleton', or 'uncountable')")
                return False
            elif morph["declension"] not in [0, 1, 2, 3, 4, 5]:
                record_error(" - invalid declension '" + str(morph["declension"]) + "'")
                return False
        elif morph["origin"] == "greek":
            if not "form-stem" in morph:
                record_error(" - noun must have 'form-stem'")
                return False
            elif not ("tags" in morph and ("count" in morph["tags"] or "mass" in morph["tags"] or "singleton" in morph["tags"] or "uncountable" in morph["tags"])):
                record_error(" - noun must have a countability tag ('count', 'mass', 'singleton', or 'uncountable')")
                return False
        elif morph["origin"] == "old-english":
            if not ("form-raw" in morph or "form-stem" in morph):
                record_error(" - noun must have 'form-raw' or 'form-stem'")
                return False
            elif not ("tags" in morph and ("count" in morph["tags"] or "mass" in morph["tags"] or "singleton" in morph["tags"] or "uncountable" in morph["tags"])):
                record_error(" - noun must have a countability tag ('count', 'mass', 'singleton', or 'uncountable')")
                return False

    elif morph_type == "adj" or derive_type == "adj":
        if morph["origin"] == "latin":
            if not "form-stem" in morph or not "declension" in morph:
                record_error(" - adjective must have 'form-stem' and 'declension'")
                return False
            elif morph["declension"] not in [0, 12, 3]:
                record_error(" - invalid declension '" + str(morph["declension"]) + "'")
                return False
        elif morph["origin"] == "greek":
            if not "form-stem" in morph:
                record_error(" - adjective must have 'form-stem'")
                return False
        elif morph["origin"] == "old-english":
            if not ("form-raw" in morph or "form-stem" in morph):
                record_error(" - noun must have 'form-raw' or 'form-stem'")
                return False

    elif morph_type == "verb" or derive_type == "verb":
        if morph["origin"] == "latin":
            if "form-stem-present" in morph and "form-stem-perfect" in morph and morph["form-stem-present"] == morph["form-stem-perfect"]:
                print("SAME: " + morph["key"])
            if not (("form-stem-present" in morph or "form-stem" in morph) \
                 and ("form-final" or "form-stem" in morph) in morph \
                 and "conjugation" in morph):
                record_error(" - verbs require 'form-stem-present', 'form-stem-perfect', 'form-final', and 'conjugation'")
                return False

            if morph["conjugation"] not in [0, 1, 2, 3, 4]:
                record_error(" - invalid conjugation '" + str(morph["conjugation"]) + "'")
                return False
            
        if morph["origin"] == "old-english":
            if not ("form-raw" in morph or "form-stem" in morph):
                record_error(" - noun must have 'form-raw' or 'form-stem'")
                return False

    elif morph_type == "prefix":
        if not ("prefix-on" in morph):
            record_error(" - prefix morphs must have 'prefix-on'")

    elif morph_type == "prep":
        if not ("prefix-on" in morph):
            record_error(" - prep morphs must have 'prefix-on'")

    # Check key whitelist
    for key in morph:
        if not key in valid_properties:
            record_error("Invalid morph property '" + key + "' found in morph '" + morph["key"] + "'")

    # Check tag whitelist
    if "tags" in morph:
        for tag in morph["tags"]:
            if not tag in valid_tags:
                record_error("Invalid morph tag '" + tag + "' found on morph '" + morph["key"] + "'")

    return True
