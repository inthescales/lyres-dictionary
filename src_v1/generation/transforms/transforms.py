import random

import src.evolutor.participles as participle
import src.generation.former as former
import src.generation.sense_choice as sense_choice
import src.utils.helpers as helpers

from src.evolutor.engine.config import Config
from src.generation.transforms.transform_context import TransformContext
from src.generation.transforms.transform_result import TransformResult
from src.generation.transforms.type.add_modern_prefix import AddModernPrefixTransform
from src.generation.transforms.type.add_prefix import AddPrefixTransform
from src.generation.transforms.type.add_preposition import AddPrepositionTransform
from src.generation.transforms.type.add_suffix import AddSuffixTransform
from src.generation.transforms.type.alternate_form import AlternateFormTransform
from src.generation.transforms.type.alternate_form_and_sense import AlternateFormAndSenseTransform
from src.generation.transforms.type.alternate_sense import AlternateSenseTransform
from src.generation.transforms.type.numerical_circumfix import NumericalCircumfixTransform
# from src.generation.transforms.type.past_participle import PastParticipleTransform
from src.generation.transforms.type.relational_circumfix import RelationalCircumfixTransform
from src.utils.logging import Logger

# Transform Lists ==================================

# Transforms that modify the form or meaning of a simplex root

root_transforms = [
    AlternateFormTransform,
    AlternateSenseTransform,
    AlternateFormAndSenseTransform,
    # PastParticipleTransform # Disabled until the ad-hoc morph creation is updated
]

# Transforms that build up a word, e.g. by adding affixes

building_transforms = [
    AddSuffixTransform,
    AddPrepositionTransform,
    AddPrefixTransform,
    AddModernPrefixTransform,
    RelationalCircumfixTransform,
    NumericalCircumfixTransform
]

all_transforms = root_transforms + building_transforms

# Functions ========================================

def get_context(word, morphothec, is_single):
    root_morph = word.root_morph()
    rand = random.Random(root_morph.seed)

    formset = root_morph.get_formset()

    # Find any relevant canon form
    canon_form = None
    if formset != None and len(formset.canon_forms) > 0:
        canon_paradigms = helpers.list_if_not(formset.canon_forms[0].canon.paradigm)
        canon_form = rand.choice(canon_paradigms).lemma

    # See if an alternate form is available
    # TODO: Find a way to generate all possible alt. forms rather than relying on rolling one
    alternate_form = None
    if formset != None and len(formset.canon_forms) > 0:
        metaform = rand.choice(formset.all)
        paradigms = helpers.list_if_not(metaform.paradigm)
        form = rand.choice(paradigms).lemma
        env = word.environment_for_index(0)
        config = former.Former_Config(True, False, seed=root_morph.seed)
        evolved_form = former.evolve(form, root_morph)
        if evolved_form != canon_form:
            alternate_form = evolved_form
    
    # See if an alternate sense is available
    alternate_sense = None
    earlier_senses = sense_choice.all_nonrecent(root_morph.all_senses(), root_morph.get_origin(), root_morph.seed)
    if len(earlier_senses) > 0:
        alternate_sense = rand.choice(earlier_senses)

    # Generate a past participle form if possible
    past_participle_form = None
    if "form-oe" in root_morph.morph and "verb-class" in root_morph.morph: # Disabled until the ad-hoc morph creation is updated
        config = Config(overrides=[["PPart:use-strong", True], ["OSL:iy", False], ["OSL:u", False]])
        metaform = rand.choice(formset.all)
        paradigms = helpers.list_if_not(metaform.paradigm)
        form = rand.choice(paradigms).lemma
        past_participle_form = participle.oe_form_to_ne_participle(form, root_morph.morph["verb-class"], config)

    return TransformContext(morphothec, canon_form, alternate_form, alternate_sense, past_participle_form)

# Returns a variant form of a single-morph root, if it is possible to get one
# Returns whether this should consume a transform
def variant_root(word, morphothec):
    if len(word.morphs) == 1:
        result = transform_word(word, morphothec, False, transforms=root_transforms)
        if result.success:
            print("--- ROOT TRANSFORMED ---")
        return result.free
    else:
        return False

def transform_word(word, morphothec, is_single, transforms=all_transforms):
    # Get transform context

    context = get_context(word, morphothec, is_single)

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
