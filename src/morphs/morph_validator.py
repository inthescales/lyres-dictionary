from src.utils.logging import Logger

valid_properties = [
    "key",
    "type",
    "prefix-on",                # Preposition / Prefix - determines what root types this can be prefixed to
    "prefix-to",                # Preposition / Prefix - determines what type the outcome of this prefixing is
    "derive-from",              # Type derive attaches to
    "derive-to",                # Type derive produces
    "derive-participle",        # Participle type used by a suffix
    "form",
    "form-final",
    "form-stem",
    "form-raw",                 # Original form, before historical changes
    "form-raw-alt",             # Nonstandard raw forms (e.g. rare or dialectal)
    "form-canon",               # Actual form in modern English (as opposed to plausible alternatives)
    "form-participle-raw",      # Original participle forms. There may be one or a list.
    "form-participle-canon",    # Accepted modern participle forms.
    "form-stem-present",        # Present participle stem for Latin verbs
    "form-stem-perfect",        # Perfect participle stem for Latin verbs
    "form-stem-assim",          # Stem for assimilating prefixes
    "form-joiner",              # Joining vowel override for this morph
    "form-joiner-present",      # Joining vowel(s) used for Latin present participles
    "form-assimilation",        # Assimilation rules
    "conjugation",
    "declension",
    "gloss",
    "gloss-alt",                # Nonstandard glosses (e.g. historical)
    "gloss-final",              # Gloss used when this is the last morph
    "gloss-link",               # Gloss used when not the last morph
    "gloss-relative",           # Verb:   Alternate gloss used with prepositional prefix
                                # Derive: Gloss used in relative constructs
    "gloss-adj",                # Gloss used when derive is attached to adjective.
    "gloss-noun",               # Gloss used when preposition attaches to noun in relative construct
    "gloss-verb",               # Gloss used when preposition or derive is attached to verb
    "gloss-state",              # Adjective gloss associated with a stative verb
    "gloss-tool",               # Verb gloss associated with a tool noun
    "gloss-animal",             # Verb gloss associated with an animal noun
    "verb-class",               # Verb class (used in Old English)
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
    "tame",                     # Noun semantics - a tame animal
    "wild",                     # Noun semantics - a wild animal
    "mammal",                   # Noun semantics - a mammal
    "plant",                    # Noun semantics - a plant
    "person",                   # Noun semantics - a kind of person
    "gendered",                 # Noun semantics - unchangeably gendered
    "role",                     # Noun semantics - a role that a person takes on (as opposed to inborn identity)
    "ruler",                    # Noun semantics - a person who rules over a place or thing
    "divine",                   # Noun semantics - a divine being (god, angel, etc)
    "magical",                  # Noun semantics - a magical or supernatural being (elf, ghost, etc)
    "bodypart",                 # Noun semantics - a member or organ of a living being, animal or plant
    "bodypart-plant",           # Noun semantics - a member belonging only to a plant, like a leaf or stem
    "bodypart-single",          # Noun semantics - a bodypart that a being has only one of, like heart or head
    "secretion",                # Noun semantics - a bodily secretion, or mental creation
    "garment",                  # Noun semantics - a garment, or anything that is worn on the body
    "man-made",                 # Noun semantics - something made by humans
    "metallic",                 # Noun semantics - an object made from metal
    "shiny",                    # Noun semantics - reflects light
    "tool",                     # Noun semantics - a tool
    "weapon",                   # Noun semantics - a weapon
    "vessel",                   # Noun semantics - a vessel (containers and boats)
    "material",                 # Noun semantics - a material things can be made out of
    "food",                     # Noun semantics - a food or ingredient of food
    "metal",                    # Noun semantics - a metal
    "fluid",                    # Noun semantics - a fluid, like a liquid or gas
    "liquid",                   # Noun semantics - a liquid
    "gas",                      # Noun semantics - a gas
    "luminous",                 # Noun semantics - emits light
    "glooming",                 # Noun semantics - obscures light or darkens (esp. of weather and times)
    "region",                   # Noun semantics - a region
    "terrain",                  # Noun semantics - a type of land
    "place",                    # Noun semantics - a specific place (e.g. hell, home, the sky)
    "grouping",                 # Noun semantics - a group or collection of things
    "color",                    # Noun semantics - a color
    "shape",                    # Noun semantics - a shape
    "quality",                  # Noun semantics - an abstract quality
    "body-state",               # Noun semantics - a bodily condition
    "mind-state",               # Noun semantics - a mental or emotional state
    "activity",                 # Noun semantics - an activity that a person can undertake
    "time",                     # Noun semantics - a period of time
    "time-of-day",              # Noun semantics - a period of time in the day (e.g. morning, dawn)
    "time-of-year",             # Noun semantics - a period of time in the year (e.g. winter, lent)
    "measure",                  # Noun semantics - a unit of measure
    "tree",                     # Noun semantics - a kind of tree
    "number",                   # Noun semantics - a number (used as a noun)
    "weather",                  # Noun semantics - a type of weather
    "superlative",              # Adjective morphology - a superlative
    "character",                # Adjective semantics - descriptor of a person's character
    "a-prefix",                 # Verb lexical - can take the OE 'ā-' prefix without change in meaning
    "ge-prefix",                # Verb lexical - can take the OE 'ġe-' prefix without change in meaning
    "transitive",               # Verb transitivity - transitive verb
    "intransitive",             # Verb transitivity - intransitive verb
    "no-prep",                  # Verb morphology - cannot take a prepositional prefix
    "always-prep",              # Verb morphology - must always have a prepositional prefix
    "stative",                  # Verb syntax - describes being in a particular state, as a verb
    "object-specifier",         # Verb syntax - specifies the object of an attached verb
    "motion",                   # Verb semantics - moving or causing motion
    "joining",                  # Verb semantics - joining or connecting two things into one
    "dividing",                 # Verb semantics - dividing one thing into two or more
    "sexual",                   # Verb semantics - may contain sexual content
    "no-head-joiner",           # Form - Doesn't take joining vowels on the front end
    "no-tail-joiner",           # Form - Doesn't take joining vowels on the back end
    "no-length",                # Generation - does not count towards maximum morph count
    "rare",                     # Generation - occurs less often in generation
    "super-rare",               # Generation - occurs even less often in generation
    "no-gen",                   # Generation - will not be chosen randomly in generation, only if specified as allowed suffix
    "obscure",                  # Generation - the morph is attested in modern English, but only in archaic texts or minor dialects
    "speculative",              # Generation - the morph is not attested in modern English
    "poetic",                   # Generation - the morph is only attested in poetic usage in its original language
    "homophonic",               # Generation - the morphs processed form is a homophone (or nearly) with a common actual word
    "final",                    # Generation - immediately ends generation
    "non-final",                # Generation - cannot be the final morph in the word
    "suffix-only",              # Generation - adding a suffix is the only valid transformation following this morph
    "fixed-gloss",              # Generation - the gloss of this morph is fixed - no additions should be made (e.g. articles, infinitive 'to', etc), and it has no embeds,
    "i-mutating",               # OE morphophonology - causes i-mutation in the joined root
    "y-to-i"                    # MnE orthography - causes a final unstressed 'y' to become 'i' when a consonant is suffixed (e.g. 'day' + '-ly' -> 'daily')
]

