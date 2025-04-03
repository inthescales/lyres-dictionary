import src.tools.morphs.morphs_files as file_tool

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
    "fixed-gloss",              # Generation - the gloss of this morph is fixedno additions should be made (e.g. articles, infinitive 'to', etc), and it has no embeds,
    "i-mutating",               # OE morphophonology - causes i-mutation in the joined root
    "y-to-i"                    # MnE orthography - causes a final unstressed 'y' to become 'i' when a consonant is suffixed (e.g. 'day' + '-ly' -> 'daily')
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

def validate_morph(morph, meta_properties):
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
    if "type" in morph and morph["type"] in type_requirements:
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

    if "origin" in morph and morph["origin"] in origin_type_requirements \
        and "type" in morph and morph["type"] in origin_type_requirements[morph["origin"]]:
        valid = valid and evaluate_requirements(origin_type_requirements[morph["origin"]][morph["type"]], morph, " ".join(morph["origin"].split("-")) + " " + morph["type"])

    # Check key whitelist
    for key in morph:
        if not key in meta_properties:
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
            print(str(len(errors)) + " errors found reading morph '" + morph["key"] + "'")
        else:
            print(str(len(errors)) + " errors found reading morph without key: " + str(morph))

        for error in errors:
            print(" - " + error)

    return valid

def validate_morphs(files, meta_dir):
    # Read in metadata
    meta = file_tool.load_metadata(meta_dir)

    # Read in morphs
    morphs = []
    for file in files:
        morphs += file_tool.get_morphs_from(file)

    fail_count = 0
    for morph in morphs:
        if not validate_morph(morph, meta["properties"]):
            fail_count += 1

    if fail_count == 0:
        print("Validation succeeded")
    else:
        print("Validation failed on " + str(fail_count) + " morphs")
