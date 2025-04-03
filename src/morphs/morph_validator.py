from src.utils.logging import Logger

valid_properties = [
    "key",
    "type",
    "prefix-on",                # Preposition / Prefixdetermines what root types this can be prefixed to
    "prefix-to",                # Preposition / Prefixdetermines what type the outcome of this prefixing is
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
    "count",                    # Noun countabilitycountable
    "mass",                     # Noun countabilitymass
    "singleton",                # Noun countabilitysingleton, e.g. "The Earth"
    "uncountable",              # Noun countabilitygenerically uncountable, will never use articles
    "concrete",                 # Noun actualitya concrete object in the world
    "abstract",                 # Noun actualitysomething not physically in the world
    "bounded",                  # Noun actualityoptionally for abstracts, does it have a bounded aspect (e.g. a length of time)
    "living",                   # Noun semanticsa living being
    "animal",                   # Noun semanticsan animal
    "tame",                     # Noun semanticsa tame animal
    "wild",                     # Noun semanticsa wild animal
    "mammal",                   # Noun semanticsa mammal
    "plant",                    # Noun semanticsa plant
    "person",                   # Noun semanticsa kind of person
    "gendered",                 # Noun semanticsunchangeably gendered
    "role",                     # Noun semanticsa role that a person takes on (as opposed to inborn identity)
    "ruler",                    # Noun semanticsa person who rules over a place or thing
    "divine",                   # Noun semanticsa divine being (god, angel, etc)
    "magical",                  # Noun semanticsa magical or supernatural being (elf, ghost, etc)
    "bodypart",                 # Noun semanticsa member or organ of a living being, animal or plant
    "bodypart-plant",           # Noun semanticsa member belonging only to a plant, like a leaf or stem
    "bodypart-single",          # Noun semanticsa bodypart that a being has only one of, like heart or head
    "secretion",                # Noun semanticsa bodily secretion, or mental creation
    "garment",                  # Noun semanticsa garment, or anything that is worn on the body
    "man-made",                 # Noun semanticssomething made by humans
    "metallic",                 # Noun semanticsan object made from metal
    "shiny",                    # Noun semanticsreflects light
    "tool",                     # Noun semanticsa tool
    "weapon",                   # Noun semanticsa weapon
    "vessel",                   # Noun semanticsa vessel (containers and boats)
    "material",                 # Noun semanticsa material things can be made out of
    "food",                     # Noun semanticsa food or ingredient of food
    "metal",                    # Noun semanticsa metal
    "fluid",                    # Noun semanticsa fluid, like a liquid or gas
    "liquid",                   # Noun semanticsa liquid
    "gas",                      # Noun semanticsa gas
    "luminous",                 # Noun semanticsemits light
    "glooming",                 # Noun semanticsobscures light or darkens (esp. of weather and times)
    "region",                   # Noun semanticsa region
    "terrain",                  # Noun semanticsa type of land
    "place",                    # Noun semanticsa specific place (e.g. hell, home, the sky)
    "grouping",                 # Noun semanticsa group or collection of things
    "color",                    # Noun semanticsa color
    "shape",                    # Noun semanticsa shape
    "quality",                  # Noun semanticsan abstract quality
    "body-state",               # Noun semanticsa bodily condition
    "mind-state",               # Noun semanticsa mental or emotional state
    "activity",                 # Noun semanticsan activity that a person can undertake
    "time",                     # Noun semanticsa period of time
    "time-of-day",              # Noun semanticsa period of time in the day (e.g. morning, dawn)
    "time-of-year",             # Noun semanticsa period of time in the year (e.g. winter, lent)
    "measure",                  # Noun semanticsa unit of measure
    "tree",                     # Noun semanticsa kind of tree
    "number",                   # Noun semanticsa number (used as a noun)
    "weather",                  # Noun semanticsa type of weather
    "superlative",              # Adjective morphologya superlative
    "character",                # Adjective semanticsdescriptor of a person's character
    "a-prefix",                 # Verb lexicalcan take the OE 'ā-' prefix without change in meaning
    "ge-prefix",                # Verb lexicalcan take the OE 'ġe-' prefix without change in meaning
    "transitive",               # Verb transitivitytransitive verb
    "intransitive",             # Verb transitivityintransitive verb
    "no-prep",                  # Verb morphologycannot take a prepositional prefix
    "always-prep",              # Verb morphologymust always have a prepositional prefix
    "stative",                  # Verb syntaxdescribes being in a particular state, as a verb
    "object-specifier",         # Verb syntaxspecifies the object of an attached verb
    "motion",                   # Verb semanticsmoving or causing motion
    "joining",                  # Verb semanticsjoining or connecting two things into one
    "dividing",                 # Verb semanticsdividing one thing into two or more
    "sexual",                   # Verb semanticsmay contain sexual content
    "no-head-joiner",           # FormDoesn't take joining vowels on the front end
    "no-tail-joiner",           # FormDoesn't take joining vowels on the back end
    "no-length",                # Generationdoes not count towards maximum morph count
    "rare",                     # Generationoccurs less often in generation
    "super-rare",               # Generationoccurs even less often in generation
    "no-gen",                   # Generationwill not be chosen randomly in generation, only if specified as allowed suffix
    "obscure",                  # Generationthe morph is attested in modern English, but only in archaic texts or minor dialects
    "speculative",              # Generationthe morph is not attested in modern English
    "poetic",                   # Generationthe morph is only attested in poetic usage in its original language
    "homophonic",               # Generationthe morphs processed form is a homophone (or nearly) with a common actual word
    "final",                    # Generationimmediately ends generation
    "non-final",                # Generationcannot be the final morph in the word
    "suffix-only",              # Generationadding a suffix is the only valid transformation following this morph
    "fixed-gloss",              # Generationthe gloss of this morph is fixedno additions should be made (e.g. articles, infinitive 'to', etc), and it has no embeds,
    "i-mutating",               # OE morphophonologycauses i-mutation in the joined root
    "y-to-i"                    # MnE orthographycauses a final unstressed 'y' to become 'i' when a consonant is suffixed (e.g. 'day' + '-ly' -> 'daily')
]

