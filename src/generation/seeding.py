import random

import src.utils.helpers as helpers

from src.models.morph import Morph

# Returns a random number of transformations to apply to the given word
def transform_count(word):
    bag = [
        (1, 5),
        (2, 3)
    ]

    if word.get_origin() == "old-english":
        if word.root_morph().has_tag("speculative"):
            bag = [
                (0, 3),
                (1, 1)
            ]
        elif word.root_morph().has_tag("obscure"):
            bag = [
                (0, 1),
                (1, 5)
            ]
        else:
            bag = [
                (1, 1)
            ]

    return helpers.choose_bag(bag)

# Returns a random root morph to use as the basis for a word
def seed_root(morphothec):
    languages_and_weights = [
        ["latin", 1],
        ["greek", 1],
        ["old-english", 0.5]
    ]

    bag = [(language, int(morphothec.root_count(language=language) * weight)) for language, weight in languages_and_weights]
    choice = helpers.choose_bag(bag)

    if choice == "latin":
        weights = { "number": 0.5 }
        root = get_root_by_type(choice, weights, morphothec)
    elif choice == "greek":
        weights = { "number": 0.8 }
        root = get_root_by_type(choice, weights, morphothec)
    elif choice == "old-english":
        expressions = [
            ({ "has-tag": "speculative"}, 2),
            ({ "has-tag": "obscure"}, 2),
            ({ "not": { "has-any-tags": ["speculative", "obscure"] } }, 1)
        ]
        root = get_root(choice, expressions, morphothec)

    return root

# Get a random root from the given language, randomly choosing a filter by weight
def get_root(language, expression_weights, morphothec):
    expression = helpers.choose_bag(expression_weights)
    choices = morphothec.filter(language, expression)
    morph = random.choice(choices)
    return Morph(morph)

# Get a random root from the given language, weighted by type count
def get_root_by_type(language, type_weights, morphothec):
    def weight_for(t):
        if t in type_weights:
            return type_weights[t]
        else:
            return 1

    bag = [(t, int(morphothec.root_count(language=language, type=t) * weight_for(t))) for t in ["noun", "adj", "verb", "number"]]
    type = helpers.choose_bag(bag)
    choices = morphothec.filter_type(type, language)
    key = random.choice(choices)
    return Morph.with_key(key, morphothec)
