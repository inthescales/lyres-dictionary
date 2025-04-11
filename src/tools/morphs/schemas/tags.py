tags = [
    "count",                    # Noun countability - countable
    "mass",                     # Noun countability - mass
    "singleton",                # Noun countability - singleton, e.g. "The Earth"
    "uncountable",              # Noun countability - generically uncountable, will never use articles
    "concrete",                 # Noun actuality - a concrete object in the world
    "abstract",                 # Noun actuality - something not physically in the world
    "bounded",                  # Noun actuality - optionally for abstracts, does it have a bounded aspect (e.g. a length of time)
    "fluid",                    # Noun semantics - a fluid, like a liquid or gas
    "liquid",                   # Noun semantics - a liquid
    "gas",                      # Noun semantics - a gas
    "living",                   # Noun semantics - a living being
    "animal",                   # Noun semantics - an animal
    "tame",                     # Noun semantics - a tame animal
    "wild",                     # Noun semantics - a wild animal
    "mammal",                   # Noun semantics - a mammal
    "plant",                    # Noun semantics - a plant
    "tree",                     # Noun semantics - a kind of tree
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
    "terrain",                  # Noun semantics - a type of land
    "region",                   # Noun semantics - a region
    "place",                    # Noun semantics - a specific place (e.g. hell, home, the sky)
    "weather",                  # Noun semantics - a type of weather
    "material",                 # Noun semantics - a material things can be made out of
    "metal",                    # Noun semantics - a metal
    "metallic",                 # Noun semantics - an object made from metal
    "shiny",                    # Noun semantics - reflects light
    "luminous",                 # Noun semantics - emits light
    "glooming",                 # Noun semantics - obscures light or darkens (esp. of weather and times)
    "man-made",                 # Noun semantics - something made by humans
    "garment",                  # Noun semantics - a garment, or anything that is worn on the body
    "tool",                     # Noun semantics - a tool
    "weapon",                   # Noun semantics - a weapon
    "vessel",                   # Noun semantics - a vessel (containers and boats)
    "food",                     # Noun semantics - a food or ingredient of food    
    "grouping",                 # Noun semantics - a group or collection of things
    "color",                    # Noun semantics - a color
    "shape",                    # Noun semantics - a shape
    "quality",                  # Noun semantics - an abstract quality
    "body-state",               # Noun semantics - a bodily condition
    "mind-state",               # Noun semantics - a mental or emotional state
    "activity",                 # Noun semantics - an activity that a person can undertake
    "time",                     # Noun semantics - a period of time
    "time-of-day",              # Noun semantics - a time of the day (e.g. morning, dawn)
    "time-of-year",             # Noun semantics - a time of the year (e.g. winter, lent)
    "measure",                  # Noun semantics - a unit of measure
    "number",                   # Noun semantics - a number (used as a noun)
    "past-participle",          # Adjective morphology - the 'adjective' is the past participle of a verb
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
    "numerical",                # Number semantics - a numerical meaning (but not a cardinal number)
    "cardinal",                 # Number semantics - a cardinal number (one, two, three, etc)
    "ordinal",                  # Number semantics - an ordinal number (first, second, third, etc)
    "distributive",             # Number semantics - a distributive number (as Latin unī, bīnī, ternī, etc)
    "multiplicative",           # Number semantics - a multiplicative number (as Latin simplex, duplex, triplex, etc.)
    "proportional",             # Number semantics - a proportional number (as Latin simplus, duplus, triplus, etc.)
    "no-head-joiner",           # Form - Doesn't take joining vowels on the front end
    "no-tail-joiner",           # Form - Doesn't take joining vowels on the back end
    "no-length",                # Usage - does not count towards maximum morph count
    "obscure",                  # Usage - the morph is attested in modern English, but only in archaic texts or minor dialects
    "poetic",                   # Usage - the morph is only attested in poetic usage in its original language
    "speculative",              # Usage - the morph is not attested in modern English
    "homophonic",               # Usage - the morphs processed form is a homophone (or nearly) with a common actual word
    "rare",                     # Generation - occurs less often in generation
    "super-rare",               # Generation - occurs even less often in generation
    "no-gen",                   # Generation - will not be chosen randomly in generation, only if specified as allowed suffix
    "final",                    # Generation - immediately ends generation
    "non-final",                # Generation - cannot be the final morph in the word
    "suffix-only",              # Generation - adding a suffix is the only valid transformation following this morph
    "fixed-gloss",              # Generation - the gloss of this morph is fixedno additions should be made (e.g. articles, infinitive 'to', etc), and it has no embeds,
    "i-mutating",               # OE morphophonology - causes i-mutation in the joined root
    "y-to-i"                    # MnE orthography - causes a final unstressed 'y' to become 'i' when a consonant is suffixed (e.g. 'day' + '-ly' -> 'daily')
]

tag_dependencies = {
    "animal": ["mammal", "tame", "wild"],
    "bodypart": ["bodypart-single", "bodypart-plant"],
    "man-made": ["food", "garment", "tool", "weapon"],
    "material": ["food", "metal"],
    "plant": ["tree"],
    "person": ["role", "ruler"],
    "time": ["time-of-day", "time-of-year"]
}

tag_dependency_map = {}
for key, values in tag_dependencies.items():
    for tag in values:
        if tag not in tag_dependency_map:
            tag_dependency_map[tag] = []

        tag_dependency_map[tag].append(key)
