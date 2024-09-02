import random

import src.models

import src.generation.derivative_morphs as derivative_morph
import src.generation.former as former
import src.utils.helpers as helpers

from src.models.word import Word
from src.models.morph import Morph
from src.morphs.morphothec import Morphothec
from src.utils.logging import Logger

# For ad-hoc morphs
# TODO: Move these
import src.evolutor.evolutor as evolutor
from src.evolutor.engine.config import Config

def seed_word(word, morphothec):
    bag = [
        ("latin", morphothec.root_count_for_language("latin")),
        ("greek", morphothec.root_count_for_language("greek")),
        ("old-english", int(morphothec.root_count_for_language("old-english") * 0.7))
    ]
    choice = helpers.choose_bag(bag)
    if choice == "latin":
        word.morphs = [get_latin_root(morphothec)]
    elif choice == "greek":
        word.morphs = [get_greek_root(morphothec)]
    elif choice == "old-english":
        word.morphs = [get_old_english_root(morphothec)]

def get_latin_root(morphothec):

    bag = [
        ("noun", 3),
        ("adj", 3),
        ("verb", 5)
    ]

    type_ = helpers.choose_bag(bag)
    key = random.choice(morphothec.filter_type(type_, "latin"))
    morph = Morph.with_key(key, morphothec)
    return morph

def get_greek_root(morphothec):

    bag = [
        ("noun", 3),
        ("adj", 1),
        ("verb", 3)
    ]

    type_ = helpers.choose_bag(bag)
    key = random.choice(morphothec.filter_type(type_, "greek"))
    morph = Morph.with_key(key, morphothec)
    return morph

def get_old_english_root(morphothec):

    bag = [
        ("speculative", 2),
        ("obscure", 2),
        ("common", 1)
    ]

    freq = helpers.choose_bag(bag)
    key = random.choice(morphothec.filter_freq(freq, "old-english"))
    morph = Morph.with_key(key, morphothec)
    return morph
 