valid_types = [
    "noun",
    "adj",
    "verb",
    "number",
    "prep",
    "prefix",
    "derive"
]

valid_origins = [
    "latin",
    "greek",
    "old-english",
    "modern-english"
]

def validate_morph(morph):
    errored = False
    # Logs an error, logging a top-level error line only once
    def record_error(message):
        nonlocal errored

        if errored == False:
            if "key" in morph:
                Logger.warn("errors found reading morph '" + morph["key"] + "'")
            else:
                Logger.warn("errors found reading morph without key: " + str(morph))
            errored = True

        Logger.warn(message)

    # Returns true if the given requirement clause is satisfied by the given morph.
    # key_required - indicates whether errors should be logged if the given key is missing
    def evaluate_clause(clause, morph, key_required=True, category=None):
        key = clause["key"]
        if key not in morph:
            if key_required:
                if category == None:
                    record_error(" - property '" + key + "' is required all morphs")
                else:
                    record_error(" - property '" + key + "' is required for morphs of type '" + category + "'")
            return False

        # TODO: Validate values where the value may be a specific value or a list of values (e.g. derive-from,
        # which may be a word type of a list of types)
        elif "values" in clause and morph[key] not in clause["values"]:
            record_error(" - invalid value '" + str(morph[key]) + "' for property '" + key + "' in morph '" + morph["key"] + "'. Accepted values: " + str(clause["values"]))
            return False

        return True

    # Returns true if any of the given clauses are satisfied by the given morph
    def evaluate_any(clauses, morph, category=None):
        for clause in clauses:
            if evaluate_clause(clause, morph, False, category):
                return True

        if category == None:
            record_error(" - all morphs must contain one of: " + ", ".join([x["key"] for x in clauses]))
        else:
            record_error(" - morphs of type '" + category + "' must contain one of: " + ", ".join([x["key"] for x in clauses]))
        return False

    # Checks whether the given requirements are satisfied by the given morph
    def evaluate_requirements(requirements, morph, category=None):
        valid = True
        for requirement in requirements:
            if "any" in requirement:
                valid = valid and evaluate_any(requirement["any"], morph, category)
            else:
                valid = valid and evaluate_clause(requirement, morph, True, category)

        return valid

    valid = True

    # Properties required by all morphs
    universal_requirements = [
        { "key": "key" },
        { "key": "type", "values": valid_types},
        { "key": "origin", "values": valid_origins }
    ]
    valid = valid and evaluate_requirements(universal_requirements, morph)

    # Properties required by morphs of a certain type
    type_requirements = {
        "derive": [
            { "key": "derive-from" },
            { "key": "derive-to" }
        ],
        "prep": [
            { "key": "prefix-on" },
        ],
        "prefix": [
            { "key": "prefix-on" },
        ]
    }
    if morph["type"] in type_requirements:
        valid = valid and evaluate_requirements(type_requirements[morph["type"]], morph, morph["type"])

    # Properties required by morphs of a certain type and origin
    origin_type_requirements = {
        "latin": {
            "noun": [
                { "key": "form-stem" },
                { "key": "declension", "values": [0, 1, 2, 3, 4, 5] },
            ],
            "adj": [
                { "key": "form-stem" },
                { "key": "declension", "values": [0, 12, 3] },
            ],
            "verb": [
                { "any": [
                    { "key": "form-stem-present" },
                    { "key": "form-stem" }
                ]},
                { "any": [
                    { "key": "form-final" },
                    { "key": "form-stem" }
                ]},
                { "key": "conjugation", "value": [0, 1, 2, 3, 4] },
            ]
        },
        "greek": {
            "noun": [
                { "key": "form-stem" },
            ],
            "adj": [
                { "key": "form-stem" },
            ],
            "verb": [
                { "key": "form-stem" },
            ]
        },
        "old-english": {
            "noun": [
                { "any": [
                    { "key": "form-stem" },
                    { "key": "form-raw" },
                ]}
            ],
            "adj": [
                { "any": [
                    { "key": "form-stem" },
                    { "key": "form-raw" },
                ]}
            ],
            "verb": [
                { "any": [
                    { "key": "form-stem" },
                    { "key": "form-raw" },
                ]},
                { "key": "verb-class", "values": [1, 2, 3, 4, 5, 6, 7, "weak", "preterite-present"] }
            ]
        }
    }

    if morph["origin"] in origin_type_requirements and morph["type"] in origin_type_requirements[morph["origin"]]:
        valid = valid and evaluate_requirements(origin_type_requirements[morph["origin"]][morph["type"]], morph, " ".join(morph["origin"].split("-")) + " " + morph["type"])

    morph_type = morph["type"]

    derive_type = None
    if morph_type == "derive": derive_type = morph["derive-to"]

    # Root and prefix type requirements
    if morph_type == "noun" or derive_type == "noun":
        if morph["origin"] == "latin":
            if not ("tags" in morph and ("count" in morph["tags"] or "mass" in morph["tags"] or "singleton" in morph["tags"] or "uncountable" in morph["tags"])):
                record_error(" - noun must have a countability tag ('count', 'mass', 'singleton', or 'uncountable')")
                return False
        elif morph["origin"] == "greek":
            if not ("tags" in morph and ("count" in morph["tags"] or "mass" in morph["tags"] or "singleton" in morph["tags"] or "uncountable" in morph["tags"])):
                record_error(" - noun must have a countability tag ('count', 'mass', 'singleton', or 'uncountable')")
                return False
        elif morph["origin"] == "old-english":
            if not ("tags" in morph and ("count" in morph["tags"] or "mass" in morph["tags"] or "singleton" in morph["tags"] or "uncountable" in morph["tags"])):
                record_error(" - noun must have a countability tag ('count', 'mass', 'singleton', or 'uncountable')")
                return False

    # Check key whitelist
    for key in morph:
        if not key in valid_properties:
            record_error("Invalid morph property '" + key + "' found in morph '" + morph["key"] + "'")
            valid = False

    # Check tag whitelist
    if "tags" in morph:
        for tag in morph["tags"]:
            if not tag in valid_tags:
                record_error("Invalid morph tag '" + tag + "' found on morph '" + morph["key"] + "'")
                valid = False

    return valid
