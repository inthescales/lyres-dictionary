import random

import src.models

import src.generation.derivative_morphs as derivative_morph
import src.generation.former as former
import src.utils.helpers as helpers

from src.generation.transforms.transform_context import TransformContext
from src.generation.transforms.transform_result import TransformResult
from src.generation.transforms.type.add_suffix import AddSuffixTransform
from src.generation.transforms.type.add_preposition import AddPrepositionTransform
from src.generation.transforms.type.add_prefix import AddPrefixTransform
from src.generation.transforms.type.add_modern_prefix import AddModernPrefixTransform
from src.generation.transforms.type.relational_circumfix import RelationalCircumfixTransform
from src.generation.transforms.type.numerical_circumfix import NumericalCircumfixTransform
from src.generation.transforms.type.alternate_form import AlternateFormTransform
from src.generation.transforms.type.alternate_gloss import AlternateGlossTransform
from src.generation.transforms.type.alternate_form_and_gloss import AlternateFormAndGlossTransform
from src.generation.transforms.type.past_participle import PastParticipleTransform

from src.models.word import Word
from src.models.morph import Morph
from src.morphs.morphothec import Morphothec
from src.utils.logging import Logger

# For alternate and participle forms
import src.evolutor.evolutor as evolutor
from src.evolutor.engine.config import Config

def seed_word(word, morphothec):
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

    word.morphs = [root]

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

def transform_word(word, morphothec, is_single):
    bag = []

    # Prepare transform context

    language = word.get_origin()
    root_morph = word.root_morph()

    # See if an alternate form is available
    # TODO: Find a way to generate all possible alt. forms rather than relying on rolling one
    alternate_form = None
    if is_single \
        and "form-canon" in root_morph.morph \
        and not root_morph.has_tag("speculative") \
        and not root_morph.has_tag("obscure"):
            env = word.environment_for_index(0)
            config = former.Former_Config(True, False)
            form = former.form(root_morph, env, config)
            if form != root_morph.morph["form-canon"]:
                alternate_form = form
        
    # Generate a participle form if possible
    past_participle_form = None
    if "form-raw" in root_morph.morph and "verb-class" in root_morph.morph:
        config = Config(overrides=[["PPart:use-strong", True], ["OSL:iy", False], ["OSL:u", False]])
        form = root_morph.morph["form-raw"]
        if isinstance(form, list):
            form = random.choice(form)
        past_participle_form = evolutor.get_participle_form(form, root_morph.morph["verb-class"], config)

    context = TransformContext(morphothec, alternate_form, past_participle_form)

    # List all transforms

    transforms = [
        AddSuffixTransform,
        AddPrepositionTransform,
        AddPrefixTransform,
        AddModernPrefixTransform,
        RelationalCircumfixTransform,
        NumericalCircumfixTransform,
        AlternateFormTransform,
        AlternateGlossTransform,
        AlternateFormAndGlossTransform,
        PastParticipleTransform
    ]

    # Check for overrides

    override_transform = None
    for transform in transforms:
        if transform.override(word):
            if override_transform != None:
                Logger.error("Multiple overrides for word with morphs: " + str(word.morphs))

            override_transform = transform
            break

    if override_transform != None:
        return override_transform.apply(word, context)

    # Choose transform

    bag = [(t, t.weight(word)) for t in transforms if t.is_eligible(word, context)]
    if len(bag) == 0:
        return TransformResult(False)

    transform = helpers.choose_bag(bag)

    # Apply transform

    Logger.trace("applied transform '" + transform.name + "'")

    return transform.apply(word, context)