def transform_word(word, morphothec, is_single):
    language = word.get_origin()
    current_type = word.get_type()

    last_morph = word.last_morph()
    first_morph = word.first_morph()
    root_morph = word.root_morph()
    has_prep = first_morph.get_type() == "prep"
    has_prefix = first_morph.get_type() == "prefix"

    relational_suffixes = []
    numerical_suffixes = []
    if language == "latin":
        relational_suffixes = ["-ate", "-al", "-al", "-ary", "-ify"]
        numerical_suffixes = ["-al-number"]
    elif language == "greek":
        relational_suffixes = ["-ic", "-y-relative", "-ize/greek"]
        numerical_suffixes = ["-ic-number", "-y-number"]
    elif language == "old-english":
        numerical_suffixes = ["-ed-having"]

    choice = None
    override = False
    bag = []
    
    # Conditions and probabilities --------------------------
    
    if last_morph.is_root() or last_morph.suffixes() is None or len(last_morph.suffixes()) > 0:
        if last_morph.has_tag("suffix-only"):
            override = True
            choice = "add_suffix"
        else:
            if root_morph.has_tag("past-participle"):
                bag.append(("add_suffix", 5))    
            else:
                bag.append(("add_suffix", 100))
        
    if word.size() == 1 and current_type == "verb" and not last_morph.has_tag("no-prep") and not has_prep and not has_prefix:
        if last_morph.has_tag("always-prep"):
            override = True
            choice = "add_prep_prefix"
        else:
            if language == "greek" and not first_morph.has_tag("motion"):
                bag.append(("add_prep_prefix", 10))
            else:
                bag.append(("add_prep_prefix", 33))

    if not first_morph.get_type() == "prefix":
        if len(morphothec.filter_prepends_to(current_type, language, { "has-type": "prefix" })) > 0:
            if root_morph.has_tag("past-participle"):
                bag.append(("add_prefix", 20))
            else:
                bag.append(("add_prefix", 5))

        if len(morphothec.filter_prepends_to(current_type, "modern-english", { "has-type": "prefix" })) > 0:
            bag.append(("add_modern_prefix", 5))
    
    if len(relational_suffixes) > 0 and word.size() == 1 and current_type == "noun":
        bag.append(("relational", 10))

    if len(numerical_suffixes) > 0 and word.size() == 1 and current_type == "noun" and last_morph.has_tag("count"):
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

    # Show an alternate form for common words
    if alternate_form != None:
        bag.append(("alternate_form", 10))

    # Show alternate gloss
    if "gloss-alt" in root_morph.morph:
        bag.append(("alternate_gloss", 10))

    # Show alternate form and gloss
    if alternate_form != None \
        and "gloss-alt" in root_morph.morph:
        bag.append(("alternate_form_and_gloss", 30))

    # Past participle
    past_participle_form = None
    if language == "old-english" \
        and root_morph.get_type() == "verb" \
        and root_morph.has_tag("transitive") \
        and (root_morph.morph["verb-class"] != "weak" or (not root_morph.has_tag("obscure") and not root_morph.has_tag("speculative"))):
        # TODO: Use a context property instead of manually setting these overrides
        config = Config(overrides=[["PPart:use-strong", True], ["OSL:iy", False], ["OSL:u", False]])
        form = root_morph.morph["form-raw"]
        if isinstance(form, list):
            form = random.choice(form)
        past_participle_form = evolutor.get_participle_form(form, root_morph.morph["verb-class"], config)

    if past_participle_form != None:
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
        
        new_morph = None
        
        if last_morph.suffixes() is None:
            # For morphs with unrestricted suffixing, choose based on type
            env = word.suffix_environment()
            suffixes = morphothec.filter_appends_to(current_type, language)
            suffixes = [suff for suff in suffixes if Morph.with_key(suff, morphothec).meets_requirements(env)]
    
            if len(suffixes) > 0:        
                choice = random.choice(suffixes)
                new_morph = Morph.with_key(choice, morphothec)
            else:
                Logger.error("No valid suffixes following morph:")
                Logger.error(" - " + last_morph.morph)
                
        else:
            # For words ending in suffixes with restriction, choose from their valid list
            suffixes = last_morph.suffixes()
            choice = random.choice(suffixes)
            new_morph = Morph.with_key(choice, morphothec)
            
        if new_morph is not None:
            word.add_suffix(new_morph)

    # Add Preposition
    elif choice == "add_prep_prefix":
        env = word.prefix_environment()
        prepositions = morphothec.filter_prepends_to(current_type, language, { "has-type": "prep" })
        prepositions = [prep for prep in prepositions if Morph.with_key(prep, morphothec).meets_requirements(env)]
                
        if len(prepositions) > 0:
            choice = random.choice(prepositions)
            new_morph = Morph.with_key(choice, morphothec)
            word.add_prefix(new_morph)
            
    # Add Prefix
    elif choice == "add_prefix":
        env = word.prefix_environment()
        prefixes = morphothec.filter_prepends_to(current_type, language, { "has-type": "prefix" })
        prefixes = [pref for pref in prefixes if Morph.with_key(pref, morphothec).meets_requirements(env)]

        if len(prefixes) > 0:
            choice = random.choice(prefixes)
            new_morph = Morph.with_key(choice, morphothec)
            word.add_prefix(new_morph)
        else:
            return False
    
    # Add Modern Prefix
    elif choice == "add_modern_prefix":
        env = word.prefix_environment()
        prefixes = morphothec.filter_prepends_to(current_type, "modern-english", { "has-type": "prefix" })
        prefixes = [pref for pref in prefixes if Morph.with_key(pref, morphothec).meets_requirements(env)]

        if len(prefixes) > 0:
            choice = random.choice(prefixes)
            new_morph = Morph.with_key(choice, morphothec)
            word.add_prefix(new_morph)

    # Relational
    elif choice == "relational":
        env = word.prefix_environment()
        prepositions = morphothec.filter_prepends_to(current_type, language, { "has-type": "prep" })
        prepositions = [prep for prep in prepositions if Morph.with_key(prep, morphothec).meets_requirements(env)]

        if len(prepositions) > 0:
            choice = random.choice(prepositions)
            prep_morph = Morph.with_key(choice, morphothec)
            end_morph = Morph.with_key(random.choice(relational_suffixes), morphothec )
            word.add_affixes(prep_morph, end_morph)
    
    # Numerical
    elif choice == "numerical":
        env = word.prefix_environment()
        numbers = morphothec.filter_type("number", language)
        numbers = [num for num in numbers if Morph.with_key(num, morphothec).meets_requirements(env)]

        if len(numbers) > 0:
            choice = random.choice(numbers)
            num_morph = Morph.with_key(choice , morphothec)
            end_morph = Morph.with_key(random.choice(numerical_suffixes), morphothec)
            word.add_affixes(num_morph, end_morph)

    # Alternate form
    elif choice == "alternate_form" and alternate_form != None:
        new_morph = derivative_morph.with_alternate_form(root_morph, alternate_form)
        word.set_morphs([new_morph])

        # TODO: Add a small chance to not use the special gloss, and return False
        # so we can get more transforms with an alternate form

    # Alternate gloss
    elif choice == "alternate_gloss":
        new_morph = derivative_morph.with_alternate_gloss(root_morph)
        word.set_morphs([new_morph])

        # Most of the time, don't count this as a transform
        if random.randint(1, 4) > 1:
            return False

    # Alternate form and gloss
    elif choice == "alternate_form_and_gloss" and alternate_form != None:
        new_morph = derivative_morph.with_alternate_form_and_gloss(root_morph, alternate_form)
        word.set_morphs([new_morph])

    elif choice == "past-participle":
        is_common = (not root_morph.has_tag("obscure") and not root_morph.has_tag("speculative"))
        canon_participles = []
        if "form-participle-canon" in root_morph.morph:
            canon_participles = root_morph.morph["form-participle-canon"]

        new_morph = derivative_morph.from_past_participle(root_morph, past_participle_form)
        word.set_morphs([new_morph])

        # HACK: I want common participles to always be put through at least one more transform.
        # Pretend that we failed a transform if the participle is in the canon list.
        # This only applies to common roots.
        #
        # Also do this randomly for all participles
        if (
            len(canon_participles) > 0
            and new_morph.morph["form-final"] in canon_participles \
            and is_common \
           ) \
            or random.randint(0, 9) == 0:
            return False

    return True