morph_types = [
    "noun",
    "adj",
    "verb",
    "number",
    "prep",
    "prefix",
    "derive"
]

root_types = [
    "noun",
    "adj",
    "verb"
]

morph_origins = [
    "latin",
    "greek",
    "old-english",
    "modern-english"
]

def validate_morph(morph):
    errors = []

    # Returns true if the key and optional value type are found by the given morph.
    # key_requiredindicates whether errors should be logged if the given key is missing
    # Clause format:
    #key                             valid if the key exists in the morph
    #values
    #  list                          valid if the key's value is any of the elements in the list
    #  dict { "one-or-many": [list] }valid if the key's value is one of the elements in the list, or a list
    #                                      all of whose contents are in the given list
    def evaluate_key(clause, morph, key_required=True, category=None):
        key = clause["key"]
        if key not in morph:
            if key_required:
                if category == None:
                    errors.append("property '" + key + "' is required all morphs")
                else:
                    errors.append("property '" + key + "' is required for morphs of type '" + category + "'")
            return False

        elif "values" in clause:
            if type(clause["values"]) is list:
                accepted = clause["values"]
                if morph[key] not in accepted:
                    errors.append("invalid value '" + str(morph[key]) + "' for property '" + key + "' in morph '" + morph["key"] + "'. Accepted values: " + str(accepted))
                    return False
            elif type(clause["values"] is dict) and "one-or-many" in clause["values"]:
                accepted = clause["values"]["one-or-many"]
                if morph[key] not in accepted and not (type(morph[key]) == list and all(x in accepted for x in morph[key])):
                    errors.append("invalid value '" + str(morph[key]) + "' for property '" + key + "' in morph '" + morph["key"] + "'. Accepted values: " + str(accepted) + ", or a list of these.")
                    return False
            else:
                errors.append("unrecognized validation values requirement: " + str(clause["values"]))

        return True

    # Returns true if any of the tags given in the clause are found in the morph
    def evaluate_tags(clause, morph, category):
        if "tags" not in morph:
            if category == None:
                errors.append("all morphs require one of the following tags: " + str(clause["tags"]))
            else:
                errors.append("morphs of type '" + category + "' require one of the following tags: " + str(clause["tags"]))
            return False

        for tag in clause["tags"]:
            if tag in morph["tags"]:
                return True

        if category == None:
            errors.append("all morphs require one of the following tags: " + str(clause["tags"]))
        else:
            errors.append("morphs of type '" + category + "' require one of the following tags: " + str(clause["tags"]))

        return False

    # Returns true if any of the given clauses are satisfied by the given morph
    # Any format:
    #anylist of clauses, at least one of which must be valid
    def evaluate_any(clauses, morph, category=None):
        for clause in clauses:
            if evaluate_key(clause, morph, False, category):
                return True

        if category == None:
            errors.append("all morphs must contain one of: " + ", ".join([x["key"] for x in clauses]))
        else:
            errors.append("morphs of type '" + category + "' must contain one of: " + ", ".join([x["key"] for x in clauses]))

        return False

    # Checks whether the given requirements are satisfied by the given morph
    def evaluate_requirements(requirements, morph, category=None):
        valid = True
        for requirement in requirements:
            if "any" in requirement:
                valid = evaluate_any(requirement["any"], morph, category) and valid
            elif "tags" in requirement:
                valid = evaluate_tags(requirement, morph, category) and valid
            elif "key" in requirement:
                valid = evaluate_key(requirement, morph, True, category) and valid
            else:
                errors.append("unrecognized validation requirement type: " + str(requirement))

        return valid

    valid = True

    # Properties required by all morphs
    universal_requirements = [
        { "key": "key" },
        { "key": "type", "values": morph_types},
        { "key": "origin", "values": morph_origins }
    ]
    valid = valid and evaluate_requirements(universal_requirements, morph)

    # Properties required by morphs of a certain type
    type_requirements = {
        "noun": [
            { "tags": ["count", "mass", "singleton", "uncountable"] },
            { "tags": ["concrete", "abstract"] }
        ],
        "derive": [
            { "key": "derive-from", "values": { "one-or-many": root_types } },
            { "key": "derive-to", "values": { "one-or-many": root_types } }
        ],
        "prep": [
            { "key": "prefix-on", "values": { "one-or-many": root_types }  },
        ],
        "prefix": [
            { "key": "prefix-on", "values": { "one-or-many": root_types }  },
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
                { "key": "conjugation", "values": [0, 1, 2, 3, 4] },
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

    # Check key whitelist
    for key in morph:
        if not key in valid_properties:
            errors.append("Invalid morph property '" + key + "' found in morph '" + morph["key"] + "'")
            valid = False

    # Check tag whitelist
    if "tags" in morph:
        for tag in morph["tags"]:
            if not tag in valid_tags:
                errors.append("Invalid morph tag '" + tag + "' found on morph '" + morph["key"] + "'")
                valid = False

    if len(errors) > 0:
        if "key" in morph:
            Logger.warn(str(len(errors)) + " errors found reading morph '" + morph["key"] + "'")
        else:
            Logger.warn(str(len(errors)) + " errors found reading morph without key: " + str(morph))

        for error in errors:
            Logger.warn(" - " + error)

    return valid
