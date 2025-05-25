import random

import src.evolutor.participles as participle
import src.generation.former as former
import src.utils.helpers as helpers

from src.evolutor.engine.config import Config
from src.generation.transforms.transform_context import TransformContext
from src.generation.transforms.transform_result import TransformResult
from src.generation.transforms.type.add_modern_prefix import AddModernPrefixTransform
from src.generation.transforms.type.add_prefix import AddPrefixTransform
from src.generation.transforms.type.add_preposition import AddPrepositionTransform
from src.generation.transforms.type.add_suffix import AddSuffixTransform
from src.generation.transforms.type.alternate_form import AlternateFormTransform
from src.generation.transforms.type.alternate_form_and_gloss import AlternateFormAndGlossTransform
from src.generation.transforms.type.alternate_gloss import AlternateGlossTransform
from src.generation.transforms.type.numerical_circumfix import NumericalCircumfixTransform
from src.generation.transforms.type.past_participle import PastParticipleTransform
from src.generation.transforms.type.relational_circumfix import RelationalCircumfixTransform
from src.utils.logging import Logger

def get_context(word, morphothec, is_single):
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
        form = helpers.one_or_random(root_morph.morph["form-raw"], seed=root_morph.seed)
        past_participle_form = participle.oe_form_to_ne_participle(form, root_morph.morph["verb-class"], config)

    return TransformContext(morphothec, alternate_form, past_participle_form)

def transform_word(word, morphothec, is_single):
    # Get transform context

    context = get_context(word, morphothec, is_single)

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
