import random

import src.models

import src.generation.derivative_morphs as derivative_morph
import src.generation.former as former
import src.utils.helpers as helpers

from src.generation.transform_context import TransformContext
from src.generation.transform_type.add_suffix import AddSuffixTransform
from src.generation.transform_type.add_preposition import AddPrepositionTransform
from src.generation.transform_type.add_prefix import AddPrefixTransform
from src.generation.transform_type.add_modern_prefix import AddModernPrefixTransform
from src.generation.transform_type.relational_circumfix import RelationalCircumfixTransform
from src.generation.transform_type.numerical_circumfix import NumericalCircumfixTransform
from src.generation.transform_type.alternate_form import AlternateFormTransform
from src.generation.transform_type.alternate_gloss import AlternateGlossTransform
from src.generation.transform_type.alternate_form_and_gloss import AlternateFormAndGlossTransform
from src.generation.transform_type.past_participle import PastParticipleTransform

from src.models.word import Word
from src.models.morph import Morph
from src.morphs.morphothec import Morphothec
from src.utils.logging import Logger

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
    language = word.get_origin()
    current_type = word.get_type()

    last_morph = word.last_morph()
    first_morph = word.first_morph()
    root_morph = word.root_morph()

    choice = None
    override = False
    bag = []
    
    # Conditions and probabilities --------------------------
    
    if AddSuffixTransform.is_eligible(word):
        if AddSuffixTransform.override(word):
            override = True
            choice = "add_suffix"
        else:
            if root_morph.has_tag("past-participle"):
                bag.append(("add_suffix", 5))    
            else:
                bag.append(("add_suffix", 100))
        
    if AddPrepositionTransform.is_eligible(word):
        if AddPrepositionTransform.override(word):
            override = True
            choice = "add_prep_prefix"
        else:
            if language == "greek" and not first_morph.has_tag("motion"):
                bag.append(("add_prep_prefix", 10))
            else:
                bag.append(("add_prep_prefix", 33))

    if AddPrefixTransform.is_eligible(word, morphothec):
        if root_morph.has_tag("past-participle"):
            bag.append(("add_prefix", 20))
        else:
            bag.append(("add_prefix", 5))

    if AddModernPrefixTransform.is_eligible(word, morphothec):
        bag.append(("add_modern_prefix", 5))
    
    if RelationalCircumfixTransform.is_eligible(word):
        bag.append(("relational", 10))

    if NumericalCircumfixTransform.is_eligible(word):
        bag.append(("numerical", 5))

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

    context = TransformContext(alternate_form)

    # Show an alternate form for common words
    if AlternateFormTransform.is_eligible(word, context):
        bag.append(("alternate_form", 10))

    # Show alternate gloss
    if AlternateGlossTransform.is_eligible(word,):
        bag.append(("alternate_gloss", 10))

    # Show alternate form and gloss
    if AlternateFormAndGlossTransform.is_eligible(word, context):
        bag.append(("alternate_form_and_gloss", 30))

    # Past participle
    if PastParticipleTransform.is_eligible(word):
        bag.append(("past-participle", 20))

    # If there is no override, choose, or return False if no choices ------
    if not override: 
        if len(bag) > 0:
            choice = helpers.choose_bag(bag)
        else:
            return False
    
    # Transformations --------------------------

    # Add Suffix
    if choice == "add_suffix":
        return AddSuffixTransform.apply(word, morphothec)

    # Add Preposition
    elif choice == "add_prep_prefix":
        return AddPrepositionTransform.apply(word, morphothec)
            
    # Add Prefix
    elif choice == "add_prefix":
        return AddPrefixTransform.apply(word, morphothec)
    
    # Add Modern Prefix
    elif choice == "add_modern_prefix":
        return AddModernPrefixTransform.apply(word, morphothec)

    # Relational
    elif choice == "relational":
        return RelationalCircumfixTransform.apply(word, morphothec)
    
    # Numerical
    elif choice == "numerical":
        return NumericalCircumfixTransform.apply(word, morphothec)

    # Alternate form
    elif choice == "alternate_form":
        return AlternateFormTransform.apply(word, context)

    # Alternate gloss
    elif choice == "alternate_gloss":
        return AlternateGlossTransform.apply(word, context)

    # Alternate form and gloss
    elif choice == "alternate_form_and_gloss":
        return AlternateFormAndGlossTransform.apply(word, context)

    elif choice == "past-participle":
        return PastParticipleTransform.apply(word)

    return True
